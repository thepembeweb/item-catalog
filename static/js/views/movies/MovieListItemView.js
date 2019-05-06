define([
  'jquery',
  'underscore',
  'backbone',
  'text!templates/movies/movieListItemTemplate.html'
], function ($, _, Backbone, movieListItemTemplate) {
  var MovieListItemView = Backbone.View.extend({
    tagName: 'li',

    className: 'movie-list-item',

    template: _.template(movieListItemTemplate),

    initialize: function (options) {
      _.bindAll(this, 'render')
      this.model.view = this
      this.mapped_genres = options.mapped_genres
    },

    render: function () {
      var data = {
        genres: this.mapped_genres,
        movie: this.model,
        _: _
      }

      var compiledTemplate = this.template(data)
      this.$el.append(compiledTemplate)

      return this
    }
  })
  return MovieListItemView
})
