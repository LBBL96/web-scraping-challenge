from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars
import scrape

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars")

@app.route('/')
def index():
    mars_data = mongo.db.collection.find_one()
    
    # Activate jinja within the website index page
    return render_template('index.html', Mars=mars_data)
    

@app.route('/scrape')
def scrape():

    # Run the scrape function for Mars news and facts
    Mars_news = scrape_mars.JPL_scrape()

    # mars.append(Mars_news)
    mongo.db.Mars.update({}, Mars_news, upsert = True)

    # Redirect back to home page
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)