from util import db
import os

def main():
    conn = db.get_connection()

    # Verifica se já existem dados
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    total = 0
    for (table_name,) in tables:
        cursor.execute(f"SELECT COUNT(*) FROM '{table_name}'")
        count = cursor.fetchone()[0]
        total += count
        print(f"{table_name}: {count} registos")

    print(f"\nTotal global: {total} registos")

    if total > 0:
        print("Base de dados já tem dados, a ignorar o populamento.")
        return

    # Carrega dummy data só se a BD estiver vazia
    source_path = os.path.join("resources", "dummy_data")
    print(f"Loading dummy data from {source_path}...")
    db.load_dummy_data(source_path, truncate=True, conn=conn)

if __name__ == "__main__":
    main()