from util import db
import os

def main():
    # Get connection to DB or create DB if it does not exist
    conn = db.get_connection()

    # Create a table
    # db.drop_table('aluno', conn)
    # db.create_table_aluno(conn)

    # Insert (dummy) data to table
    # db.insert_to_aluno({"nome_proprio": "João", "apelido": "Silva"}, conn)
    # db.insert_to_aluno({"nome_proprio": "Maria", "apelido": "Santos"}, conn)
    # db.insert_to_aluno({"nome_proprio": "Pedro", "apelido": "Almeida"}, conn)
	
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