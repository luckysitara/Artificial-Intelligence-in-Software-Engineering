#!/usr/bin/env python3
"""Procedural user management using raw SQL through a mysql.connector cursor.

This is the starting point of the task. Every operation is a hand-written SQL
string executed through a cursor whose connection, transaction and error
handling are the caller's responsibility.
"""

import mysql.connector
from mysql.connector import Error


def get_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="example_db"
    )


def create_user(db_cursor, username, email):
    """Create a new user safely using parameterized queries."""
    if not username or not email:
        print("Username and email are required.")
        return
    sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
    try:
        db_cursor.execute(sql, (username, email))
        print(f"User '{username}' created successfully.")
    except Error as e:
        print(f"Error creating user: {e}")


def get_user_by_username(db_cursor, username):
    """Fetch a single user by username."""
    sql = "SELECT id, username, email FROM users WHERE username = %s"
    try:
        db_cursor.execute(sql, (username,))
        return db_cursor.fetchone()
    except Error as e:
        print(f"Error fetching user: {e}")
        return None


def update_user_email(db_cursor, username, new_email):
    """Update the email of an existing user."""
    sql = "UPDATE users SET email = %s WHERE username = %s"
    try:
        db_cursor.execute(sql, (new_email, username))
        print(f"User '{username}' updated successfully.")
    except Error as e:
        print(f"Error updating user: {e}")


def delete_user(db_cursor, username):
    """Delete a user by username."""
    sql = "DELETE FROM users WHERE username = %s"
    try:
        db_cursor.execute(sql, (username,))
        print(f"User '{username}' deleted successfully.")
    except Error as e:
        print(f"Error deleting user: {e}")


def list_users(db_cursor):
    """Return every user in the table."""
    sql = "SELECT id, username, email FROM users"
    try:
        db_cursor.execute(sql)
        return db_cursor.fetchall()
    except Error as e:
        print(f"Error listing users: {e}")
        return []


if __name__ == "__main__":
    # The caller owns the connection, the commits and the cleanup.
    connection = get_connection()
    cursor = connection.cursor()

    create_user(cursor, "alice", "alice@example.com")
    connection.commit()

    print(get_user_by_username(cursor, "alice"))

    update_user_email(cursor, "alice", "alice@new-domain.com")
    connection.commit()

    print(list_users(cursor))

    delete_user(cursor, "alice")
    connection.commit()

    cursor.close()
    connection.close()
