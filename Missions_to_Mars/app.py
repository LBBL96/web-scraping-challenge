from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars")

@app.route('/')
def index():
    mars_data = mongo.db.collection.find_one()
    # mars_weather = mongo.db.collection.find_one()
    return render_template('index.html', Mars=mars_data)
    # return render_template('index.html', Mars=mars_weather)
    
    # mars_facts = mongo.db.collection.find_one()
    # return render_template('index.html', Mars=mars_facts)



@app.route('/scrape')
def scrape():

     # Make a list to hold outputs of scrapes
    # mars = []

    # # Run the scrape function for Mars news
    Mars_news = scrape_mars.NASA_scrape()
    # mars.append(Mars_news)
    mongo.db.collection.update({}, Mars_news, upsert = True)

    # Mars weather function
    Mars_weather = scrape_mars.mars_weather_scrape()
    # mars.append(Mars_weather)
    mongo.db.collection.update({}, Mars_weather, upsert = True)

    # Update the Mongo database using update and upsert=True
    # mongo.db.collection.update({}, *mars, upsert=True)

   

    #Mars facts function
    # Mars_facts = scrape_mars.Mars_Facts_scrape()

    #Update the Mongo database using update and upsert=True
    # mongo.db.collection.update({}, Mars_facts, upsert=True) 

    # Redirect back to home page
    return redirect('/')

# @app.route('/scrape2')
# def scrape2():

#     # Mars weather function
#     Mars_weather = scrape_MarsWeather.mars_weather_scrape()

#     # Update the Mongo database using update and upsert=True
#     mongo.db.collection.update({}, Mars_weather, upsert=True) 

    # Mars facts function
    # Mars_facts = scrape_MarsFacts.Mars_Facts_scrape()

    # Update the Mongo database using update and upsert=True
    # mongo.db.collection.update({}, Mars_facts, upsert=True) 

if __name__ == "__main__":
    app.run(debug=True)