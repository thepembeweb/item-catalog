#!/usr/bin/env python
# coding: utf-8

import dicttoxml
from flask import Blueprint
from flask import request
from flask import jsonify
from database import db_session
from models import Genre, Movie
from sqlalchemy import func
from inspect import getmembers
from pprint import pprint

genres = Blueprint('genres', __name__)


# setup show Genres route
@genres.route('/genres', methods=['GET'])
def showGenres():
    count = request.args.get('count')
    catalog_mode = request.args.get('catalog')
    xml_format = request.args.get('xml')

    if (catalog_mode == 'true' or catalog_mode == 'TRUE'):
        genre_list = db_session.query(Genre).all()

        genres = []

        for i in genre_list:
            movies = []
            for movie in i.genre_movies:
                movies.append(movie.serialize)
            genre = i.serialize
            genre['movies'] = movies
            genres.append(genre)

        serialized_result = genres

    elif (count == 'true' or count == 'TRUE'):
        genre_list = db_session.query(Genre).all()

        genres = []

        for i in genre_list:
            genre = {'name': i.name, 'id': i.id}
            genre['count'] = len(i.genre_movies)
            genres.append(genre)

        serialized_result = genres

    else:
        genre_list = db_session.query(Genre).all()
        serialized_result = [i.serialize for i in genre_list]

    if (xml_format == 'true' or xml_format == 'TRUE'):
        xml_output = dicttoxml.dicttoxml(serialized_result)
        return xml_output, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    else:
        return jsonify(collection=serialized_result)


# setup Genre update route
@genres.route('/genres/<int:genre_id>', methods=['GET'])
def showOne(genre_id):
    catalog_mode = request.args.get('catalog')
    xml_format = request.args.get('xml')

    genre_list = db_session.query(Genre).filter(
        Genre.id == genre_id).all()

    if (catalog_mode == 'true' or catalog_mode == 'TRUE'):
        genres = []

        for i in genre_list:
            movies = []
            for movie in i.genre_movies:
                movies.append(movie.serialize)
            genre = i.serialize
            genre['movies'] = movies
            genres.append(genre)

        serialized_result = [genres]
    else:
        serialized_result = [i.serialize for i in genre_list]

    if (xml_format == 'true' or xml_format == 'TRUE'):
        xml_output = dicttoxml.dicttoxml(serialized_result)
        return xml_output, 200, {'Content-Type': 'text/xml; charset=utf-8'}
    else:
        return jsonify(collection=serialized_result)
