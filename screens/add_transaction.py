#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:22:05 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from datetime import datetime
from backend import add_transaction
# Removed: top-level import of AccountViewerScreen

class AddTransactionScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page, account_id, account_name):
        page.controls.clear()
        
        description_field = ft.TextField(label="Transaction Description", width=300)
        amount_field = ft.TextField(label="Transaction Amount", width=300)
        date_field = ft.TextField(label="Transaction Date (YYYY-MM-DD)", width=300)
        currency_dropdown = ft.Dropdown(
            label="Transaction Currency", width=300,
            options=[
                ft.dropdown.Option("USD"),
                ft.dropdown.Option("EUR"),
                ft.dropdown.Option("GBP"),
                ft.dropdown.Option("JPY")
            ],
            value="USD"
        )
        txn_type_dropdown = ft.Dropdown(
            label="Transaction Type", width=300,
            options=[
                ft.dropdown.Option("Credit"),
                ft.dropdown.Option("Debit")
            ],
            value="Credit"
        )
        category_dropdown = ft.Dropdown(
            label="Category", width=300,
            options=[
                ft.dropdown.Option("Salary"),
                ft.dropdown.Option("Shopping"),
                ft.dropdown.Option("Bills"),
                ft.dropdown.Option("Other")
            ],
            value="Other"
        )
        add_txn_result = ft.Text("", color=ft.Colors.BLACK, size=16, text_align=ft.TextAlign.CENTER)

        def on_add_txn(e):
            print("Add Transaction button clicked")
            if not description_field.value or not amount_field.value or not date_field.value:
                add_txn_result.value = "Error: All fields are required."
                page.update()
                return
            try:
                txn_amount = float(amount_field.value)
            except ValueError:
                add_txn_result.value = "Error: Amount must be numeric."
                page.update()
                return
            try:
                dt = datetime.strptime(date_field.value, "%Y-%m-%d")
                txn_date_str = dt.strftime("%Y-%m-%d")
            except ValueError:
                add_txn_result.value = "Error: Date must be in YYYY-MM-DD format."
                page.update()
                return
            if txn_type_dropdown.value.lower() == "debit":
                txn_amount = -abs(txn_amount)
            else:
                txn_amount = abs(txn_amount)
            txn_currency = currency_dropdown.value if currency_dropdown.value else "USD"
            txn_type = txn_type_dropdown.value if txn_type_dropdown.value else "Credit"
            txn_category = category_dropdown.value if category_dropdown.value else ""
            
            result = add_transaction(
                account_id, txn_amount, txn_date_str, description_field.value,
                txn_currency, txn_type, txn_category
            )
            print("Backend add_transaction result:", result)
            add_txn_result.value = result
            page.update()
            if result.lower().startswith("transaction added"):
                # Local import to avoid circular dependency
                from screens.account_viewer import AccountViewerScreen
                AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, "Updated")

        def on_cancel(e):
            print("Cancel button clicked")
            from screens.account_viewer import AccountViewerScreen
            AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, "Updated")

        add_txn_btn = ft.ElevatedButton("Add Transaction", on_click=on_add_txn,
                                        bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        cancel_txn_btn = ft.ElevatedButton("Cancel", on_click=on_cancel,
                                           bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)

        add_txn_view = ft.Column([
            ft.Text("Add Transaction", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            description_field,
            amount_field,
            date_field,
            currency_dropdown,
            txn_type_dropdown,
            category_dropdown,
            ft.Row([add_txn_btn, cancel_txn_btn], alignment="center", spacing=20),
            add_txn_result
        ], spacing=20, horizontal_alignment="center")
        
        page.controls.append(add_txn_view)
        page.update()
