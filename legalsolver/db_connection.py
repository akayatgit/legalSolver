import os
import sqlite3
import uuid
import datetime

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_file), exist_ok=True)
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
    return conn

def initialize_database():
    """ Ensure all required tables and columns are present in the database """
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = create_connection(db_path)
    if conn is None:
        print("Failed to create database connection.")
        return False

    try:
        with conn:
            cur = conn.cursor()
            
            # Check if the users table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
            table_exists = cur.fetchone() is not None
            
            if not table_exists:
                # Create users table if it doesn't exist
                cur.execute('''
                    CREATE TABLE users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        full_name TEXT,
                        email TEXT
                    )
                ''')
                print("Users table created successfully.")
            else:
                # Check if required columns exist
                cur.execute("PRAGMA table_info(users)")
                columns = [column[1] for column in cur.fetchall()]
                
                # Add email column if it doesn't exist
                if 'email' not in columns:
                    print("Adding email column to users table...")
                    try:
                        cur.execute("ALTER TABLE users ADD COLUMN email TEXT")
                        print("Email column added successfully.")
                    except sqlite3.Error as e:
                        print(f"Error adding email column: {e}")
                
                # Add full_name column if it doesn't exist
                if 'full_name' not in columns:
                    print("Adding full_name column to users table...")
                    try:
                        cur.execute("ALTER TABLE users ADD COLUMN full_name TEXT")
                        print("Full_name column added successfully.")
                    except sqlite3.Error as e:
                        print(f"Error adding full_name column: {e}")
            
            # Check if document_history table exists
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='document_history'")
            doc_table_exists = cur.fetchone() is not None
            
            if not doc_table_exists:
                # Create document_history table if it doesn't exist
                cur.execute('''
                    CREATE TABLE document_history (
                        doc_id TEXT PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        filename TEXT NOT NULL,
                        original_filename TEXT NOT NULL,
                        upload_date TIMESTAMP NOT NULL,
                        analysis_results TEXT,
                        file_path TEXT NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                print("Document history table created successfully.")
            
        return True
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")
        return False

def register_user(username, password, email=None, full_name=None):
    """ Register a new user in the database """
    # Initialize the database first
    if not initialize_database():
        return False, "Database initialization failed"
    
    # Use an absolute path for the database file
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = create_connection(db_path)
    if conn is None:
        return False, "Failed to create database connection"

    try:
        with conn:
            cur = conn.cursor()
            # Check if username already exists
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            if cur.fetchone():
                return False, "Username already exists"
            
            # Check if email already exists (if provided)
            if email:
                cur.execute("SELECT * FROM users WHERE email=?", (email,))
                if cur.fetchone():
                    return False, "Email already exists"
            
            # Insert new user
            cur.execute(
                "INSERT INTO users (name, username, password, email, full_name) VALUES (?, ?, ?, ?, ?)",
                (username, username, password, email, full_name)
            )
            return True, "User registered successfully"
    except sqlite3.Error as e:
        return False, f"Registration error: {e}"

def check_user_credentials(username, password):
    """ Check if the provided username and password match a user in the database """
    # Initialize the database first
    initialize_database()
    
    # Use an absolute path for the database file
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = create_connection(db_path)
    if conn is None:
        print("Failed to create database connection.")
        return False

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT user_id, username, email, full_name FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        return user

def get_user_id(username):
    """ Get the user_id for a given username """
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = create_connection(db_path)
    if conn is None:
        print("Failed to create database connection.")
        return None

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users WHERE username=?", (username,))
        result = cur.fetchone()
        return result[0] if result else None

def save_document_history(username, original_filename, file_path, analysis_results):
    """ Save document history to the database """
    user_id = get_user_id(username)
    if not user_id:
        return None
    
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = create_connection(db_path)
    if conn is None:
        return None

    try:
        with conn:
            cur = conn.cursor()
            doc_id = str(uuid.uuid4())
            upload_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cur.execute(
                "INSERT INTO document_history (doc_id, user_id, filename, original_filename, upload_date, analysis_results, file_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (doc_id, user_id, os.path.basename(file_path), original_filename, upload_date, analysis_results, file_path)
            )
            return doc_id
    except sqlite3.Error as e:
        print(f"Error saving document history: {e}")
        return None

def get_user_documents(username):
    """ Get all documents for a specific user """
    user_id = get_user_id(username)
    if not user_id:
        return []
    
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = create_connection(db_path)
    if conn is None:
        print("Failed to create database connection.")
        return []

    with conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT doc_id, original_filename, upload_date, file_path FROM document_history WHERE user_id=? ORDER BY upload_date DESC",
            (user_id,)
        )
        return cur.fetchall()

def get_document_by_id(doc_id):
    """Get document details by document ID"""
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = create_connection(db_path)
    if conn is None:
        return None

    try:
        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM document_history WHERE doc_id = ?
            ''', (doc_id,))
            document = cur.fetchone()
            
            if document:
                return dict(document)
            return None
    except sqlite3.Error as e:
        print(f"Error retrieving document: {e}")
        return None

def get_user_by_id(user_id):
    """Get user details by user ID"""
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    conn = create_connection(db_path)
    if conn is None:
        return None

    try:
        with conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute('''
                SELECT * FROM users WHERE user_id = ?
            ''', (user_id,))
            user = cur.fetchone()
            
            if user:
                return dict(user)
            return None
    except sqlite3.Error as e:
        print(f"Error retrieving user: {e}")
        return None 