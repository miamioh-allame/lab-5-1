from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL
            );
        ''')
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        if request.form.get('action') == 'delete':
            contact_id = request.form.get('contact_id')
            db = get_db()
            db.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            db.commit()
            message = 'Contact deleted successfully.'
        else:
            name = request.form.get('name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            if name and phone and address:
                db = get_db()
                db.execute('INSERT INTO contacts (name, phone, address) VALUES (?, ?, ?)', (name, phone, address))
                db.commit()
                message = 'Contact added successfully.'
            else:
                message = 'Missing contact details.'

    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contact List</title>
            <style>
                body { font-family: Arial; background-color: #f2f2f2; }
                table { width: 80%; margin: auto; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 12px; border: 1px solid #ddd; text-align: center; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                h2 { text-align: center; color: #4CAF50; }
                .form-container { width: 50%; margin: auto; padding: 20px; background: white; border-radius: 10px; box-shadow: 0 0 10px #ccc; }
                input[type=text], input[type=submit] {
                    width: 100%; padding: 10px; margin: 5px 0 10px 0; border: 1px solid #ccc; border-radius: 5px;
                }
                input[type=submit] { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
                input[type=submit]:hover { background-color: #45a049; }
                .delete-btn { background-color: #f44336; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; }
                .delete-btn:hover { background-color: #e53935; }
            </style>
        </head>
        <body>
            <div class="form-container">
                <h2>Manage Contacts</h2>
                <form method="POST" action="/">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required>

                    <label for="phone">Phone Number:</label>
                    <input type="text" id="phone" name="phone" required>

                    <label for="address">Address:</label>
                    <input type="text" id="address" name="address" required>

                    <input type="submit" value="Add Contact">
                </form>
                <p>{{ message }}</p>
            </div>

            {% if contacts %}
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Address</th>
                        <th>Action</th>
                    </tr>
                    {% for contact in contacts %}
                        <tr>
                            <td>{{ contact['name'] }}</td>
                            <td>{{ contact['phone'] }}</td>
                            <td>{{ contact['address'] }}</td>
                            <td>
                                <form method="POST" action="/">
                                    <input type="hidden" name="contact_id" value="{{ contact['id'] }}">
                                    <input type="hidden" name="action" value="delete">
                                    <input type="submit" value="Delete" class="delete-btn">
                                </form>
                            </td>
                        </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p style="text-align:center;">No contacts found.</p>
            {% endif %}
        </body>
        </html>
    ''', message=message, contacts=contacts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(debug=True, host='0.0.0.0', port=port)
