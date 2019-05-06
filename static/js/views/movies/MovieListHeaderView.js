define([
  'jquery',
  'underscore',
  'backbone',
  'text!templates/movies/movieListHeaderTemplate.html'
], function ($, _, Backbone, movieListHeaderTemplate) {
  var MovieListHeaderView = Backbone.View.extend({
    template: _.template(movieListHeaderTemplate),

    initialize: function (options) {
      _.bindAll(this, 'render')

      this.defaultGenre = options.defaultGenre
      this.render()
    },

    render: function () {
      var data = {
        defaultGenre: this.defaultGenre,
        _: _
      }
      var compiledTemplate = this.template(data)
      $('#movie-list-header').html(compiledTemplate)
    }
  })

  return MovieListHeaderView
})
