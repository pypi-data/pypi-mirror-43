from flask import Flask
app = Flask(__name__)

@app.route("/add")
def add(a,b):
    z=a+b
    print(z)
add(10,20)
