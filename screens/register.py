#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:19:52 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import register_user
# Removed: from screens.login import LoginScreen

class RegisterScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page):
        page.controls.clear()

        reg_username_field = ft.TextField(label="Username", width=300)
        reg_password_field = ft.TextField(label="Password", password=True, width=300)
        reg_confirm_password_field = ft.TextField(label="Confirm Password", password=True, width=300)
        register_result = ft.Text(color=ft.Colors.RED, size=16, text_align=ft.TextAlign.CENTER)
        show_password_checkbox = ft.Checkbox(
            label="Show Password",
            value=False,
            on_change=lambda e: self.toggle_password(reg_password_field, reg_confirm_password_field, page)
        )

        def on_register(e):
            if reg_password_field.value != reg_confirm_password_field.value:
                register_result.value = "Passwords don't match"
                page.update()
                return

            result = register_user(reg_username_field.value, reg_password_field.value)
            register_result.value = result
            page.update()

            if result == "User registered successfully!":
                # Local import of LoginScreen to break the circular dependency
                from screens.login import LoginScreen
                LoginScreen(self.nav_manager).show(page)

        register_btn = ft.ElevatedButton(
            "Register", on_click=on_register,
            bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE
        )

        def go_back(e):
            from screens.login import LoginScreen  # local import here
            LoginScreen(self.nav_manager).show(page)

        back_btn = ft.TextButton(
            "Back to Login", on_click=go_back,
            style=ft.ButtonStyle(color=ft.Colors.BLACK)
        )

        register_view = ft.Column([
            ft.Text("Register", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            reg_username_field,
            reg_password_field,
            reg_confirm_password_field,
            ft.Container(content=show_password_checkbox, width=300),
            ft.Row([register_btn, back_btn], alignment="center", spacing=20),
            register_result
        ], horizontal_alignment="center", alignment=ft.alignment.center, spacing=10)

        page.controls.append(register_view)
        page.update()

    def toggle_password(self, password_field, confirm_field, page):
        password_field.password = not password_field.password
        confirm_field.password = not confirm_field.password
        page.update()
