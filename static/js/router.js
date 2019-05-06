// Filename: router.js
define([
  'jquery',
  'underscore',
  'backbone',
  'views/topbar/TopBarView',
  'views/movies/MovieListView',
  'views/movies/MovieView',
  'views/movies/FormMovieView',
  'views/genresmenu/GenresMenuView',
  'views/movies/AddPictureView',
  'collections/genres'
], function (
  $,
  _,
  Backbone,
  TopBarView,
  MovieListView,
  MovieView,
  FormMovieView,
  GenresMenuView,
  AddPictureView,
  GenreCollection
) {
  $.ajaxSetup({
    headers: {
      Accept: 'application/json; charset=UTF-8',
      'Content-Type': 'application/json; charset=UTF-8'
    }
  })

  var AppRouter = Backbone.Router.extend({
    routes: {
      movies: 'showMovies',

      new_movie: 'newMovie',

      'genre/:genre_id': 'filterByGenre',

      'movie/:movie_id': 'showOneMovie',

      'edit/:movie_id': 'editMovie',

      'picture/:movie_id': 'editPicture',

      'user/:user_id': 'showUser',

      // Default
      '*actions': 'showMovies'
    }
  })

  var initialize = function () {
    var app_router = new AppRouter()

    var genres = new GenreCollection()

    // Fetch data from the collections
    var promise = _.invoke([genres], 'fetch', {
      data: {
        count: 'true'
      }
    })

    // When genres are collected, let's render the view
    $.when.apply($, promise).done(function () {
      var formMovie = new FormMovieView({
        genres: genres
      })

      var movieList = new MovieListView({
        genres: genres
      })

      var readMovieView = new MovieView({
        genres: genres
      })

      app_router.on('route:showMovies', function () {
        movieList.populate()
      })

      app_router.on('route:filterByGenre', function (genre_id) {
        movieList.populate(genre_id)
      })

      app_router.on('route:newMovie', function () {
        formMovie.populate()
      })

      app_router.on('route:editMovie', function (movie_id) {
        formMovie.populate(movie_id)
      })

      app_router.on('route:editPicture', function (movie_id) {
        var addPicView = new AddPictureView({ movie_id: movie_id, old: true })
      })

      app_router.on('route:showOneMovie', function (movie_id) {
        readMovieView.populate(movie_id)
      })

      app_router.on('route:showUser', function (user_id) {
        movieList.populate(null, user_id)
      })

      GenresMenuView.render(genres)

      Backbone.history.start()
    })
  }

  return {
    initialize: initialize
  }
})
