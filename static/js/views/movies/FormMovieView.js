define([
  'jquery',
  'underscore',
  'backbone',
  'collections/movies',
  'models/movie',
  'views/flash/FlashView',
  'views/movies/AddPictureView',
  'text!templates/movies/formMovieTemplate.html',
  'domready',
  'foundation.slider'
], function (
  $,
  _,
  Backbone,
  MovieCollection,
  MovieModel,
  FlashView,
  AddPictureView,
  newMovieTemplate,
  domready
) {
  var FormMovieView = Backbone.View.extend({
    el: $('#container'),

    events: {
      'submit #new-movie-form': 'addMovie'
    },

    initialize: function (options) {
      this.genres = options.genres
      _.bindAll(this, 'render', 'addMovie')
    },

    populate: function (movie_id) {
      this.undelegateEvents()
      this.delegateEvents()
      this.collection = new MovieCollection()

      // Let's nullify the model first
      this.model = null
      this.actual_genre = null

      if (movie_id) {
        this.model = new MovieModel({
          id: movie_id
        })
        this.model.parse = function (response) {
          return response.collection[0]
        }
        this.collection.add(this.model)

        this.model.bind('sync', this.render)

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
      } else {
        this.render()
      }
    },

    render: function (movie) {
      if (movie) {
        this.actual_genre = parseInt(movie.get('genre_id'))
      }

      var data = {
        movie: movie,
        genres: this.genres.models,
        _: _
      }

      var compiledTemplate = _.template(newMovieTemplate)(data)
      this.$el.html(compiledTemplate)

      this.pullupPage()

      domready(function () {
        $(document).foundation('slider', 'reflow')

        $('.rating label').click(function (e) {
          e.preventDefault()
          var targetId = e.target.getAttribute('for')
          $('#' + targetId).prop('checked', true)
        })
      })
    },

    addMovie: function (e) {
      e.preventDefault()

      var self = this

      $(document).trigger('close.fndtn.alert')

      var flash = new FlashView()

      /**
       * If it's not a brand new movie -> PUT
       */
      if (this.model) {
        $('#new-movie-form')
          .serializeArray()
          .forEach(function (el) {
            self.model.set(el.name, el.value)
          })

        this.model.save(movie, {
          success: function (model, resp) {
            var genreId = parseInt(model.get('genre_id'))

            // If we have changed genre we have to update the counter
            if (self.actual_genre !== genreId) {
              var $new_counter = $('.genre-count').filter(function (index, el) {
                return parseInt($(el).attr('data-genre-count')) === genreId
              })

              var $old_counter = $('.genre-count').filter(function (index, el) {
                return (
                  parseInt($(el).attr('data-genre-count')) === self.actual_genre
                )
              })

              var newCounterValue = parseInt($new_counter.text() || '0') + 1

              var oldCounterValue = parseInt($old_counter.text()) - 1

              oldCounterValue = oldCounterValue === 0 ? '' : oldCounterValue

              $new_counter.text(newCounterValue.toString())

              $old_counter.text(oldCounterValue.toString())
            }

            var successMsg = ''
            successMsg += '<b>'
            successMsg += self.model.get('name')
            successMsg += '</b>'
            successMsg += ' updated successfully.'

            flash.render('success', successMsg)

            Backbone.history.history.back()
          },
          error: function (model, error) {
            var errorMsg = ''
            errorMsg += '<b>' + error.status + '</b>'
            errorMsg += ' Something went wrong. --->'
            for (var i = 0; i < error.responseJSON.error.length; i++) {
              errorMsg += ' <b>' + error.responseJSON.error[i] + '</b>'
            }

            flash.render('error', errorMsg)
          }
        })

        /**
         * If we are creating a new movie from scratch -> POST
         */
      } else {
        var movie = {}

        $('#new-movie-form')
          .serializeArray()
          .forEach(function (el) {
            var currentObject = {}

            currentObject[el.name] = el.value

            movie = $.extend({}, movie, currentObject)
          })

        this.collection.create(movie, {
          success: function (model, resp) {
            // Let's pass the model id and name to the second form
            // i.e. form for adding a picture
            var addPicView = new AddPictureView({
              movie_id: resp.id,
              old: false
            })

            // Update the counter in the menu
            var genreId = parseInt(model.get('genre_id'))

            var $counter = $('.genre-count').filter(function (index, el) {
              return parseInt($(el).attr('data-genre-count')) === genreId
            })

            var $totalCount = $('#total-count')

            var actualValue = parseInt($counter.text() || '0') + 1

            var totalValue = parseInt($totalCount.text() || '0') + 1

            $counter.text(actualValue.toString())

            $totalCount.text(totalValue.toString())
          },
          error: function (model, error) {
            var errorMsg = ''
            errorMsg += '<b>' + error.status + '</b>'
            errorMsg += ' Something went wrong. --->'
            for (var i = 0; i < error.responseJSON.error.length; i++) {
              errorMsg += ' <b>' + error.responseJSON.error[i] + '</b>'
            }

            flash.render('error', errorMsg)
          }
        })
      }
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
  return FormMovieView
})
