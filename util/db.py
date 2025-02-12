import csv
import logging
import sqlite3
import os

from config import *

def get_connection(database_path: str = None) -> sqlite3.Connection:
    """
    Create and return a database connection. If not database path is provided
    then the connection is returned for the default database.

    The database is created if it does not exist.

    Args:
        database_path (str, optional): The name of the database. Defaults to None in which
            case the default database path is used.

    Returns:
        sqlite3.Connection: The database connection.
    """
    if not database_path:
        database_path = DB_PATH
    database_folder = os.path.split(database_path)[0]
    if database_folder and not os.path.exists(database_folder):
        os.makedirs(database_folder)
    conn = sqlite3.connect(database_path)
    return conn
    
def fetchall(query: str, conn: sqlite3.Connection = None) -> list:
    """
    Fetch all records for the provided SELECT query.

    Args:
        query (str): A SELECT query.
        conn (sqlite3.Connection, optional): The database connection. Defaults to None.

    Returns:
        list: The list of rows in the query result.
    """
    _conn = get_connection() if conn is None else conn
    cursor = _conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if conn is None:
        _conn.close
    return rows

def drop_table(table_name: str, conn: sqlite3.Connection = None):
    """
    Drop a table if it exists

    Args:
        table_name (str): The name of the table
        conn (sqlite3.Connection, optional): The database connection. Defaults to None.
    """    
    _conn = get_connection() if conn is None else conn
    cursor = _conn.cursor()
    query = f"DROP TABLE IF EXISTS {table_name};"
    cursor.execute(query)
    _conn.commit()
    if conn is None:
        _conn.close

def insert_into_table(table_name: str, row: dict, conn: sqlite3.Connection = None):
    """
    Inserts a row into any specified table.
    
    Args:
        table_name (str): Name of the table.
        row (dict): Dictionary containing column names and values.
        conn (sqlite3.Connection, optional): Database connection. If None, creates a new one.
    """
    if not row:
        raise ValueError("The data dictionary cannot be empty.")
    
    _conn = get_connection() if conn is None else conn
    
    query = f"""
        INSERT INTO {table_name} ({', '.join(row.keys())})
        VALUES ({', '.join(['?' for _ in row])});
    """
    
    cursor = _conn.cursor()
    cursor.execute(query, tuple(row.values()))
    _conn.commit()
    
    if conn is None:
        _conn.close()

def table_exists(table_name: str, conn: sqlite3.Connection) -> bool:
    """Check if a table exists in the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cursor.fetchone() is not None

def load_dummy_data(source_path: str, truncate: bool, conn: sqlite3.Connection = None):
    """
    Load dummy data from CSV files into corresponding database tables.
    
    Args:
        source_path (str): Directory containing CSV files.
        truncate (bool): If True, existing data will be deleted before inserting new data.
    """
    conn = get_connection() if conn is None else conn
    for file in os.listdir(source_path):
        if file.endswith(".csv"):
            table_name = os.path.splitext(file)[0]
            file_path = os.path.join(source_path, file)
            
            if not table_exists(table_name, conn):
                logging.warning(f"Skipping {file}: Table '{table_name}' does not exist in the database.")
                continue
            
            cursor = conn.cursor()
            if truncate:
                cursor.execute(f"DELETE FROM {table_name};")
                conn.commit()
            
            with open(file_path, newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    insert_into_table(table_name, row, conn)
    
    conn.close()