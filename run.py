from util import db
import os

def main():
    # Get connection to DB or create DB if it does not exist
    conn = db.get_connection()

    source_path = os.path.join("resources", "dummy_data")
    print(f"Loading dummy data from {source_path}...")
    db.load_dummy_data(source_path, truncate=True, conn=conn)


if __name__ == "__main__":
    main()