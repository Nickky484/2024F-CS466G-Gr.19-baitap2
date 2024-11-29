import sqlite3
def create_data():
    b=sqlite3.connect("lst.db")
    cur=b.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            role TEXT 
        )
        
    ''')
    b.commit()
    b.close()
if __name__ == "__main__":
    create_data()
