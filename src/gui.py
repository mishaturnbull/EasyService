# -*- coding: utf-8 -*-
# Python 3 only

import tkinter as tk
from tkinter import ttk


class ServiceManagerGUI (object):

    def __init__(self, coordinator):
        """Start the GUI."""
        self.coordinator = coordinator

        self.name = 'main'
        self.root = tk.Tk()
        self.root.resizable(False, False)

        self.variables = {}

    def start(self):
        """Build the GUI!"""
        self._spawn_gui()
        self.root.mainloop()

    def _add_label(self, text, root=None, label_opts=None, **grids):
        """Adds a tk.Label element to the root window and grids it
        using the **args provided."""
        if label_opts is None:
            label_opts = {}
        if root is None:
            root = self.root
        lbl = tk.Label(root, text=text, **label_opts).grid(**grids)
        return lbl

    def _add_changinglabel(self, text, varname, root=None, label_opts=None,
                           **grids):
        """Adds a label that uses a variable for its text."""
        label_opts = label_opts or {}
        root = root or self.root
        var = tk.StringVar()
        self.variables.update({varname: var})
        var.set(text)
        lbl = tk.Label(root, textvariable=var, **label_opts)
        lbl.grid(**grids)
        return lbl

    def _add_button(self, label, callback, root=None, btn_opts=None, **grids):
        """Adds a tk.Button element to the root window, configures it,
        and grids it to the root."""
        if btn_opts is None:
            btn_opts = {}
        if root is None:
            root = self.root
        btn = tk.Button(root, text=label, command=callback, **btn_opts)
        btn.grid(**grids)
        return btn

    def _spawn_gui(self):
        """Spawn the basic GUI elements"""
        self.root.wm_title("EasyService Manager")
        self._notebook = ttk.Notebook(self.root)
        self._notebook.grid(row=0, column=0, sticky='nesw')

        for category in self.coordinator.config.categories.keys():
            self._spawn_page(category)

    def _spawn_page(self, category):
        """Given a category, spawn a page for it."""
        page = tk.Frame(self._notebook)
        self._notebook.add(page, text=category, compound=tk.TOP)

        self._add_label("Service", root=page, row=0, column=0)
        self._add_label("Status", root=page, row=0, column=1)
        self._add_label("Options", root=page, row=0, column=2, columnspan=2)

        i = 1
        for service in self.coordinator.config.categories[category]:
            self._add_service_line(service, page, i)
            i += 1

    def _add_service_line(self, service, root, row):
        """Given a Service object, add a line in the GUI for it"""
        self._add_label(service.friendly_name, root=root, row=row, column=0)
        self._add_changinglabel('Status',
                                '{}_state'.format(service.computer_name),
                                root=root,
                                row=row, column=1)
        self._add_button('Start', service.start, root=root, row=row,
                         column=2)
        self._add_button('Stop', service.stop, root=root, row=row,
                         column=3)
