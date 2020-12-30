from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Flask instance
app = Flask(__name__)

# Pymongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")

# Route to render
@app.route("/")
def main():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars_dict=mars)


# Trigger Scrape Function
@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape_info()
    mongo.db.collection.update({}, mars_dict, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)