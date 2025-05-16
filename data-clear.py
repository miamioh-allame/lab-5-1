import sqlite3

DATABASE = '/nfs/demo.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def clear_test_contacts():
    """Delete only the sample/test contacts."""
    db = connect_db()
    db.execute("DELETE FROM contacts WHERE name LIKE 'Test Name %'")
    db.commit()
    print('Test contacts have been deleted.')
    db.close()

if __name__ == '__main__':
    clear_test_contacts()
