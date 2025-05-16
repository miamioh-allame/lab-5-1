import sqlite3

# Ensure this path matches what your Flask app uses
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_test_contacts():
    """Clear only the test contacts from the database."""
    db = connect_db()

    # Ensure table exists before trying to delete
    db.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')

    # Delete only test contacts matching the naming pattern
    db.execute("DELETE FROM contacts WHERE name LIKE 'Test Name %'")
    db.commit()
    print('Test contacts have been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_test_contacts()
