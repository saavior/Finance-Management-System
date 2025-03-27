#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:17:57 2025

@author: davidsalvadormediavilla
"""

import nest_asyncio
nest_asyncio.apply()

import flet as ft
from navigation import NavigationManager
from screens.login import LoginScreen  # or do a local import in the code below if needed

def main(page: ft.Page):
    page.title = "Finance Management System"
    page.bgcolor = ft.Colors.WHITE
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.window_width = 800
    page.window_height = 600

    nav_manager = NavigationManager()
    login_screen = LoginScreen(nav_manager)
    login_screen.show(page)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
