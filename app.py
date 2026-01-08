from flask import Flask, request, render_template
from detector import validate_login

app = Flask(__name__)

# Dummy database
users = {
    "admin": "admin123",
    "junaid": "cyber@123"
}

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0]
    return request.remote_addr

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    ip = get_client_ip()

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        result = validate_login(ip, username, password, users)

        if result == "blocked":
            message = "🚫 Too many attempts. Try again later."
        elif result == "success":
            message = "✅ Login successful"
        else:
            message = "❌ Invalid credentials"

    return render_template("login.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
