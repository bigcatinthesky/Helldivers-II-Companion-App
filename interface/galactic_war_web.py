from flask import Flask, response

app = Flask(__name__)

@app.route('/')
def home():
    raise RuntimeError("not yet implemented")

def run_app():
    app.run()