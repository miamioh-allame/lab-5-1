from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f2f5;
            padding: 20px;
        }
        h2 {
            text-align: center;
            color: #333;
        }
        table {
            width: 90%;
            margin: auto;
            border-collapse: collapse;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        th, td {
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #007BFF;
            color: white;
        }
        td {
            color: #333;
        }
        .delete-button {
            background-color: #dc3545;
            color: white;
            padding: 6px 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .delete-button:hover {
            background-color: #c82333;
        }
    </style>
</head>
<body>
    <h2>👥 Contact List &mdash; Powered by Jenkins CI/CD</h2>
    <table>
        <tr>
            <th>Name</th>
            <th>Phone</th>
            <th>Address</th>
            <th>Delete</th>
        </tr>
        {% for contact in contacts %}
        <tr>
            <td>{{ contact[0] }}</td>
            <td>{{ contact[1] }}</td>
            <td>{{ contact[2] }}</td>
            <td><button class="delete-button">Delete</button></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def contact_list():
    conn = sqlite3.connect("/nfs/demo.db")
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            name TEXT,
            phone TEXT,
            address TEXT
        )
    """)

    cur.execute("SELECT COUNT(*) FROM contacts")
    if cur.fetchone()[0] == 0:
        real_contacts = [
            ("Marie Alla", "513-888-2342", "101 Main St"),
            ("John Smith", "305-456-7890", "22 Oak Ave"),
            ("Lisa Ray", "312-555-1212", "77 Park Blvd"),
            ("Tony Lee", "412-667-7789", "9 Maple Ct"),
            ("Amy Wu", "215-300-2020", "44 Birch Rd")
        ]
        sample_contacts = [
            (f"Sample Contact {i}", f"999-000-{1000+i}", f"Fake Address {i}")
            for i in range(1, 16)
        ]
        cur.executemany("INSERT INTO contacts (name, phone, address) VALUES (?, ?, ?)", real_contacts + sample_contacts)
        conn.commit()

    cur.execute("SELECT name, phone, address FROM contacts")
    rows = cur.fetchall()
    conn.close()
    return render_template_string(TEMPLATE, contacts=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
