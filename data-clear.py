import sqlite3

# Database file path, ensure this matches the path used in your Flask application
DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)


def clear_sample_contacts():
    db = sqlite3.connect("/nfs/demo.db")
    cursor = db.cursor()
    cursor.execute("DELETE FROM contacts WHERE name LIKE 'Sample Contact %'")
    db.commit()
    db.close()
    print("Sample contacts removed.")

if __name__ == '__main__':
    clear_sample_contacts()
