# -*- coding: utf-8 -*-
# Python 3 only

import threading
import subprocess
import functools


@functools.lru_cache()
def parse_lsof_output(output, desired_service):
    """Given a text output from an lsof command run,
    see if a service is running or not."""
    lines = output.split('\n')
    for line in lines:
        l = line.strip()
        if not l.startswith(desired_service):
            continue
        else:
            return True
    return False


class Service (object):
    """Represents a service that can be started/stopped/etc."""

    def __init__(self, friendly_name, computer_name, start_cmd, stop_cmd,
                 category, coordinator):
        """Create a Service object that can be started or stopped."""
        self.friendly_name = friendly_name
        self.computer_name = computer_name
        self.start_cmd = start_cmd
        self.stop_cmd = stop_cmd
        self.coordinator = coordinator
        self.is_running = None
        self.category = category
        self.queue_auto_state_update()

    def queue_auto_state_update(self):
        """Iff the coordinator exists, and iff the GUI exists,
        then try to auto update the state and push it to the user."""
        if self.coordinator is not None:
            if hasattr(self.coordinator, 'gui'):
                self.check_running(self.coordinator.gui.variables[
                                       '{}_state'.format(self.computer_name)
                                   ])

    def _send_status(self, status_msg):
        """Send a status message update to the GUI"""
        if hasattr(self.coordinator, 'gui'):
            statemsg = self.coordinator.gui.variables[
                '{}_state'.format(self.computer_name)
            ]
            statemsg.set(status_msg)

    def start(self):
        """Start the service."""
        if self.is_running:
            pass
        else:
            self._send_status("Starting...")
            CommandExecutor(self.start_cmd, self.coordinator, False).start()
            self.is_running = True
        self.queue_auto_state_update()

    def stop(self):
        """Stop the service."""
        if not self.is_running:
            pass
        else:
            self._send_status("Stopping...")
            CommandExecutor(self.stop_cmd, self.coordinator, False).start()
            self.is_running = False
        self.queue_auto_state_update()

    def check_running(self, store_is_running=None):
        """Returns True if the service is running, or False if it's not.
        Probabilistic -- false returns are not guaranteed, but True returns
        are guaranteed to be correct.  Uses `lsof` under the hood."""

        def _is_running():

            cmd = CommandExecutor("lsof | tr -s ' ' | cut -d' ' -f1,4 | grep {}".format(
                self.computer_name
            ), self.coordinator)
            cmd.start()
            cmd.join()
            status = parse_lsof_output(cmd.get_output()['stdout'],
                                       self.computer_name)
            return status

        if store_is_running is None:
            self.is_running = _is_running()
            return self.is_running
        else:
            # store_is_running must be a bool-ish object with a .set() method
            # i.e. a Tkinter BoolVar() or something that does the same thing
            assert hasattr(store_is_running, 'set'), "Must be a set-able boolean"

            def check_run():
                status = _is_running()
                store_is_running.set("Running" if status else "Stopped")
            pce = _PyCodeExecutor(check_run, self.coordinator)
            pce.start()


class _PyCodeExecutor (threading.Thread):
    """Similar to CommandExecutor, but for arbitrary Python code, not
    Bash commands."""

    def __init__(self, func, coordinator):
        """Set up the execution thread."""
        super(_PyCodeExecutor, self).__init__()
        self.func = func
        self.coordinator = coordinator

    def run(self):
        self.func()


class CommandExecutor (threading.Thread):

    def __init__(self, command, coordinator, suppress_stderr=True):
        """Do something"""
        super(CommandExecutor, self).__init__()

        self._command = command
        self.coordinator = coordinator
        self._result = None
        self.suppress_stderr = suppress_stderr

    def _do_cmd(self):
        """Internal execution"""
        self._result = subprocess.run(self._command, capture_output=True,
                                      shell=True)
        output = self.get_output()
        if output['stderr'] != '' and not self.suppress_stderr:
            print(output['stderr'])

    def get_output(self):
        """Return the string version of the completed StdOut from the command."""
        out = {}
        if self._result is None:
            return
        out.update(returncode=self._result.returncode,
                   stdout=self._result.stdout.decode('utf-8'),
                   stderr=self._result.stderr.decode('utf-8'))
        return out

    def run(self):
        """Execute the command"""
        self._do_cmd()


if __name__ == '__main__':
    class A(object):
        def __init__(self):
            self.val = None
        def set(self, q):
            self.val = q
    n = Service("Nessus", 'nessusd', '/etc/init.d/nessusd start',
                '/etc/init.d/nessusd stop', 'scanning', None)
    a = A()
