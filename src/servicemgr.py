# -*- coding: utf-8 -*-
# Python 3 only

import threading
import subprocess


class CommandExecutor (threading.Thread):

    def __init__(self, command, coordinator):
        """Do something"""
        super(CommandExecutor, self).__init__()

        self._command = command
        self.coordinator = coordinator

    def _do_cmd(self):
        """Internal execution"""
        subprocess.run(self._command,)

    def run(self):
        """Execute the command"""
        self._do_cmd()
