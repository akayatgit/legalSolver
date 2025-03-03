from db_connection import check_user_credentials

def login(username, password):
    if check_user_credentials(username, password):
        print("Login successful!")
        # Proceed with login
    else:
        print("Invalid username or password.")
        # Handle login failure 