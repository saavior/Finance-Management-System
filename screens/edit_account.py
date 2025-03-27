#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:23:09 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import update_account

class EditAccountScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page, account_id, account_name, balance):
        page.controls.clear()
        name_field = ft.TextField(label="New Account Name", width=300, value=account_name)
        currency_dropdown = ft.Dropdown(
            label="New Currency", width=300,
            options=[
                ft.dropdown.Option("USD"),
                ft.dropdown.Option("EUR"),
                ft.dropdown.Option("GBP"),
                ft.dropdown.Option("JPY")
            ],
            value="USD"
        )
        edit_result = ft.Text("", color=ft.Colors.BLACK, size=16, text_align=ft.TextAlign.CENTER)

        def on_edit_account(e):
            new_name = name_field.value
            new_currency = currency_dropdown.value if currency_dropdown.value else "USD"
            result = update_account(account_id, new_name, new_currency)
            edit_result.value = result
            page.update()
            if "successfully" in result.lower():
                from screens.account_viewer import AccountViewerScreen
                AccountViewerScreen(self.nav_manager).show(page, account_id, new_name, balance)

        edit_btn = ft.ElevatedButton("Update Account", on_click=on_edit_account,
                                     bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        def on_cancel(e):
            from screens.account_viewer import AccountViewerScreen
            AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, balance)
        cancel_btn = ft.ElevatedButton("Cancel", on_click=on_cancel,
                                       bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)

        edit_account_view = ft.Column([
            ft.Text("Edit Account", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            name_field,
            currency_dropdown,
            ft.Row([edit_btn, cancel_btn], alignment="center", spacing=20),
            edit_result
        ], spacing=20, horizontal_alignment="center")
        
        page.controls.append(edit_account_view)
        page.update()
