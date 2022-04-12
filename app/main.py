from flask import Flask

app = Flask(__name__)


@app.route("/")
def home_view():
    return "<h1>If you see this, your python app has a webpage</h1>"