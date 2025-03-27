#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:21:30 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import delete_account, get_dashboard_data
import global_vars

class RemoveAccountScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page):
        page.controls.clear()
        # Directly import get_dashboard_data from backend:
        data = get_dashboard_data(global_vars.current_user_id)
        accounts_data = data.get("accounts", []) if isinstance(data, dict) else []
        options = [ft.dropdown.Option(acc["account_name"]) for acc in accounts_data]
        account_dropdown = ft.Dropdown(
            label="Select Account to Remove", width=300,
            options=options,
            value=options[0].text if options else None
        )
        remove_result = ft.Text("", color=ft.Colors.BLACK, size=16, text_align=ft.TextAlign.CENTER)

        def on_remove_account(e):
            selected_account = None
            for acc in accounts_data:
                if acc["account_name"] == account_dropdown.value:
                    selected_account = acc
                    break
            if not selected_account:
                remove_result.value = "Error: No account selected."
                page.update()
                return
            self.show_remove_account_confirmation(page, selected_account["account_id"],
                                                  selected_account["account_name"])

        remove_btn = ft.ElevatedButton("Remove Account", on_click=on_remove_account,
                                       bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        def on_cancel(e):
            from screens.dashboard import DashboardScreen  # Local import
            DashboardScreen(self.nav_manager).show(page)
        cancel_btn = ft.ElevatedButton("Cancel", on_click=on_cancel,
                                       bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)

        remove_account_view = ft.Column([
            ft.Text("Remove Account", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            account_dropdown,
            ft.Row([remove_btn, cancel_btn], alignment="center", spacing=20),
            remove_result
        ], spacing=20, horizontal_alignment="center")
        
        page.controls.append(remove_account_view)
        page.update()

    def show_remove_account_confirmation(self, page: ft.Page, account_id, account_name):
        page.controls.clear()
        def confirm_yes(e):
            result = delete_account(account_id)
            print("Delete account result:", result)
            from screens.dashboard import DashboardScreen  # Local import
            DashboardScreen(self.nav_manager).show(page)
        def confirm_no(e):
            self.show(page)
        confirm_view = ft.Column([
            ft.Text(f"Are you sure you want to remove account '{account_name}'?",
                    size=24, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            ft.Row([
                ft.ElevatedButton("Yes", on_click=confirm_yes, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE),
                ft.ElevatedButton("No", on_click=confirm_no, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
            ], alignment="center", spacing=20)
        ], horizontal_alignment="center", spacing=20)
        page.controls.append(confirm_view)
        page.update()
