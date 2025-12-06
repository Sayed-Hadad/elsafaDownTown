#!/usr/bin/env python3
"""
Simple SQLite migration helper for the Elsafa (Safa) project.

This script will add the following columns if they are missing:
- bookings.addons (TEXT)
- halls.addons (TEXT)
- halls.receipt_number (TEXT)

Run from the project root or call directly. It will not modify existing data.
"""
import os
import sqlite3
import sys


def get_db_path(cli_path=None):
    if cli_path:
        return os.path.abspath(cli_path)
    # script located in scripts/ relative to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.normpath(os.path.join(script_dir, '..'))
    db_path = os.path.join(project_root, 'elsafa_halls.db')
    return db_path


def table_has_column(conn, table, column):
    cur = conn.execute(f"PRAGMA table_info('{table}')")
    cols = [r[1] for r in cur.fetchall()]
    return column in cols


def add_column(conn, table, column_def):
    sql = f"ALTER TABLE {table} ADD COLUMN {column_def};"
    print(f"Executing: {sql}")
    conn.execute(sql)


def main():
    cli_db = os.environ.get('ELS_DB_PATH')
    db = get_db_path(cli_db)
    if not os.path.exists(db):
        print(f"Database not found at: {db}")
        print("Make sure you are running this script from the project that contains `elsafa_halls.db`.")
        sys.exit(1)

    conn = sqlite3.connect(db)
    try:
        # bookings.addons
        if not table_has_column(conn, 'bookings', 'addons'):
            add_column(conn, 'bookings', "addons TEXT")
            print("Added column bookings.addons")
        else:
            print("Column bookings.addons already exists")

        # halls.addons
        if not table_has_column(conn, 'halls', 'addons'):
            add_column(conn, 'halls', "addons TEXT")
            print("Added column halls.addons")
        else:
            print("Column halls.addons already exists")

        # halls.receipt_number
        if not table_has_column(conn, 'halls', 'receipt_number'):
            add_column(conn, 'halls', "receipt_number TEXT")
            print("Added column halls.receipt_number")
        else:
            print("Column halls.receipt_number already exists")

        conn.commit()
        print("Migration complete.")
    except sqlite3.OperationalError as e:
        print("SQLite OperationalError:", e)
        print("If ALTER TABLE failed, consider inspecting the schema or recreating the database.")
        sys.exit(2)
    finally:
        conn.close()


if __name__ == '__main__':
    cli_db = None
    if len(sys.argv) > 1:
        cli_db = sys.argv[1]
    # Pass cli_db into main by re-calling get_db_path inside main
    # (we'll just set an environment variable for simplicity)
    if cli_db:
        os.environ['ELS_DB_PATH'] = cli_db
    main()
