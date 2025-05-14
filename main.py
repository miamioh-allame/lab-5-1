from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # This enables name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''  # Message indicating the result of the operation
    if request.method == 'POST':
        # Check if it's a delete action
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            db.commit()
            message = 'Contact deleted successfully.'
        else:
            name = request.form.get('name')
            phone = request.form.get('phone')
            if name and phone:
                db = get_db()
                db.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
                db.commit()
                message = 'Contact added successfully.'
            else:
                message = 'Missing name or phone number.'

    # Always display the contacts table
    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()

    # Display the HTML form along with the contacts table
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contacts</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body class="bg-light">
            <div class="container mt-5">
                <h2 class="mb-4">Contact List</h2>

                <form method="POST" action="/" class="mb-4 p-4 bg-white shadow rounded">
                    <div class="mb-3">
                        <label for="name" class="form-label">Name:</label>
                        <input type="text" id="name" name="name" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label for="phone" class="form-label">Phone Number:</label>
                        <input type="text" id="phone" name="phone" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary">Add Contact</button>
                </form>

                {% if message %}
                    <div class="alert alert-info">{{ message }}</div>
                {% endif %}

                {% if contacts %}
                    <table class="table table-bordered table-striped bg-white shadow">
                        <thead class="table-dark">
                            <tr>
                                <th>Name</th>
                                <th>Phone Number</th>
                                <th>Delete</th>
                            </tr>
                        </thead>
                        <tbody>
                        {% for contact in contacts %}
                            <tr>
                                <td>{{ contact['name'] }}</td>
                                <td>{{ contact['phone'] }}</td>
                                <td>
                                    <form method="POST" action="/">
                                        <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                        <input type="hidden" name="action" value="delete">
                                        <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                                    </form>
                                </td>
                            </tr>
                        {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <p>No contacts found.</p>
                {% endif %}
            </div>
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()  # Initialize the database and table
    app.run(debug=True, host='0.0.0.0', port=port)
