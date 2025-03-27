#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:17:57 2025

@author: davidsalvadormediavilla
"""

# screens/__init__.py
# Do not include LoginScreen here.
from .register import RegisterScreen

from .account_viewer import AccountViewerScreen
from .add_account import AddAccountScreen
from .remove_account import RemoveAccountScreen
from .add_transaction import AddTransactionScreen
from .remove_transaction import RemoveTransactionScreen
from .edit_account import EditAccountScreen
from .edit_transaction import EditTransactionScreen
from .transaction_visualizations import TransactionVisualizationsScreen
from .logout import LogoutScreen


# If you have a data structures demo file, you can import it here too.
# from .data_structures_demo import DataStructuresDemoScreen

