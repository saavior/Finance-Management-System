#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:23:25 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import update_transaction, get_dashboard_data
import global_vars

class EditTransactionScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page, account_id, account_name):
        page.controls.clear()
        # Direct import of get_dashboard_data from backend
        data = get_dashboard_data(global_vars.current_user_id)
        transactions = data.get("transactions", [])
        account_transactions = [txn for txn in transactions if txn.get("account_id") == account_id]
        options = [ft.dropdown.Option(txn.get("description", "N/A")) for txn in account_transactions]
        txn_dropdown = ft.Dropdown(
            label="Select Transaction to Edit", width=300,
            options=options,
            value=options[0].text if options else None
        )
        new_description_field = ft.TextField(label="New Description", width=300)
        new_amount_field = ft.TextField(label="New Amount", width=300)
        new_date_field = ft.TextField(label="New Date (YYYY-MM-DD)", width=300)
        new_currency_dropdown = ft.Dropdown(
            label="New Currency", width=300,
            options=[
                ft.dropdown.Option("USD"),
                ft.dropdown.Option("EUR"),
                ft.dropdown.Option("GBP"),
                ft.dropdown.Option("JPY")
            ],
            value="USD"
        )
        new_txn_type_dropdown = ft.Dropdown(
            label="New Transaction Type", width=300,
            options=[
                ft.dropdown.Option("Credit"),
                ft.dropdown.Option("Debit")
            ],
            value="Credit"
        )
        new_category_dropdown = ft.Dropdown(
            label="New Category", width=300,
            options=[
                ft.dropdown.Option("Salary"),
                ft.dropdown.Option("Shopping"),
                ft.dropdown.Option("Bills"),
                ft.dropdown.Option("Other")
            ],
            value="Other"
        )
        edit_txn_result = ft.Text("", color=ft.Colors.BLACK, size=16, text_align=ft.TextAlign.CENTER)

        def on_edit_txn(e):
            selected_description = txn_dropdown.value
            selected_txn = None
            for txn in account_transactions:
                if txn.get("description", "N/A") == selected_description:
                    selected_txn = txn
                    break
            if not selected_txn:
                edit_txn_result.value = "Error: No transaction selected."
                page.update()
                return
            try:
                new_amount = float(new_amount_field.value)
            except ValueError:
                edit_txn_result.value = "Error: Amount must be numeric."
                page.update()
                return
            if new_txn_type_dropdown.value.lower() == "debit":
                new_amount = -abs(new_amount)
            else:
                new_amount = abs(new_amount)
            new_category = new_category_dropdown.value if new_category_dropdown.value else ""
            result = update_transaction(
                transaction_id=selected_txn["transaction_id"],
                new_amount=new_amount,
                new_date=new_date_field.value,
                new_description=new_description_field.value,
                new_currency=new_currency_dropdown.value if new_currency_dropdown.value else "USD",
                new_transaction_type=new_txn_type_dropdown.value if new_txn_type_dropdown.value else "Credit",
                new_category=new_category
            )
            edit_txn_result.value = result
            page.update()
            if result.lower().startswith("transaction updated"):
                from screens.account_viewer import AccountViewerScreen
                AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, "Updated")

        edit_txn_btn = ft.ElevatedButton("Update Transaction", on_click=on_edit_txn,
                                         bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        def on_cancel(e):
            from screens.account_viewer import AccountViewerScreen
            AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, "Updated")
        cancel_txn_btn = ft.ElevatedButton("Cancel", on_click=on_cancel,
                                           bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)

        edit_txn_view = ft.Column([
            ft.Text("Edit Transaction", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            txn_dropdown,
            new_description_field,
            new_amount_field,
            new_date_field,
            new_currency_dropdown,
            new_txn_type_dropdown,
            new_category_dropdown,
            ft.Row([edit_txn_btn, cancel_txn_btn], alignment="center", spacing=20),
            edit_txn_result
        ], spacing=20, horizontal_alignment="center")
        
        page.controls.append(edit_txn_view)
        page.update()
