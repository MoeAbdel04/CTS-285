from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit-text", methods=["POST"])
def submit_text():
    # Get the text from the input field
    user_input = request.form["user_input"]
    return f"You entered: {user_input}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
