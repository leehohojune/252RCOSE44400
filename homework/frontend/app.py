from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

# URL of the backend container inside Docker network
BACKEND_URL = "http://backend:5001"


@app.route("/", methods=["GET"])
def index():
    """
    TODO:
    - Send a GET request to BACKEND_URL + "/api/message"
    - Extract the message from the JSON response
    - Render index.html and pass the message as "current_message"
    """
    response = requests.get(BACKEND_URL + "/api/message")
    stored_message = response.json().get("message", "")

    current_message = stored_message
    last_updated = ""

    marker = " (updated at "
    if stored_message.endswith(")") and marker in stored_message:
        base, _, ts_part = stored_message.rpartition(marker)
        if base:
            current_message = base
        if ts_part.endswith(")"):
            ts_part = ts_part[:-1]
        last_updated = ts_part

    return render_template(
        "index.html",
        current_message=current_message,
        last_updated=last_updated,
    )


@app.route("/update", methods=["POST"])
def update():
    """
    TODO:
    - Get the value from the form field named "new_message"
    - Send a POST request to BACKEND_URL + "/api/message"
      with JSON body { "message": new_message }
    - Redirect back to "/"
    """
    new_message = request.form.get("new_message", "")
    response = requests.post(BACKEND_URL + "/api/message", json={"message": new_message})
    return redirect("/")


# v2 TODO:
# - Change page title (in HTML)
# - Parse timestamp from backend message
# - Show "Last updated at: <timestamp>" in the template


if __name__ == "__main__":
    # Do not change the host or port
    app.run(host="0.0.0.0", port=5000)
