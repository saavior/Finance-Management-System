#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:19:31 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import login_user
# Note: We do not import LoginScreen here in a circular manner.
import global_vars

class LoginScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page):
        page.controls.clear()

        username_field = ft.TextField(label="Username", width=300)
        password_field = ft.TextField(label="Password", password=True, width=300)
        login_result = ft.Text(color=ft.Colors.RED, size=16, text_align=ft.TextAlign.CENTER)
        show_password_checkbox = ft.Checkbox(
            label="Show Password", 
            value=False, 
            on_change=lambda e: self.toggle_password(password_field, page)
        )

        def on_login(e):
            result = login_user(username_field.value, password_field.value)
            if not result.startswith("Login successful!"):
                login_result.value = "Username or password not valid"
                page.update()
            else:
                parts = result.split("|")
                global_vars.current_user_id = int(parts[1]) if len(parts) == 2 else 1
                global_vars.current_username = username_field.value
                # DO NOT push the login screen; let the dashboard be the base.
                from screens.dashboard import DashboardScreen  # local import
                DashboardScreen(self.nav_manager).show(page)

        login_button = ft.ElevatedButton(
            "Login", on_click=on_login,
            bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE
        )
        def go_to_register(e):
            from screens.register import RegisterScreen  # local import
            RegisterScreen(self.nav_manager).show(page)
        register_button = ft.TextButton(
            "Register", on_click=go_to_register,
            style=ft.ButtonStyle(color=ft.Colors.BLACK)
        )

        login_view = ft.Column([
            ft.Text("Login", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            username_field,
            password_field,
            ft.Container(content=show_password_checkbox, width=300),
            ft.Row([login_button, register_button], alignment="center", spacing=20),
            login_result
        ], horizontal_alignment="center", alignment=ft.alignment.center, spacing=10)

        page.controls.append(login_view)
        page.update()

    def toggle_password(self, password_field, page):
        password_field.password = not password_field.password
        page.update()
