#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 20:28:58 2025

@author: davidsalvadormediavilla
"""

from data_structures import Stack

class NavigationManager:
    def __init__(self):
        self.history = Stack()
    
    def push(self, screen):
        self.history.push(screen)
    
    def pop(self):
        return self.history.pop()
    
    def current(self):
        return self.history.peek()
