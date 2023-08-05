from flask import Flask
app = Flask(__name__)

@app.route("/add")
def add(a,b):
    z=a+b
add()

if __name__ == "__main__":
    app.run()
