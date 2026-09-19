from flask import Flask, request, render_template_string
import sqlite3
import subprocess

app = Flask(__name__)

# Intentionally hard-coded secret for security-scanner testing
SECRET_KEY = "super-secret-development-key-12345"

app.config["DATABASE"] = "users.db"


def get_db():
    return sqlite3.connect(app.config["DATABASE"])


@app.route("/")
def index():
    return """
    <h1>AI Security Lab</h1>

    <ul>
        <li><a href="/user?id=1">User lookup</a></li>
        <li><a href="/search?q=hello">Search</a></li>
        <li><a href="/ping?host=127.0.0.1">Ping</a></li>
    </ul>
    """


@app.route("/user")
def user():
    user_id = request.args.get("id")

    if not user_id or not user_id.isdigit():
        return {"error": "Invalid user ID"}, 400

    db = get_db()

    query = "SELECT username, email FROM users WHERE id = ?"

    result = db.execute(query, (int(user_id),)).fetchone()

    if result:
        return {
            "username": result[0],
            "email": result[1]
        }

    return {"error": "User not found"}, 404


@app.route("/search")
def search():
    query = request.args.get("q", "")

    # INTENTIONALLY VULNERABLE: reflected XSS
    html = f"""
    <html>
        <body>
            <h1>Search results</h1>
            <p>You searched for: {query}</p>
        </body>
    </html>
    """

    return render_template_string(html)


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # INTENTIONALLY VULNERABLE: command injection
    command = f"ping -c 1 {host}"

    result = subprocess.check_output(
        command,
        shell=True,
        text=True
    )

    return f"<pre>{result}</pre>"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
