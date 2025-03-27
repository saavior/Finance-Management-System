#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:23:55 2025

@author: davidsalvadormediavilla
"""
import flet as ft
import base64
import pandas as pd
import plotly.express as px
from datetime import datetime
from backend import get_dashboard_data
import global_vars

class TransactionVisualizationsScreen:
    def __init__(self, nav_manager):
        self.nav_manager = nav_manager

    def show(self, page: ft.Page, account_id, account_name):
        page.controls.clear()
        data = get_dashboard_data(global_vars.current_user_id)
        transactions = data.get("transactions", [])
        account_transactions = [txn for txn in transactions if txn.get("account_id") == account_id]
        
        account_info = None
        for acc in data.get("accounts", []):
            if acc.get("account_id") == account_id:
                account_info = acc
                break
        if not account_info:
            ft.AlertDialog(title=ft.Text("Account not found"))
            return
        
        current_balance = float(account_info.get("balance", 0))
        df_txn = pd.DataFrame(account_transactions)
        if not df_txn.empty:
            df_txn['amount'] = pd.to_numeric(df_txn['amount'], errors='coerce').fillna(0.0)
            total_txn = df_txn['amount'].sum()
        else:
            total_txn = 0.0
        
        original_balance = current_balance - total_txn
        
        if df_txn.empty:
            info = ft.Text("No transactions available for visualization.", color=ft.Colors.BLACK)
            def on_back(e):
                from screens.account_viewer import AccountViewerScreen
                AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, "Updated")
            back_btn = ft.ElevatedButton("Back", on_click=on_back,
                                         bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
            layout = ft.Column([info, back_btn], horizontal_alignment="center", spacing=20)
            page.controls.append(layout)
            page.update()
            return
        
        df_txn['transaction_date'] = pd.to_datetime(df_txn['transaction_date'], errors='coerce')
        df_txn = df_txn.sort_values('transaction_date')
        running_balance = original_balance
        balance_list = []
        for amt in df_txn['amount']:
            running_balance += amt
            balance_list.append(running_balance)
        df_txn['running_balance'] = balance_list
        
        fig = px.line(
            df_txn,
            x='transaction_date',
            y='running_balance',
            markers=True,
            title="Total Balance Over Time",
            labels={"transaction_date": "Time", "running_balance": "Total Balance"}
        )
        
        png_bytes = fig.to_image(format="png", engine="kaleido")
        b64_str = base64.b64encode(png_bytes).decode("utf-8")
        chart_img = ft.Image(src_base64=b64_str, width=800, height=400, fit=ft.ImageFit.CONTAIN)
        
        def on_back(e):
            from screens.account_viewer import AccountViewerScreen
            AccountViewerScreen(self.nav_manager).show(page, account_id, account_name, "Updated")
        back_btn = ft.ElevatedButton("Back", on_click=on_back,
                                     bgcolor=ft.Colors.BLACK, color=ft.Colors.WHITE)
        
        layout = ft.Column([
            ft.Text("Total Balance Over Time", size=32, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER),
            chart_img,
            back_btn
        ], horizontal_alignment="center", spacing=20)
        
        page.controls.append(layout)
        page.update()
