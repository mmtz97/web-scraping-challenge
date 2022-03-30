from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_data")


@app.route("/")
def home():
    nasa_data = mongo.db.nasa_info.find_one()
    print(nasa_data)
    return render_template("index.html", nasa_data=nasa_data)


@app.route("/scrape")
def scrape():
    nasa_data = scrape_mars.scrape_info()
    mongo.db.nasa_info.update_one({}, {"$set": nasa_data}, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)