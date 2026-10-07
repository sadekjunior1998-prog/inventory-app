import sqlite3

from constants import (
    SUCCESS,
    NOT_FOUND,
    ALREADY_EXISTS,
    INSUFFICIENT_STOCK,
    DATABASE_ERROR,
)

DB_NAME = "shop.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


def initialize_database():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY,
            product TEXT UNIQUE,
            quantity INTEGER,
            price FLOAT
        )
    """)

    conn.commit()


def add_product(product, quantity, price):
    try:
        cursor.execute("""
            INSERT INTO products(product, quantity, price)
            VALUES (?, ?, ?)
        """, (product, quantity, price))

        conn.commit()
        return SUCCESS

    except sqlite3.IntegrityError:
        return ALREADY_EXISTS


def search_product(product):
    cursor.execute("""
        SELECT * FROM products
        WHERE product = ?
    """, (product,))

    return cursor.fetchone()


def get_inventory():
    cursor.execute("""
        SELECT * FROM products
    """)

    return cursor.fetchall()


def add_stock(product, quantity):
    cursor.execute("""
        SELECT quantity FROM products
        WHERE product = ?
    """, (product,))

    row = cursor.fetchone()

    if row is None:
        return NOT_FOUND

    new_quantity = row[0] + quantity

    cursor.execute("""
        UPDATE products
        SET quantity = ?
        WHERE product = ?
    """, (new_quantity, product))

    conn.commit()
    return SUCCESS


def remove_stock(product, quantity):
    cursor.execute("""
        SELECT quantity FROM products
        WHERE product = ?
    """, (product,))

    row = cursor.fetchone()

    if row is None:
        return NOT_FOUND

    if row[0] < quantity:
        return INSUFFICIENT_STOCK

    new_quantity = row[0] - quantity

    cursor.execute("""
        UPDATE products
        SET quantity = ?
        WHERE product = ?
    """, (new_quantity, product))

    conn.commit()
    return SUCCESS


def delete_product(product):
    cursor.execute("""
        DELETE FROM products
        WHERE product = ?
    """, (product,))

    if cursor.rowcount == 0:
        return NOT_FOUND

    conn.commit()
    return SUCCESS


def close_database():
    conn.close()