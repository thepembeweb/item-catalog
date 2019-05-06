import os
import dicttoxml
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import session as login_session
from jinja2 import Markup
from werkzeug import secure_filename
from database import db_session
from models import Genre, Movie, User
from sqlalchemy.sql import func
from settings import UPLOAD_FOLDER

movies = Blueprint('movies', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


class InputDataHolder:

    """Helper class to store input fields data and their errors"""

    def __init__(self, errors, inputs):
        self.errors = errors
        self.inputs = inputs


def sanitize(key, value):
    """Helper function to sanitize data sent over the form.
    Returns a dictionary"""
    str_to_sanitize = value
    return {key: Markup(str_to_sanitize).striptags()}


def checkMovieForm(data_request):
    """Helper function to check if required fields in the form were filled.
    Returns a InputDataHolder instance"""
    errors = []
    sanitized_inputs = {}
    for key, value in data_request.iteritems():
        tmp = sanitize(key, value)
        if (tmp[key] == '' or tmp[key] is None):
            if(key == 'image_url'):
                pass
            else:
                errors.append(key)
        else:
            sanitized_inputs.update(tmp)
    return InputDataHolder(errors, sanitized_inputs)


def removeImage(image_url):
    """Remove image after movie has been deleted"""
    file_to_remove = os.path.join(UPLOAD_FOLDER, image_url)
    if(os.path.isfile(file_to_remove)):
        print 'File to remove', file_to_remove
        os.remove(file_to_remove)


# setup get Movies route
@movies.route('/movies', methods=['GET'])
def showAll():
    """RESTful method for reading movies"""
    genre_id = request.args.get('genre_id')
    user_id = request.args.get('user_id')
    xml_format = request.args.get('xml')

    if (genre_id != '' and genre_id is not None):
        movies_list = db_session.\
            query(Movie).filter_by(genre_id=genre_id).order_by(
                Movie.last_update.desc()).all()
    elif (user_id != '' and user_id is not None):
        movies_list = db_session.\
            query(Movie).filter_by(user_id=user_id).order_by(
                Movie.last_update.desc()).all()
    else:
        movies_list = db_session.query(Movie).order_by(
            Movie.last_update.desc()).all()

    serialized_result = [i.serialize for i in movies_list]
    if (xml_format == 'true' or xml_format == 'TRUE'):
        xml_output = dicttoxml.dicttoxml(serialized_result)
        return xml_output, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    else:
        return jsonify(collection=serialized_result)


# setup show Movie route
@movies.route('/movies/<int:movie_id>', methods=['GET'])
def showMovie(movie_id):
    """RESTful method for reading a single movie"""
    xml_format = request.args.get('xml')
    movies_list = db_session.query(Movie).filter(
        Movie.id == movie_id).all()
    serialized_result = [i.serialize for i in movies_list]

    if (xml_format == 'true' or xml_format == 'TRUE'):
        xml_output = dicttoxml.dicttoxml(serialized_result)
        return xml_output, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    else:
        return jsonify(collection=serialized_result)


# setup Movie delete route
@movies.route('/movies/<int:movie_id>', methods=['DELETE'])
def deleteMovie(movie_id):
    """RESTful method for deleting a movie"""
    if request.headers.get('moviezone-token') != login_session['state']:
        resp = jsonify(error=['You are not allowed to make such request.'])
        resp.status_code = 401
        return resp

    if 'username' not in login_session:
        resp = jsonify(error=['You are not allowed to do this'])
        resp.status_code = 401
        return resp

    movie = db_session.query(Movie).filter(
        Movie.id == movie_id).one()

    if movie.user_id != login_session['user_id']:
        resp = jsonify(error=['You are not authorized to do this!'])
        resp.status_code = 403
        return resp

    if(movie.image_url is not None):
        removeImage(movie.image_url)

    db_session.delete(movie)
    db_session.commit()
    return jsonify(id=movie.id)


# setup Movie add route
@movies.route('/movies', methods=['POST'])
def addMovie():
    """RESTful method for creating a movie"""
    if request.headers.get('moviezone-token') != login_session['state']:
        resp = jsonify(error=['You are not allowed to make such request.'])
        resp.status_code = 401
        return resp

    if 'username' not in login_session:
        resp = jsonify(error=['You are not allowed to do this'])
        resp.status_code = 401
        return resp

    data = checkMovieForm(request.get_json())
    if (len(data.errors) == 0):
        newMovie = Movie(
            name=data.inputs['name'],
            description=data.inputs['description'],
            duration=data.inputs['duration'],
            rating=data.inputs['rating'],
            genre_id=data.inputs['genre_id'],
            user_id=login_session['user_id'])
        db_session.add(newMovie)
        db_session.commit()
        return jsonify(id=newMovie.id, name=newMovie.name)
    else:
        resp = jsonify(error=data.errors)
        resp.status_code = 400
        return resp


# setup Movie update route
@movies.route('/movies/<int:movie_id>', methods=['PUT'])
def updateMovie(movie_id):
    """RESTful method for updating a movie"""
    if request.headers.get('moviezone-token') != login_session['state']:
        resp = jsonify(error=['You are not allowed to make such request.'])
        resp.status_code = 401
        return resp

    if 'username' not in login_session:
        resp = jsonify(error=['You are not allowed to do this'])
        resp.status_code = 401
        return resp

    movie = db_session.query(Movie).filter_by(id=movie_id).one()

    if movie.user_id != login_session['user_id']:
        resp = jsonify(error=['You are not authorized to do this!'])
        resp.status_code = 403
        return resp

    data = checkMovieForm(request.get_json())
    if (len(data.errors) == 0):
        movie.name = data.inputs['name']
        movie.description = data.inputs['description']
        movie.duration = data.inputs['duration']
        movie.rating = data.inputs['rating']
        movie.genre_id = data.inputs['genre_id']
        movie.last_update = func.now()
        db_session.add(movie)
        db_session.commit()
        return jsonify(collection=[movie.serialize])
    else:
        resp = jsonify(error=data.errors)
        resp.status_code = 400
        return resp


def allowed_file(filename):
    """Check if what we are trying to upload is a valid file (picture)"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# setup picture upload route
@movies.route('/uploadpicture/<movie_id>', methods=['POST'])
def upload_picture(movie_id):
    """Upload and associate image with a movie"""
    if request.headers.get('moviezone-token') != login_session['state']:
        resp = jsonify(error=['You are not allowed to make such request.'])
        resp.status_code = 401
        return resp

    if 'username' not in login_session:
        resp = jsonify(error=['You are not allowed to do this'])
        resp.status_code = 401
        return resp

    movie = db_session.query(Movie).filter_by(id=movie_id).one()

    if movie.user_id != login_session['user_id']:
        resp = jsonify(error=['You are not authorized to do this!'])
        resp.status_code = 403
        return resp

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = str(movie.id) + '-' + secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        if(movie.image_url is not None):
            removeImage(movie.image_url)
        movie.image_url = filename
        db_session.add(movie)
        db_session.commit()
        return jsonify(collection=[movie.serialize])
    else:
        errorMsg = """It \'s likely that
        you sent an invalid format file.
        Could not process your request."""
        resp = jsonify(error=[errorMsg])
        resp.status_code = 400
        return resp
