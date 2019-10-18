from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
# import scrape_mars
import Mars_scrape

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars")

@app.route('/')
def index():
    mars_data = mongo.db.collection.find_one()
    # mars_weather = mongo.db.collection.find_one()
    return render_template('index.html', Mars=mars_data)
    

@app.route('/scrape')
def scrape():

    # Run the scrape function for Mars news and facts
    Mars_news = Mars_scrape.Mars_Scrape()
    # mars.append(Mars_news)
    mongo.db.Mars.update({}, Mars_news, upsert = True)

    # Redirect back to home page
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)