#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:22:27 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import remove_transaction, get_dashboard_data
from screens.account_viewer import AccountViewerScreen
import global_vars

class RemoveTransactionScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page, account_id, account_name):
        page.controls.clear()
        # Directly import get_dashboard_data from backend
        data = get_dashboard_data(global_vars.current_user_id)
        transactions = data.get("transactions", [])
        account_transactions = [txn for txn in transactions if txn.get("account_id") == account_id]
        options = [ft.dropdown.Option(txn.get("description", "N/A")) for txn in account_transactions]
        txn_dropdown = ft.Dropdown(
            label="Select Transaction to Remove", width=300,
            options=options,
            value=options[0].text if options else None
        )
        remove_txn_result = ft.Text("", color=ft.Colors.BLACK, size=16, text_align=ft.TextAlign.CENTER)

        def on_remove_txn(e):
            selected_txn = None
            for t in account_transactions:
                if t.get("description", "N/A") == txn_dropdown.value:
                    selected_txn = t
                    break
            if not selected_txn:
                remove_txn_result.value = "Error: No transaction selected."
                page.update()
                return
            self.show_remove_transaction_confirmation(page, selected_txn["transaction_id"], account_id, account_name)

        remove_txn_btn = ft.ElevatedButton("Remove Transaction", on_click=on_remove_txn,
                                           bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        def on_cancel(e):
            AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, "Updated")
        cancel_txn_btn = ft.ElevatedButton("Cancel", on_click=on_cancel,
                                           bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)

        remove_txn_view = ft.Column([
            ft.Text("Remove Transaction", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            txn_dropdown,
            ft.Row([remove_txn_btn, cancel_txn_btn], alignment="center", spacing=20),
            remove_txn_result
        ], spacing=20, horizontal_alignment="center")
        
        page.controls.append(remove_txn_view)
        page.update()

    def show_remove_transaction_confirmation(self, page: ft.Page, transaction_id, account_id, account_name):
        page.controls.clear()
        def confirm_yes(e):
            result = remove_transaction(transaction_id)
            print("Remove transaction result:", result)
            from screens.account_viewer import AccountViewerScreen  # Local import
            AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, "Updated")
        def confirm_no(e):
            self.show(page, account_id, account_name)
        confirm_view = ft.Column([
            ft.Text("Are you sure you want to remove the transaction?", size=24, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            ft.Row([
                ft.ElevatedButton("Yes", on_click=confirm_yes, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE),
                ft.ElevatedButton("No", on_click=confirm_no, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
            ], alignment="center", spacing=20)
        ], horizontal_alignment="center", spacing=20)
        page.controls.append(confirm_view)
        page.update()
