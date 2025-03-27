#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 13 11:15:20 2025

@author: davidsalvadormediavilla
"""
import mysql.connector
from mysql.connector import pooling
from hashlib import sha256
from decimal import Decimal
from datetime import datetime
import time

# Database configuration for the local MySQL server hosted via XAMPP.
dbconfig = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "finance_db"
}

# Create a connection pool with a fixed pool size (5 connections) to improve performance.
pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **dbconfig)

def connect_to_database():
    # Retrieve a connection from the pool.
    return pool.get_connection()

def hash_password(password):
    # Hash the password using SHA256.
    return sha256(password.encode()).hexdigest()

def login_user(username, password):
    # Connect to the database.
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Execute a parameterized query to fetch the user.
        cursor.execute('SELECT user_id, password FROM User WHERE username = %s', (username,))
        user = cursor.fetchone()
        if not user:
            return "Error: Username not found."
        user_id, stored_hashed_password = user
        # Compare the provided password (hashed) with the stored hashed password.
        if hash_password(password) == stored_hashed_password:
            return f"Login successful!|{user_id}"
        else:
            return "Error: Invalid password."
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        # Always close the cursor and connection.
        cursor.close()
        conn.close()

def register_user(username, password, role="user"):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Check if the username already exists.
        cursor.execute('SELECT username FROM User WHERE username = %s', (username,))
        if cursor.fetchone():
            return "Error: Username already exists."
        # Hash the password for security.
        hashed_password = hash_password(password)
        # Insert the new user into the User table.
        cursor.execute('INSERT INTO User (username, password, role) VALUES (%s, %s, %s)', 
                       (username, hashed_password, role))
        conn.commit()
        return "User registered successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def create_account(user_id, account_name, initial_balance=0.00, type_of_account="N/A", type_of_currency="N/A"):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Insert a new account record into the Account table.
        cursor.execute('''
            INSERT INTO Account (account_name, user_id, balance, type_of_account, currency)
            VALUES (%s, %s, %s, %s, %s)
        ''', (account_name, user_id, initial_balance, type_of_account, type_of_currency))
        conn.commit()
        return "Account created successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def update_account(account_id, new_name, new_currency):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Retrieve current currency and balance of the account.
        cursor.execute('SELECT currency, balance FROM Account WHERE account_id = %s', (account_id,))
        old_data = cursor.fetchone()
        if not old_data:
            return "Error: Account not found."
        old_currency, old_balance = old_data
        if old_currency != new_currency:
            # Perform currency conversion if necessary.
            old_rate = get_currency_rate_cached(old_currency)
            new_rate = get_currency_rate_cached(new_currency)
            if old_rate is None or new_rate is None:
                return "Error: Could not fetch currency rates."
            balance_in_usd = Decimal(old_balance) / Decimal(old_rate)
            new_balance = balance_in_usd * Decimal(new_rate)
            cursor.execute('''
                UPDATE Account
                SET account_name = %s, currency = %s, balance = %s
                WHERE account_id = %s
            ''', (new_name, new_currency, new_balance, account_id))
        else:
            # Update only the account name if currency remains the same.
            cursor.execute('UPDATE Account SET account_name = %s WHERE account_id = %s', (new_name, account_id))
        conn.commit()
        return "Account updated successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def delete_account(account_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Delete all transactions associated with the account.
        cursor.execute('DELETE FROM `Transaction` WHERE account_id = %s', (account_id,))
        conn.commit()
        # Delete the account itself.
        cursor.execute('DELETE FROM Account WHERE account_id = %s', (account_id,))
        conn.commit()
        return "Account deleted successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def add_transaction(account_id, amount, date, description, currency, transaction_type, category=""):
    start_time = time.perf_counter()  # Start performance timer.
    if amount == 0:
        return "Error: Amount cannot be zero."
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Parse the transaction date.
        txn_date = datetime.strptime(date, "%Y-%m-%d").date()
        # Insert the new transaction.
        cursor.execute('''
            INSERT INTO `Transaction` (account_id, amount, transaction_date, description, currency, transaction_type)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (account_id, amount, txn_date, description, currency, transaction_type))
        transaction_id = cursor.lastrowid  # Retrieve the transaction ID.
        if category.strip():
            # Insert category information if provided.
            cursor.execute('''
                INSERT INTO Category (category_name, transaction_id)
                VALUES (%s, %s)
            ''', (category, transaction_id))
        conn.commit()
        elapsed = time.perf_counter() - start_time  # Calculate operation duration.
        print(f"add_transaction completed in {elapsed:.2f} seconds")
        return "Transaction added successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    except ValueError as ve:
        return f"Error: {ve}"
    finally:
        cursor.close()
        conn.close()

def remove_transaction(transaction_id):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Retrieve transaction details for balance update via triggers.
        cursor.execute('SELECT account_id, amount, currency FROM `Transaction` WHERE transaction_id = %s', (transaction_id,))
        transaction = cursor.fetchone()
        if not transaction:
            return "Error: Transaction not found."
        account_id, amount, currency = transaction
        # Delete related category and transaction records.
        cursor.execute('DELETE FROM Category WHERE transaction_id = %s', (transaction_id,))
        cursor.execute('DELETE FROM `Transaction` WHERE transaction_id = %s', (transaction_id,))
        conn.commit()
        return "Transaction removed successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def update_transaction(transaction_id, new_amount, new_date, new_description, new_currency, new_transaction_type, new_category=""):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Check that the transaction exists.
        cursor.execute('SELECT account_id, amount, currency FROM `Transaction` WHERE transaction_id = %s', (transaction_id,))
        old_txn = cursor.fetchone()
        if not old_txn:
            return "Error: Transaction not found."
        account_id, old_amount, old_currency = old_txn
        # Parse the new transaction date.
        txn_date = datetime.strptime(new_date, "%Y-%m-%d").date()
        # Update the transaction record.
        cursor.execute('''
            UPDATE `Transaction`
            SET amount = %s, transaction_date = %s, description = %s, currency = %s, transaction_type = %s
            WHERE transaction_id = %s
        ''', (new_amount, txn_date, new_description, new_currency, new_transaction_type, transaction_id))
        # Update category information.
        cursor.execute('DELETE FROM Category WHERE transaction_id = %s', (transaction_id,))
        if new_category.strip():
            cursor.execute('''
                INSERT INTO Category (category_name, transaction_id)
                VALUES (%s, %s)
            ''', (new_category, transaction_id))
        conn.commit()
        return "Transaction updated successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    except ValueError as ve:
        return f"Error: {ve}"
    finally:
        cursor.close()
        conn.close()

# Global cache for currency conversion rates.
currency_cache = {}

def get_currency_rate(currency_code):
    # Fetch conversion rate for a currency from the Currency table.
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT conversion_rate FROM Currency WHERE currency_code = %s', (currency_code,))
        row = cursor.fetchone()
        return float(row[0]) if row else None
    except:
        return None
    finally:
        cursor.close()
        conn.close()

def get_currency_rate_cached(currency_code):
    global currency_cache
    now = time.time()  # Current time.
    cache_duration = 600  # Cache duration: 10 minutes.
    if currency_code in currency_cache:
        cached_rate, timestamp = currency_cache[currency_code]
        if now - timestamp < cache_duration:
            return cached_rate
    rate = get_currency_rate(currency_code)
    currency_cache[currency_code] = (rate, now)
    return rate

def update_balance(account_id, amount, currency):
    conn = connect_to_database()
    cursor = conn.cursor()
    try:
        # Retrieve current account balance and currency.
        cursor.execute('SELECT balance, currency FROM Account WHERE account_id = %s', (account_id,))
        row = cursor.fetchone()
        if not row:
            return "Error: Account not found."
        current_balance, account_currency = row
        if currency != account_currency:
            # Perform currency conversion if necessary.
            src_rate = get_currency_rate_cached(currency)
            dest_rate = get_currency_rate_cached(account_currency)
            if src_rate is None or dest_rate is None:
                return "Error: Could not fetch currency rates."
            amount_in_usd = Decimal(amount) / Decimal(src_rate)
            final_amount = amount_in_usd * Decimal(dest_rate)
        else:
            final_amount = Decimal(amount)
        new_balance = Decimal(current_balance) + final_amount
        cursor.execute('UPDATE Account SET balance = %s WHERE account_id = %s', (new_balance, account_id))
        conn.commit()
        return "Balance updated successfully!"
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def get_dashboard_data(user_id):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    try:
        # Retrieve accounts for the user.
        cursor.execute('SELECT account_id, account_name, balance, type_of_account, currency, creation_date, initial_balance FROM Account WHERE user_id = %s', (user_id,))
        accounts = cursor.fetchall()
        # Retrieve transactions for the user, joining with Account table for additional details.
        cursor.execute('''
            SELECT t.transaction_id, t.amount, t.transaction_date, t.description, t.currency, t.transaction_type,
                   (SELECT category_name FROM Category WHERE transaction_id = t.transaction_id) AS category,
                   a.account_id, a.account_name
            FROM `Transaction` t
            JOIN Account a ON t.account_id = a.account_id
            WHERE a.user_id = %s
            ORDER BY t.transaction_date DESC
        ''', (user_id,))
        transactions = cursor.fetchall()
        return {"accounts": accounts, "transactions": transactions}
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()

def filter_transactions(user_id, start_date=None, end_date=None, min_amount=None, max_amount=None, category=None):
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    try:
        query = '''
            SELECT t.transaction_id, t.amount, t.transaction_date, t.description, t.currency, t.transaction_type, a.account_name,
                   (SELECT category_name FROM Category WHERE transaction_id = t.transaction_id) AS category
            FROM `Transaction` t
            JOIN Account a ON t.account_id = a.account_id
            WHERE a.user_id = %s
        '''
        params = [user_id]
        if start_date:
            query += ' AND t.transaction_date >= %s'
            params.append(start_date)
        if end_date:
            query += ' AND t.transaction_date <= %s'
            params.append(end_date)
        if min_amount is not None:
            query += ' AND t.amount >= %s'
            params.append(min_amount)
        if max_amount is not None:
            query += ' AND t.amount <= %s'
            params.append(max_amount)
        if category:
            query += ' AND t.description LIKE %s'
            params.append(f'%{category}%')
        cursor.execute(query, params)
        transactions = cursor.fetchall()
        return transactions
    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        cursor.close()
        conn.close()
