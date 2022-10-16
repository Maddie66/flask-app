import random
from tokenize import String
from flask import Flask, render_template, request, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db = SQLAlchemy(app)

movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_list['title'].values
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False) 
    poster = db.Column(db.Text, nullable=False)

    def __str__(self):
        return f'{self.id} {self.name} {self.poster}'


def movie_serializer(movie):
    return{
        'title': movie.name,
        'poster': movie.poster
    }

#to clear all the movies recommendation in database
@app.route('/clear', methods=['GET'])
def clear_data():
    for movie in Movie.query.all():
        Movie.query.filter_by(id=movie.id).delete()
    db.session.commit()
    return [{"a":"b"}]

#All the movies that the user might like
@app.route('/searched', methods=['GET'])
def searched():
    if Movie.query.first() == None:
        return [{ "title": "Aliens", "poster": "https://image.tmdb.org/t/p/w500/r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg" }, { "title": "Silent Running", "poster": "https://image.tmdb.org/t/p/w500/uWoj7EfHBprcssXUzCCWeI383Tx.jpg" }, { "title": "Moonraker", "poster": "https://image.tmdb.org/t/p/w500/6LrJdXNmu5uHOVALZxVYd44Lva0.jpg" }, { "title": "Alien", "poster": "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg" }, { "title": "Mission to Mars", "poster": "https://image.tmdb.org/t/p/w500/beDWEWxgFlt1UWvf2al9cjDol2i.jpg" }]
    return jsonify([*map(movie_serializer, Movie.query.all())])

#The similar movies according to the movie that users searched
@app.route('/similar', methods=['GET'])
def similar():
    jsonMovies = []
    if (Movie.query.first() == None):
        return [{ "title": "Aliens", "poster": "https://image.tmdb.org/t/p/w500/r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg" }, { "title": "Silent Running", "poster": "https://image.tmdb.org/t/p/w500/uWoj7EfHBprcssXUzCCWeI383Tx.jpg" }, { "title": "Moonraker", "poster": "https://image.tmdb.org/t/p/w500/6LrJdXNmu5uHOVALZxVYd44Lva0.jpg" }, { "title": "Alien", "poster": "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg" }, { "title": "Mission to Mars", "poster": "https://image.tmdb.org/t/p/w500/beDWEWxgFlt1UWvf2al9cjDol2i.jpg" }]
    for movie in Movie.query.all()[-5:]:
        jsonMovies.append(movie_serializer(movie))
    return jsonify(jsonMovies)

#The Movies users might like accoding to the searchinf history
@app.route('/mightLike', methods=['GET'])
def mightLike():
    jsonMovies = []
    indexes = []
    if (Movie.query.first() == None):
        return [{ "title": "Aliens", "poster": "https://image.tmdb.org/t/p/w500/r1x5JGpyqZU8PYhbs4UcrO1Xb6x.jpg" }, { "title": "Silent Running", "poster": "https://image.tmdb.org/t/p/w500/uWoj7EfHBprcssXUzCCWeI383Tx.jpg" }, { "title": "Moonraker", "poster": "https://image.tmdb.org/t/p/w500/6LrJdXNmu5uHOVALZxVYd44Lva0.jpg" }, { "title": "Alien", "poster": "https://image.tmdb.org/t/p/w500/vfrQk5IPloGg1v9Rzbh2Eg3VGyM.jpg" }, { "title": "Mission to Mars", "poster": "https://image.tmdb.org/t/p/w500/beDWEWxgFlt1UWvf2al9cjDol2i.jpg" }]
    if (len(Movie.query.all()) == 5):
        return jsonify([*map(movie_serializer, Movie.query.all())])
    for i in range(5):
        index = random.randint(0, len(Movie.query.all()))
        while (index in indexes or index >= len(Movie.query.all())):
            index = random.randint(0, len(Movie.query.all()))
        jsonMovies.append(movie_serializer(Movie.query.all()[index]))
        indexes.append(index)
    return jsonify(jsonMovies)

def fetch_poster(movie_id):
    movie_id = str(movie_id)
    response = requests.get('https://api.themoviedb.org/3/movie/'+movie_id
                            + '?api_key=f1d1f2255416c803d88a1d61f2b672d4')
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500'+data['poster_path']


#The machine learning part that find the similar movies
@app.route('/recommend', methods=["POST"])
def recommend():
    request_data = json.loads(request.data)
    movie = request_data["name"]
    
    movie_index = movies[movies['title'].str.lower() == movie.strip().lower()].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),
                         reverse=True, key=lambda x: x[1])[1:6]
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie = movies.iloc[i[0]].title
        addposter = fetch_poster(movie_id)
        addmovie = Movie(name=recommend_movie, poster=addposter)
        db.session.add(addmovie)
    
    db.session.commit()
    return {'201': "success"}

#all the movies in database
@app.route("/titles")
def titles():
    dictionary = []
    for i in movies_list:
        dictionary.append({"title": i})
    json_object = json.dumps(dictionary, indent=len(movies_list))
    return json_object


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5002)
