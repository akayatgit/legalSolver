import os
import sqlite3
from db_connection import initialize_database

def check_database_structure():
    """Check the structure of the database"""
    print("Checking database structure...")
    
    # Initialize the database first
    initialize_database()
    
    # Use an absolute path for the database file
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = sqlite3.connect(db_path)
    
    if conn is None:
        print("Failed to create database connection.")
        return
    
    try:
        with conn:
            cur = conn.cursor()
            
            # Check if the users table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cur.fetchall()
            print(f"Tables in database: {[table[0] for table in tables]}")
            
            # Check the structure of the users table
            cur.execute("PRAGMA table_info(users)")
            columns = cur.fetchall()
            print("\nColumns in users table:")
            for column in columns:
                print(f"  {column[1]} ({column[2]}){' PRIMARY KEY' if column[5] else ''}{' NOT NULL' if column[3] else ''}")
            
            # Check if there are any users in the database
            cur.execute("SELECT COUNT(*) FROM users")
            user_count = cur.fetchone()[0]
            print(f"\nNumber of users in database: {user_count}")
            
    except sqlite3.Error as e:
        print(f"Error checking database structure: {e}")

if __name__ == "__main__":
    check_database_structure() 