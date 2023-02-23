# Import Flask and the necessary libraries
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import jsonify
import os


# Set up the Flask app
app = Flask(__name__)

# Set up the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)

# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    poster_img = db.Column(db.String, unique=True)

    def __init__(self, title, genre, poster_img):
        self.title = title
        self.genre = genre
        self.poster_img = poster_img

@app.route('/movie/add', methods=['POST'])
def add_movie():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON CHUMP')

    post_data = request.get_json()
    title = post_data.get('title')
    genre = post_data.get('genre')
    mpaa_rating = post_data.get('mpaa_rating')
    poster_img = post_data.get('poster_img')

    if title == None:
        return jsonify('Error: Title cannot be empty you must supply a valid title')

    new_record  = Movie(title, genre, mpaa_rating, poster_img)
    db.session.add(new_record)
    db.session.commit()

    # console.log('Added movie record')
    return jsonify(movie_schema.dump(new_record))

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ('id', 'star_rating', 'review_text', 'movie_id')
        
review_schema = ReviewSchema()
multi_review_schema = ReviewSchema(many=True)


class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'genre', 'mpaa_rating', 'poster_img', 'all_reviews')
    all_reviews = ma.Nested(multi_review_schema)

movie_schema = MovieSchema()
multi_movie_schema = MovieSchema(many=True)



if __name__ == "__main__":
    app.run(debug=True)