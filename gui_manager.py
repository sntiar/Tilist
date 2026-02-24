from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk

@dataclass
class WidgetRules:
    modes: set
    is_readonly: bool

class GuiManager:

    def __init__(self):
        self.registry = {}
        self.modes = {'NORMAL','NEW_TASK','BLOCKED'}
        self.active_mode = 'NORMAL'
       
    def is_registered(self,widget:tk)->bool:
        rules = self._fail_safe(widget)
        return bool(rules)
    
    def remove_destroyed(self,widget):
        self.registry.pop(widget)

    
    def register(self,widget,modes:set,is_readonly:bool):
        self.registry[widget] = WidgetRules(modes,is_readonly)
        self._toggle(widget)

    def _toggle(self,widget):
        rules = self._fail_safe(widget) #rules is short for the dataclass object's name
        if rules is None: return 

        permit = self._should_enable(rules)
        if not permit:
            widget.config(state='disabled')
        else:
            if rules.is_readonly:
                widget.config(state='readonly')
                return
            widget.config(state='normal')

    def _should_enable(self, rules):
       if rules is None: return False
       return self.active_mode in rules.modes
    
    def _fail_safe (self, widget):
        return self.registry.get(widget,None) #look for the key(widget) if is not there return a default value None

    def set_active_mode(self, new_mode):
        if new_mode not in self.modes: return
        self.active_mode = new_mode
        for i in self.registry:
            self._toggle(i)


