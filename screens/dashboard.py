#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:20:09 2025

@author: davidsalvadormediavilla
"""

import flet as ft
from backend import get_dashboard_data
from data_structures import LinkedList
from screens.ui_helpers import build_table_row  # for building table rows
import global_vars

class DashboardScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page):
        page.controls.clear()

        # Fetch all account data
        data = get_dashboard_data(global_vars.current_user_id)
        accounts_data = data.get("accounts", []) if isinstance(data, dict) else []

        try:
            total_balance_value = sum([float(acc["balance"]) for acc in accounts_data])
        except Exception:
            total_balance_value = 0.0

        currency_signs = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥"}
        sign = currency_signs.get(accounts_data[0].get("currency", "USD"), "$") if accounts_data else "$"
        total_balance = f"{sign}{total_balance_value:,.2f}"

        welcome_text = ft.Text(
            f"Welcome: {global_vars.current_username}",
            size=16, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER
        )
        title_section = ft.Column([
            ft.Text("Main Dashboard", size=28, weight="bold", color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            ft.Text("Financial Management", size=18, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            ft.Text("Version 1.0.0", size=14, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment="center", spacing=2)

        total_balance_label = ft.Text(
            f"Total Balance: {total_balance}",
            color=ft.Colors.BLACK, size=16, text_align=ft.TextAlign.CENTER
        )

        # --- Filtering Controls for Accounts ---
        account_search_field = ft.TextField(label="Search accounts...", width=200)
        min_balance_field = ft.TextField(label="Min Balance", width=100)
        max_balance_field = ft.TextField(label="Max Balance", width=100)
        currency_dropdown = ft.Dropdown(
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

        def filter_accounts(e=None):
            keyword = account_search_field.value.lower().strip() if account_search_field.value else ""
            try:
                min_bal = float(min_balance_field.value) if min_balance_field.value else None
            except ValueError:
                min_bal = None
            try:
                max_bal = float(max_balance_field.value) if max_balance_field.value else None
            except ValueError:
                max_bal = None
            selected_currency = currency_dropdown.value

            filtered = []
            for acc in accounts_data:
                # Check if the keyword appears in the account name or type
                name_ok = True
                if keyword:
                    name_ok = (keyword in acc.get("account_name", "").lower() or
                               keyword in acc.get("type_of_account", "").lower())
                try:
                    balance = float(acc.get("balance", 0))
                except:
                    balance = 0
                balance_ok = True
                if min_bal is not None and balance < min_bal:
                    balance_ok = False
                if max_bal is not None and balance > max_bal:
                    balance_ok = False
                currency_ok = (selected_currency == "Any" or acc.get("currency", "") == selected_currency)
                if name_ok and balance_ok and currency_ok:
                    filtered.append(acc)

            def build_account_rows_from_list(acc_list):
                rows = []
                for acc in acc_list:
                    view_button = ft.ElevatedButton(
                        text="View",
                        on_click=lambda e, a=acc: __import__("screens.account_viewer").account_viewer.AccountViewerScreen(self.nav_manager).show(page, a["account_id"], a["account_name"], a["balance"]),
                        bgcolor=ft.Colors.BLACK,
                        color=ft.Colors.WHITE
                    )
                    row_cells = [
                        acc.get("account_name", "N/A"),
                        str(acc.get("balance", "0")),
                        acc.get("type_of_account", "N/A"),
                        acc.get("currency", "N/A")
                    ]
                    row_comp = build_table_row(row_cells)
                    # Append the view button to the row
                    row_comp.controls[0].controls.append(
                        ft.Container(width=1, bgcolor=ft.Colors.BLACK, margin=ft.margin.symmetric(horizontal=5))
                    )
                    row_comp.controls[0].controls.append(
                        ft.Container(content=view_button, expand=True, alignment=ft.alignment.center)
                    )
                    rows.append(row_comp)
                return rows

            accounts_table_body.controls = build_account_rows_from_list(filtered)
            page.update()

        account_search_field.on_change = filter_accounts
        min_balance_field.on_change = filter_accounts
        max_balance_field.on_change = filter_accounts
        currency_dropdown.on_change = filter_accounts

        filter_row = ft.Row(
            [account_search_field, min_balance_field, max_balance_field, currency_dropdown],
            alignment="center", spacing=10
        )

        # --- Build the Accounts Table ---
        accounts_list = LinkedList()
        for acc in accounts_data:
            accounts_list.append(acc)

        table_header = build_table_row(["Account Name", "Account Balance", "Type of Account", "Currency", "Action"], is_header=True)

        def build_account_rows(linked_list):
            rows = []
            for acc in linked_list.to_list():
                view_button = ft.ElevatedButton(
                    text="View",
                    on_click=lambda e, a=acc: __import__("screens.account_viewer").account_viewer.AccountViewerScreen(self.nav_manager).show(page, a["account_id"], a["account_name"], a["balance"]),
                    bgcolor=ft.Colors.BLACK,
                    color=ft.Colors.WHITE
                )
                row_cells = [
                    acc.get("account_name", "N/A"),
                    str(acc.get("balance", "0")),
                    acc.get("type_of_account", "N/A"),
                    acc.get("currency", "N/A")
                ]
                row_comp = build_table_row(row_cells)
                row_comp.controls[0].controls.append(
                    ft.Container(width=1, bgcolor=ft.Colors.BLACK, margin=ft.margin.symmetric(horizontal=5))
                )
                row_comp.controls[0].controls.append(
                    ft.Container(content=view_button, expand=True, alignment=ft.alignment.center)
                )
                rows.append(row_comp)
            return rows

        accounts_table_body = ft.Column(build_account_rows(accounts_list), spacing=0)
        table_container = ft.Container(
            content=ft.Column([table_header, accounts_table_body], spacing=0),
            border=ft.border.all(1, ft.Colors.BLACK),
            border_radius=5,
            padding=10,
            margin=ft.margin.all(10),
            expand=True,
            alignment=ft.alignment.center
        )

        # --- Navigation Buttons ---
        def on_add_account(e):
            from screens.add_account import AddAccountScreen
            AddAccountScreen(self.nav_manager).show(page)
        def on_remove_account(e):
            from screens.remove_account import RemoveAccountScreen
            RemoveAccountScreen(self.nav_manager).show(page)
        def on_logout(e):
            from screens.logout import LogoutScreen
            LogoutScreen(self.nav_manager).show(page)
        add_account_button = ft.ElevatedButton("Add Account", on_click=on_add_account, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        remove_account_button = ft.ElevatedButton("Remove Account", on_click=on_remove_account, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        logout_button = ft.ElevatedButton("Logout", on_click=on_logout, bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        buttons_row = ft.Row([add_account_button, remove_account_button, logout_button], alignment="center", spacing=20)

        dashboard_view = ft.Column([
            title_section,
            welcome_text,
            total_balance_label,
            filter_row,
            table_container,
            buttons_row
        ], spacing=20, horizontal_alignment="center", expand=True)

        page.controls.append(dashboard_view)
        page.update()
