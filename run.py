from util import db
import os

def main():
    # Get connection to DB or create DB if it does not exist
    conn = db.get_connection()
	
    # Load dummy data from CSV files
    source_path = os.path.join("resources", "dummy_data")
    print(f"Loading dummy data from {source_path}...")
    db.load_dummy_data(source_path, truncate=True, conn=conn)

    # # Fetch all tables in the database
    # tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
    # tables = db.fetchall(tables_query, conn)

    # # Display data from all tables
    # print("\n=== DATABASE CONTENT ===")
    # for (table_name,) in tables:
    #     print(f"\nTable: {table_name}")
    #     rows = db.fetchall(f"SELECT * FROM {table_name};", conn)
    #     for row in rows:
    #         print(row)
    #     if not rows:
    #         print("[No data]")

if __name__ == "__main__":
    main()