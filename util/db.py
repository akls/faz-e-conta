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

def create_table_aluno(conn: sqlite3.Connection = None):
    """
    Create the 'aluno' table.

    Args:
        conn (sqlite3.Connection, optional): The database connection. Defaults to None.
    """    
    _conn = get_connection() if conn is None else conn
    cursor = _conn.cursor()
    query = f"""
        CREATE TABLE IF NOT EXISTS aluno (
            nome_proprio TEXT,
            apelido TEXT
        );
    """
    cursor.execute(query)
    _conn.commit()
    if conn is None:
        _conn.close

def insert_to_aluno(row: dict, conn: sqlite3.Connection= None):
    """
    Insert a row into the aluno table.

    Args:
        row (dict): The column name(s) and value(s).
        conn (sqlite3.Connection, optional): The database connection. Defaults to None.
    """
    _conn = get_connection() if conn is None else conn
    query = f"""
        INSERT INTO aluno ({', '.join(row.keys())})
        VALUES ({", ".join(len(row)*'?')});
    """
    cursor = _conn.cursor()
    cursor.execute(query, tuple(row.values()))
    _conn.commit()
    if conn is None:
        _conn.close

