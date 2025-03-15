from util import db

def main():
    # Get connection to DB or create DB if it does not exist
    conn = db.get_connection()

    # Create a table
    db.drop_table('aluno', conn)
    db.create_table_aluno(conn)

    # Insert (dummy) data to table
    db.insert_to_aluno({"nome_proprio": "João", "apelido": "Silva"}, conn)
    db.insert_to_aluno({"nome_proprio": "Maria", "apelido": "Santos"}, conn)
    db.insert_to_aluno({"nome_proprio": "Pedro", "apelido": "Almeida"}, conn)
	
    # Get all data from table
    query = "SELECT * FROM aluno;"
    rows = db.fetchall(query, conn)
    conn.close()
    for row in rows:
        print(row)

if __name__ == "__main__":
    main()