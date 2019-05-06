define([
  'jquery',
  'underscore',
  'backbone',
  'collections/movies',
  'models/movie',
  'text!templates/movies/movieTemplate.html',
  'domready',
  'foundation.dropdown',
  'foundation.reveal'
], function (
  $,
  _,
  Backbone,
  MovieCollection,
  MovieModel,
  movieTemplate,
  domready
) {
  var MovieView = Backbone.View.extend({
    el: $('#container'),

    events: {
      'click .movie-delete-btn': 'deleteItem'
    },

    template: _.template(movieTemplate),

    initialize: function (options) {
      var self = this
      this.genres = options.genres

      self.mapped_genres = []
      _.each(self.genres.models, function (genre) {
        self.mapped_genres[genre.get('id')] = genre.get('name')
      })

      _.bindAll(
        this,
        'render',
        'deleteItem',
        'confirmedDeleteItem',
        'abortedDeleteItem'
      )
    },

    populate: function (movie_id) {
      this.undelegateEvents()
      this.delegateEvents()

      this.model = new MovieModel({
        id: movie_id
      })
      this.model.parse = function (response) {
        return response.collection[0]
      }
      this.collection = new MovieCollection([this.model])

      this.model.bind('change', this.render)

      var queryParams = {
        success: function (movies, response) {
          if (response.collection.length == 0) {
            var emptyCategory =
              '<div class="row"><div class="small-12 columns">'
            emptyCategory +=
              '<h2 class="text-center m-t-3">There are no movies corresponding to the given id.</h2>'
            emptyCategory += '</div></div>'

            self.$el.html(emptyCategory)
          }
        }
      }

      this.model.fetch(queryParams)
    },

    render: function (movie) {
      var data = {
        genres: this.mapped_genres,
        movie: movie,
        _: _
      }

      var compiledTemplate = this.template(data)
      this.$el.html(compiledTemplate)

      this.pullupPage()

      $('.go-back-btn').one('click', function (e) {
        e.preventDefault()
        Backbone.history.history.back()
      })

      domready(function () {
        $(document).foundation()
      })
    },

    deleteItem: function (e) {
      e.preventDefault()
      var self = this
      $('#confirm-deletion-name').text(self.model.get('name'))
      $('#confirm-deletion').foundation('reveal', 'open')
      $('.confirm-deletion-confirm').one('click', self.confirmedDeleteItem)
      $('.confirm-deletion-abort').one('click', self.abortedDeleteItem)
    },

    confirmedDeleteItem: function (e) {
      e.preventDefault()
      this.model.clear()
      $('#confirm-deletion').foundation('reveal', 'close')
      Backbone.history.history.back()
    },

    abortedDeleteItem: function (e) {
      e.preventDefault()
      $('#confirm-deletion').foundation('reveal', 'close')
    },

    pullupPage: function () {
      $('html, body').animate(
        {
          scrollTop: 0
        },
        0
      )
    }
  })
  return MovieView
})
