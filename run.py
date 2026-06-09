from util import db
import os

def main():
    conn = db.get_connection()

    # Verifica se já existem dados
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM aluno")
    count = cursor.fetchone()[0]

    if count > 0:
        print("Base de dados já tem dados, a ignorar o populamento.")
        return

    # Carrega dummy data só se a BD estiver vazia
    source_path = os.path.join("resources", "dummy_data")
    print(f"Loading dummy data from {source_path}...")
    db.load_dummy_data(source_path, truncate=True, conn=conn)

if __name__ == "__main__":
    main()