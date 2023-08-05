
from flask import Flask
from flask import viwes

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, I love Digital Ocean!"

if __name__ == "__main__":
    app.run()
