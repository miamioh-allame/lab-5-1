from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Contacts</title>
    <style>
        body { font-family: Arial; background-color: #f9f9f9; }
        table { width: 70%; margin: auto; border-collapse: collapse; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #eee; }
    </style>
</head>
<body>
    <h2 style="text-align:center;">📞 Contact List – Powered by Jenkins CI/CD</h2>
    <table>
        <tr><th>Name</th><th>Phone</th><th>Delete</th></tr>
        {% for contact in contacts %}
        <tr>
            <td>{{ contact[0] }}</td>
            <td>{{ contact[1] }}</td>
            <td>🗑️ Delete</td>
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

    # Create table if it doesn't exist
    cur.execute("CREATE TABLE IF NOT EXISTS contacts (name TEXT, phone TEXT)")

    # Seed if empty
    cur.execute("SELECT COUNT(*) FROM contacts")
    if cur.fetchone()[0] == 0:
        contacts = [
            ('Marie Alla', '513-888-2342'),
            ('John Smith', '385-456-7890'),
            ('Lisa Ray', '312-555-1212')
        ]
        cur.executemany("INSERT INTO contacts (name, phone) VALUES (?, ?)", contacts)
        conn.commit()

    # Retrieve and show all contacts
    cur.execute("SELECT name, phone FROM contacts")
    rows = cur.fetchall()
    conn.close()
    return render_template_string(TEMPLATE, contacts=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

