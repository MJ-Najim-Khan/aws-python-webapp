from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>AWS Python Web Application</title>
</head>
<body>
    <h1>AWS Python Web Application</h1>
    <p>Running with Flask + Docker + AWS ECS</p>
    <p>API endpoint: <a href="/hello">/hello</a></p>
</body>
</html>
"""


@app.route("/hello", methods=["GET"])
def hello():
    return jsonify({
        "message": "Hello from ECS Fargate!",
        "application": "Python Web App",
        "status": "success"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)