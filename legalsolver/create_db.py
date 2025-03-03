import os
import sqlite3

def create_database(db_file):
    """ Create a new SQLite database and a users table """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    
    conn = sqlite3.connect(db_file)
    try:
        cur = conn.cursor()
        # Create users table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        
        # Check if admin user already exists
        cur.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        admin_exists = cur.fetchone()[0] > 0
        
        # Insert admin user if it doesn't exist
        if not admin_exists:
            cur.execute('''
                INSERT INTO users (name, username, password)
                VALUES (?, ?, ?)
            ''', ('Administrator', 'admin', 'admin'))
            print("Admin user created successfully")
            
        conn.commit()
        print(f"Database and table created successfully in {db_file}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    # Use an absolute path for the database file
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    create_database(db_path) 