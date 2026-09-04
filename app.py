from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/hello")
def hello():
    return jsonify({
        "message": "Hello from Python Flask!",
        "status": "success"
    })


@app.route("/api/info")
def info():
    return jsonify({
        "application": "AWS Python Web App",
        "platform": "Docker",
        "deployment": "ECS"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
