define(['underscore', 'backbone', 'models/movie'], function (
  _,
  Backbone,
  Movie
) {
  var MoviesCollection = Backbone.Collection.extend({
    // Reference to this collection's model.
    model: Movie,

    url: '/movies',

    parse: function (response) {
      return response.collection
    }
  })

  return MoviesCollection
})
