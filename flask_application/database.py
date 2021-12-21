import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''CREATE TABLE search_history (search_id INTEGER PRIMARY KEY NOT NULL, file_name TEXT NOT NULL, result TEXT NOT NULL);''')
        conn.commit()
        print("table created successfully")
    except Exception as e:
        print(e)
        print("table creation failed or table exists")
    finally:
        conn.close()

def insert_search_history(search_history):
    inserted_search_history = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO search_history(file_name, result) VALUES  (?, ?)", (search_history['file_name'], search_history['result']) )
        conn.commit()
        a = cur.lastrowid
    except Exception as e:
        conn().rollback()
    finally:
        conn.close()
    return a


def get_search_historys():
    search_historys = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM search_history")
        rows = cur.fetchall()
        for i in rows:
            search_history = {}
            search_history["search_id"] = i["search_id"]
            search_history["file_name"] = i["file_name"]
            search_history["result"] = i["result"]
            search_historys.append(search_history)
    except Exception as e:
        print(e)
        search_historys = []
    return search_historys