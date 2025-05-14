import sqlite3

# Database file path, ensure this matches the path used in your Flask application
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_contacts():
    """Clear only the test contacts from the database."""
    db = connect_db()
    cursor = db.cursor()

    # Make sure the contacts table exists before deleting from it
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT
        )
    ''')

    # Delete test contacts that follow the naming pattern
    cursor.execute("DELETE FROM contacts WHERE name LIKE 'Test Name %'")
    db.commit()
    print('Test contacts have been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_contacts()
