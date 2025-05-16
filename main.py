from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database file path
DATABASE = '/nfs/demo.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Enable name-based access to columns
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT,
                is_sample INTEGER DEFAULT 0
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
            if name and phone:
                db = get_db()
                db.execute('INSERT INTO contacts (name, phone, address, is_sample) VALUES (?, ?, ?, ?)', (name, phone, address, 0))
                db.commit()
                message = 'Contact added successfully.'
            else:
                message = 'Missing name or phone number.'

    db = get_db()
    contacts = db.execute('SELECT * FROM contacts').fetchall()

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contact List</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #333;
                    margin: 0;
                    padding: 20px;
                }
                h2 {
                    color: #4a90e2;
                    text-align: center;
                }
                table {
                    width: 90%;
                    margin: 20px auto;
                    border-collapse: collapse;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                th, td {
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: left;
                }
                th {
                    background-color: #f0f0f0;
                }
                .form-container {
                    width: 60%;
                    margin: 0 auto;
                    padding: 15px;
                    background-color: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                input[type="text"] {
                    width: 100%;
                    padding: 8px;
                    margin: 6px 0;
                    box-sizing: border-box;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
                .delete-btn {
                    background-color: #e74c3c;
                    padding: 6px 12px;
                }
                .delete-btn:hover {
                    background-color: #c0392b;
                }
            </style>
        </head>
        <body>
            <h2>📱 Contact List – Managed by Jenkins CI/CD</h2>
            <div class="form-container">
                <form method="POST" action="/">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" required>
                    <label for="phone">Phone Number:</label>
                    <input type="text" id="phone" name="phone" required>
                    <label for="address">Address:</label>
                    <input type="text" id="address" name="address">
                    <input type="submit" value="Add Contact">
                </form>
            </div>
            <p style="text-align:center; color:green;">{{ message }}</p>

            {% if contacts %}
                <table>
                    <tr>
                        <th>Name</th>
                        <th>Phone</th>
                        <th>Address</th>
                        <th>Delete</th>
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
