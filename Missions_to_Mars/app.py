from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars")

# Route to index page to render Mongo data to template
@app.route("/")
def index():

    # Find one record of data from Mongo
    Mars_data = mongo.db.Mars.find_one()
    
    # Activate jinja within the website index page
    return render_template("index.html", mars=Mars_data)
    

@app.route("/scrape")
def scrape():

    # Run the scrape function for Mars news and facts
    mars_data = scrape_mars.Mars_scrape()

    # mars.append
    mongo.db.Mars.update({}, mars_data, upsert = True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)