#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:21:15 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import create_account
import global_vars

class AddAccountScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page):
        page.controls.clear()
        account_name_field = ft.TextField(label="Account Name", width=300)
        balance_field = ft.TextField(label="Initial Balance", width=300)
        type_of_account_field = ft.TextField(label="Type of Account", width=300)
        type_of_currency_field = ft.Dropdown(
            label="Type of Currency", width=300,
            options=[
                ft.dropdown.Option("USD"),
                ft.dropdown.Option("EUR"),
                ft.dropdown.Option("GBP"),
                ft.dropdown.Option("JPY")
            ],
            value="USD"
        )
        add_result = ft.Text("", color=ft.Colors.BLACK, size=16, text_align=ft.TextAlign.CENTER)

        def on_add(e):
            if not account_name_field.value:
                add_result.value = "Error: Please enter an account name."
                page.update()
                return
            if not balance_field.value:
                add_result.value = "Error: Please enter an initial balance."
                page.update()
                return
            try:
                initial_balance = float(balance_field.value)
            except ValueError:
                add_result.value = "Error: Balance must be numeric."
                page.update()
                return

            type_of_account = type_of_account_field.value if type_of_account_field.value else "N/A"
            type_of_currency = type_of_currency_field.value if type_of_currency_field.value else "N/A"

            result = create_account(global_vars.current_user_id, account_name_field.value,
                                    initial_balance, type_of_account, type_of_currency)
            add_result.value = result
            page.update()
            if "successfully" in result.lower():
                # Local import to avoid circular dependency
                from screens.dashboard import DashboardScreen
                DashboardScreen(self.nav_manager).show(page)

        add_btn = ft.ElevatedButton("Add Account", on_click=on_add,
                                    bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        def on_cancel(e):
            from screens.dashboard import DashboardScreen
            DashboardScreen(self.nav_manager).show(page)
        cancel_btn = ft.ElevatedButton("Cancel", on_click=on_cancel,
                                       bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)

        add_account_view = ft.Column([
            ft.Text("Add Account", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            account_name_field,
            balance_field,
            type_of_account_field,
            type_of_currency_field,
            ft.Row([add_btn, cancel_btn], alignment="center", spacing=20),
            add_result
        ], spacing=20, horizontal_alignment="center")
        
        page.controls.append(add_account_view)
        page.update()
