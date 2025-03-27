#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:18:44 2025

@author: davidsalvadormediavilla
"""

# screens/ui_helpers.py
import flet as ft

def build_table_row(cell_texts: list[str], is_header=False) -> ft.Column:

    cells = []
    for idx, text in enumerate(cell_texts):
        cell = ft.Container(
            expand=True,
            content=ft.Text(
                text,
                weight="bold" if is_header else "normal",
                color=ft.Colors.BLACK,
                text_align=ft.TextAlign.CENTER
            )
        )
        cells.append(cell)
        if idx < len(cell_texts) - 1:
            # Add a thin vertical line between cells
            cells.append(
                ft.Container(
                    width=1, 
                    bgcolor=ft.Colors.BLACK, 
                    margin=ft.margin.symmetric(horizontal=5)
                )
            )
    row = ft.Row(cells, vertical_alignment="center")
    return ft.Column(
        [row, ft.Divider(color=ft.Colors.BLACK, thickness=1)],
        spacing=0
    )

def build_transaction_row(cell_texts: list[str], is_header=False) -> ft.Column:
    # For transactions, you can reuse build_table_row if you want a consistent style
    return build_table_row(cell_texts, is_header)











