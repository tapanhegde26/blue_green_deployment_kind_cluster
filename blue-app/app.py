from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return """
    <html>
        <head>
            <title>Welcome</title>
        </head>
        <body style="background-color: blue; color: white; text-align: center; padding-top: 20%;">
            <h1>Welcome to blue deployment</h1>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8880)


