#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:20:41 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import get_dashboard_data
from data_structures import Queue
from screens.ui_helpers import build_transaction_row
import global_vars

class AccountViewerScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page, account_id, account_name, dummy_balance):
        page.controls.clear()
        data = get_dashboard_data(global_vars.current_user_id)
        accounts = data.get("accounts", [])
        updated_balance = "0"
        for acc in accounts:
            if acc["account_id"] == account_id:
                updated_balance = acc.get("balance", "0")
                break

        transactions = data.get("transactions", [])
        account_transactions = [txn for txn in transactions if txn.get("account_id") == account_id]

        # --- Filtering Controls for Transactions ---
        txn_search_field = ft.TextField(label="Search transactions...", width=200)
        min_txn_field = ft.TextField(label="Min Amount", width=100)
        max_txn_field = ft.TextField(label="Max Amount", width=100)
        txn_type_dropdown = ft.Dropdown(
            label="Type", width=120,
            options=[
                ft.dropdown.Option("Any"),
                ft.dropdown.Option("Credit"),
                ft.dropdown.Option("Debit")
            ],
            value="Any"
        )
        txn_currency_dropdown = ft.Dropdown(
            label="Currency", width=120,
            options=[
                ft.dropdown.Option("Any"),
                ft.dropdown.Option("USD"),
                ft.dropdown.Option("EUR"),
                ft.dropdown.Option("GBP"),
                ft.dropdown.Option("JPY")
            ],
            value="Any"
        )

        def filter_transactions(e=None):
            keyword = txn_search_field.value.lower().strip() if txn_search_field.value else ""
            try:
                min_amt = float(min_txn_field.value) if min_txn_field.value else None
            except ValueError:
                min_amt = None
            try:
                max_amt = float(max_txn_field.value) if max_txn_field.value else None
            except ValueError:
                max_amt = None
            selected_type = txn_type_dropdown.value
            selected_currency = txn_currency_dropdown.value

            filtered_txns = []
            for txn in account_transactions:
                desc_ok = True
                if keyword:
                    desc_ok = keyword in txn.get("description", "").lower()
                try:
                    amt = float(txn.get("amount", 0))
                except:
                    amt = 0
                amt_ok = True
                if min_amt is not None and amt < min_amt:
                    amt_ok = False
                if max_amt is not None and amt > max_amt:
                    amt_ok = False
                type_ok = (selected_type == "Any" or txn.get("transaction_type", "").lower() == selected_type.lower())
                currency_ok = (selected_currency == "Any" or txn.get("currency", "") == selected_currency)
                if desc_ok and amt_ok and type_ok and currency_ok:
                    filtered_txns.append(txn)

            def build_txn_rows_from_list(txn_list):
                rows = []
                for txn in txn_list:
                    row_cells = [
                        txn.get("description", "N/A"),
                        str(txn.get("amount", 0)),
                        txn.get("transaction_type", "N/A"),
                        str(txn.get("transaction_date", "N/A")),
                        txn.get("currency", "N/A"),
                        txn.get("category", "N/A")
                    ]
                    row_comp = build_transaction_row(row_cells)
                    rows.append(row_comp)
                return rows

            txn_table_body.controls = build_txn_rows_from_list(filtered_txns)
            page.update()

        txn_search_field.on_change = filter_transactions
        min_txn_field.on_change = filter_transactions
        max_txn_field.on_change = filter_transactions
        txn_type_dropdown.on_change = filter_transactions
        txn_currency_dropdown.on_change = filter_transactions

        txn_filter_row = ft.Row(
            [txn_search_field, min_txn_field, max_txn_field, txn_type_dropdown, txn_currency_dropdown],
            alignment="center", spacing=10
        )

        # --- Build the Transactions Table ---
        from screens.ui_helpers import build_transaction_row
        table_header = build_transaction_row(
            ["Description", "Amount", "Type", "Date", "Currency", "Category"],
            is_header=True
        )
        txn_table_body = ft.Column([], spacing=0)

        def build_txn_rows(queue):
            rows = []
            items = []
            while not queue.is_empty():
                item = queue.dequeue()
                items.append(item)
            for item in items:
                queue.enqueue(item)
                row_cells = [
                    item.get("description", "N/A"),
                    str(item.get("amount", 0)),
                    item.get("transaction_type", "N/A"),
                    str(item.get("transaction_date", "N/A")),
                    item.get("currency", "N/A"),
                    item.get("category", "N/A")
                ]
                row_comp = build_transaction_row(row_cells)
                rows.append(row_comp)
            return rows

        txn_queue = Queue()
        for txn in account_transactions:
            txn_queue.enqueue(txn)
        txn_table_body.controls = build_txn_rows(txn_queue)

        transaction_table = ft.Container(
            content=ft.Column([table_header, txn_table_body], spacing=0),
            border=ft.border.all(1, ft.Colors.BLACK),
            border_radius=5,
            padding=10,
            margin=ft.margin.all(10),
            expand=True,
            alignment=ft.alignment.center
        )

        # --- Action Buttons ---
        def on_add_transaction(e):
            from screens.add_transaction import AddTransactionScreen
            AddTransactionScreen(self.nav_manager).show(page, account_id, account_name)
        def on_remove_transaction(e):
            from screens.remove_transaction import RemoveTransactionScreen
            RemoveTransactionScreen(self.nav_manager).show(page, account_id, account_name)
        def on_edit_account(e):
            from screens.edit_account import EditAccountScreen
            EditAccountScreen(self.nav_manager).show(page, account_id, account_name, updated_balance)
        def on_edit_transaction(e):
            from screens.edit_transaction import EditTransactionScreen
            EditTransactionScreen(self.nav_manager).show(page, account_id, account_name)
        def on_visualize(e):
            from screens.transaction_visualizations import TransactionVisualizationsScreen
            TransactionVisualizationsScreen(self.nav_manager).show(page, account_id, account_name)
        def on_return_dashboard(e):
            from screens.dashboard import DashboardScreen
            DashboardScreen(self.nav_manager).show(page)

        return_dashboard_button = ft.ElevatedButton("Return to Dashboard", on_click=on_return_dashboard,
                                                    bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)

        actions_row = ft.Row([
            ft.ElevatedButton("Add Transaction", on_click=on_add_transaction, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE),
            ft.ElevatedButton("Remove Transaction", on_click=on_remove_transaction, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE),
            ft.ElevatedButton("Edit Account", on_click=on_edit_account, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE),
            ft.ElevatedButton("Edit Transaction", on_click=on_edit_transaction, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE),
            ft.ElevatedButton("Visualize", on_click=on_visualize, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE),
            return_dashboard_button
        ], alignment="center", spacing=20)

        account_viewer_layout = ft.Column([
            ft.Text("Account Viewer", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            ft.Text(f"Account Name: {account_name}", color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            ft.Text(f"Total Balance: {updated_balance}", color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            txn_filter_row,
            transaction_table,
            actions_row
        ], spacing=20, horizontal_alignment="center")

        page.controls.append(account_viewer_layout)
        page.update()
