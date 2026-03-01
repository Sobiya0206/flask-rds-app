from flask import Flask, render_template, request, redirect
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_connection():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    return conn


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (?)", name)
        conn.commit()
        conn.close()

        return redirect("/")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template("index.html", users=users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)