# -*- coding: utf-8 -*-

from configmgr import ConfigReader
from gui import ServiceManagerGUI

class Coordinator (object):
    """Keeps everything in sync and coordinates program efforts."""

    def __init__(self):
        """Instantiate the program.  No arguments."""
        self.config = ConfigReader('services.json', self)
        self.config.read()
        self.gui = ServiceManagerGUI(self)
        self.gui.start()


if __name__ == '__main__':
    c = Coordinator()
