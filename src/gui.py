# -*- coding: utf-8 -*-
# Python 3 only

import tkinter as tk


class ServiceManagerGUI (object):

    def __init__(self, coordinator):
        """Start the GUI."""
        self.coordinator = coordinator

        self.name = 'main'
        self.root = tk.Tk()
        self.root.resizeable(False, False)

        self.variables = {}

    def _add_changinglabel(self, text, varname, root=None, label_opts=None,
                           **grids):
        """Adds a label that uses a variable for its text."""
        label_opts = label_opts or {}
        root = root or self.root
        var = tk.StringVar()
        self.variables.update({varname: var})
        var.set(text)
        lbl = tk.Label(root, textvariable=var, **label_opts, **self.colors)
        lbl.grid(**grids)
        return lbl

    def _add_button(self, label, callback, root=None, btn_opts=None, **grids):
        """Adds a tk.Button element to the root window, configures it,
        and grids it to the root."""
        if btn_opts is None:
            btn_opts = {}
        if root is None:
            root = self.root
        btn = tk.Button(root, text=label, command=callback,
                        **btn_opts, **self.colors)
        btn.grid(**grids)
        return btn
