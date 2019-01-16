# -*- coding: utf-8 -*-

import json


class ConfigReader (object):

    def __init__(self, filename):
        """Read config data from filename."""
        self._filename = filename
        self._data = None

    def _read_file(self):
        """Read & parse data."""
        with open(self._filename, 'r') as cfg:
            contents = cfg.read()
        self._data = json.loads(contents)
