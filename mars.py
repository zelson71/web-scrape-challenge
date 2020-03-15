from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import os
import marsScraper

# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scraper")
mars_data = {}
mars_data = mongo.db.collection.find_one()
# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    
#    mars_data = mongo.db.collection.find_one()

    # Return template and data#
    return render_template("index.html", mars_scrape={})
    
# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_final = marsScraper.scrape_mars()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_final, upsert=True)
    mars_data = mongo.db.collection.find_one()
    # Redirect back to home page
#    return redirect("/")
    return render_template("index.html", mars_scrape=mars_data)

if __name__ == "__main__":
    app.run(debug=True)
