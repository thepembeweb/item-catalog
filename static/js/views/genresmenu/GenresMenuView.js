define([
  'jquery',
  'underscore',
  'backbone',
  'genremenu',
  'text!templates/genresmenu/genresMenuTemplate.html',
  'domready'
], function ($, _, Backbone, genremenu, newMovieTemplate, domready) {
  var GenresMenuView = Backbone.View.extend({
    el: $('#modal-menu-ctr'),

    render: function (genres) {
      var totalCount = 0

      _.each(genres.models, function (genre) {
        totalCount += genre.get('count')
      })

      var data = {
        genres: genres.models,
        totalCount: totalCount,
        _: _
      }

      var compiledTemplate = _.template(newMovieTemplate)(data)
      this.$el.html(compiledTemplate)
    }
  })
  return new GenresMenuView()
})
