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
        self._categories = {}

    def _read_file(self):
        """Read & parse data."""
        with open(self._filename, 'r') as cfg:
            contents = cfg.read()
        self._data = json.loads(contents)
        categories = self._data['categories']

        for category in categories:
            self._categories.update({category: []})

        for service in self._data['services']:
            svo = Service(service['name'], service['computer_name'],
                          service['start'], service['stop'],
                          service['category'], self.coordinator)
            self._services.append(svo)
            self._categories[service['category']].append(svo)


    def read(self):
        """Public interface for reading & parsing data.  Does not return."""
        self._read_file()

    @property
    def services(self):
        """Get a list of the services provided in the config."""
        return self._services

    @property
    def categories(self):
        """Get a dictionary of services by categorization."""
        return self._categories
