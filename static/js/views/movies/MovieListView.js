define([
  'jquery',
  'underscore',
  'backbone',
  'views/movies/MovieListItemView',
  'views/movies/MovieListHeaderView',
  'views/user/UserHeaderView',
  'models/user',
  'collections/movies',
  'text!templates/movies/movieListTemplate.html',
  'domready',
  'imageloader',
  'foundation.dropdown',
  'foundation.reveal'
], function (
  $,
  _,
  Backbone,
  MovieListItemView,
  MovieListHeaderView,
  UserHeaderView,
  User,
  MovieCollection,
  movieListTemplate,
  domready,
  imageloader
) {
  var MovieListView = Backbone.View.extend({
    el: $('#container'),

    events: {
      'click .card-delete-btn': 'deleteItem'
    },

    template: _.template(movieListTemplate),

    initialize: function (options) {
      var self = this

      this.genres = options.genres

      self.mapped_genres = []
      _.each(self.genres.models, function (genre) {
        self.mapped_genres[genre.get('id')] = genre.get('name')
      })

      _.bindAll(
        this,
        'addOne',
        'initFoundation',
        'deleteItem',
        'confirmedDeleteItem',
        'abortedDeleteItem'
      )
    },

    populate: function (genre_id, user_id) {
      var queryParams = {}

      if (genre_id) {
        queryParams.data = {
          genre_id: genre_id
        }
      } else if (user_id) {
        queryParams.data = {
          user_id: user_id
        }
      }

      queryParams.success = function (movies) {
        // If there are no movies
        if (movies.length == 0) {
          var emptyCategory = '<div class="row"><div class="small-12 columns">'
          emptyCategory +=
            '<h2 class="text-center">There are no items in this category.</h2>'
          emptyCategory += '</div></div>'

          $('.movie-list-container').html(emptyCategory)
        }
      }

      this.undelegateEvents()
      this.delegateEvents()

      this.collection = new MovieCollection()
      this.collection.bind('add', this.addOne)
      // Let's init the foundation plugins when we have done adding movies to the view
      this.collection.bind('update', this.initFoundation)

      this.render(genre_id, user_id)
      this.collection.fetch(queryParams)
    },

    render: function (genre_id, user_id) {
      var defaultGenre = {
        id: 0,
        name: 'All the genres'
      }

      if (genre_id) {
        defaultGenre.id = genre_id
        defaultGenre.name = this.mapped_genres[genre_id]
      }

      var data = {
        genres: this.mapped_genres,
        defaultGenre: defaultGenre,
        _: _
      }

      var compiledTemplate = this.template(data)
      this.$el.html(compiledTemplate)

      if (user_id) {
        var user = new User({
          id: user_id
        })
        user.parse = function (response) {
          return response.collection[0]
        }
        var userInfo = new UserHeaderView({
          model: user
        })
      } else {
        var subNav = new MovieListHeaderView({
          defaultGenre: defaultGenre
        })
      }
    },

    addOne: function (movie) {
      var view = new MovieListItemView({
        model: movie,
        mapped_genres: this.mapped_genres
      })
      $('.movie-list').append(view.render().el)
      imageloader.revalidate()
    },

    initFoundation: function () {
      var self = this

      domready(function () {
        $(document).foundation()
      })
    },

    deleteItem: function (e) {
      e.preventDefault()
      var self = this
      var target = e.target ? e.target : e.srcElement
      var targetID = target.getAttribute('data-id')
      var model = this.collection.get(targetID)
      $('.confirm-deletion-confirm').data('id', targetID)
      $('#confirm-deletion-name').text(model.get('name'))
      $('#confirm-deletion').foundation('reveal', 'open')
      $('.confirm-deletion-confirm').one('click', self.confirmedDeleteItem)
      $('.confirm-deletion-abort').one('click', self.abortedDeleteItem)
    },

    confirmedDeleteItem: function (e) {
      e.preventDefault()
      var targetID = $('.confirm-deletion-confirm').data('id')
      var modelToDelete = this.collection.get(targetID)
      modelToDelete.clear()
      $('#confirm-deletion').foundation('reveal', 'close')
    },

    abortedDeleteItem: function (e) {
      e.preventDefault()
      $('#confirm-deletion').foundation('reveal', 'close')
    }
  })
  return MovieListView
})
