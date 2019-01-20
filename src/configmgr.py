# -*- coding: utf-8 -*-

import json
from servicemgr import Service


class ConfigReader (object):

    def __init__(self, filename, coordinator):
        """Read config data from filename."""
        self._filename = filename
        self._data = None
        self._services = []
        self.coordinator = coordinator

    def _read_file(self):
        """Read & parse data."""
        with open(self._filename, 'r') as cfg:
            contents = cfg.read()
        self._data = json.loads(contents)
        for service in self._data['services']:
            self._services.append(
                Service(service['name'], service['computer_name'],
                        service['start'], service['stop'], self.coordinator)
            )

    @property
    def services_list(self):
        """Get a list of the services provided in the config."""
        return self._services
