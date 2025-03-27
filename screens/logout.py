#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:24:13 2025

@author: davidsalvadormediavilla
"""

import flet as ft
# Removed top-level import of LoginScreen

class LogoutScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page):
        page.controls.clear()

        def confirm_yes(e):
            # Local import to break circular dependency
            from screens.login import LoginScreen
            LoginScreen(self.nav_manager).show(page)

        def confirm_no(e):
            # Instead of returning to nav_manager.current(),
            # always return to DashboardScreen.
            from screens.dashboard import DashboardScreen
            DashboardScreen(self.nav_manager).show(page)

        logout_view = ft.Column([
            ft.Text("Are you sure you want to logout?", size=24, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            ft.Row([
                ft.ElevatedButton("Yes", on_click=confirm_yes, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE),
                ft.ElevatedButton("No", on_click=confirm_no, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
            ], alignment="center", spacing=20)
        ], horizontal_alignment="center", alignment=ft.alignment.center, spacing=20)

        page.controls.append(logout_view)
        page.update()
