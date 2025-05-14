import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DATABASE)

def clear_sample_contacts():
    """Delete only sample contacts from the database."""
    db = connect_db()
    cursor = db.cursor()

    cursor.execute('''
        DELETE FROM contacts
        WHERE name LIKE 'Sample Contact%'
    ''')

    db.commit()
    print('Sample contacts have been deleted from the database.')
    db.close()

if __name__ == '__main__':
    clear_sample_contacts()
