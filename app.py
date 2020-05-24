from flask import Flask, render_template
import StockData

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('webpage.html')

@app.route("/about")
def about():
    return render_template('about.html')

