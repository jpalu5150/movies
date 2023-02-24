# Import Flask and the necessary libraries
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Set up the Flask app
app = Flask(__name__)

# Set up the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
ma = Marshmallow(app)
db = SQLAlchemy(app)


# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    
    def __init__(self, title, year, genre ):
        self.title = title
        self.year = year
        self.genre = genre
        
class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title' , 'year', 'genre')
        
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


#this is the first endpoint single post
@app.route('/movie', methods=['POST'])
def add_movie():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON CHUMP')

    #post_data = request.get_json()
    title = request.json['title']
    genre = request.json['genre']
    year = request.json['year']

    if title == None:
        return jsonify('Error: Title cannot be empty you must supply a valid title')
    new_movie  = Movie(title, genre, year)
    db.session.add(new_movie)
    db.session.commit()
    
    movie = Movie.query.get(new_movie.id)
    return movie_schema.jsonify(movie)

#end point for returning all movies 

@app.route("/movies", methods=['GET'])
def get_movies():
    all_movies = Movie.query.all()
    result =  movies_schema.dump(all_movies)
    return jsonify(result)

# get single movie
@app.route("/movie/<id>", methods=["GET"])
def get_movie(id):
    movie = Movie.query.get(id)
    return movie_schema.jsonify(movie)

#update movie by id
@app.route("/movie/edit/<id>", methods=["PUT"])
def movie_update(id):
    movie = Movie.query.get(id)
    title = request.json['title']
    genre = request.json['genre']
    year = request.json['year']

    movie.title = title
    movie.genre = genre
    movie.year = year 

    db.session.commit()
    return movie_schema.jsonify(movie)

#Endpoint for deleting a record
@app.route("/movie/<id>", methods = ["DELETE"])
def movie_delete(id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    return "Guide was successfully deleted"


if __name__ == "__main__":
    app.run(debug=True)


