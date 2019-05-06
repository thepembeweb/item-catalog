define(['jquery', 'underscore', 'backbone', 'views/flash/FlashView'], function (
  $,
  _,
  Backbone,
  FlashView
) {
  var MovieModel = Backbone.Model.extend({
    clear: function () {
      var self = this
      var flash = new FlashView()
      this.destroy({
        success: function (model, resp) {
          var successMsg = 'The movie '
          successMsg += '<b>' + model.get('name') + '</b>'
          successMsg += ' was deleted succesfully'
          flash.render('success', successMsg)

          // Update the counter in the menu
          var genreId = parseInt(model.get('genre_id'))

          var $counter = $('.genre-count').filter(function (index, el) {
            return parseInt($(el).attr('data-genre-count')) === genreId
          })

          var $totalCount = $('#total-count')

          var actualValue = parseInt($counter.text()) - 1

          actualValue = actualValue === 0 ? '' : actualValue

          var totalValue = parseInt($totalCount.text()) - 1

          totalValue = totalValue === 0 ? '' : totalValue

          $counter.text(actualValue.toString())

          $totalCount.text(totalValue.toString())

          self.view.remove()
        },
        error: function (model, error) {
          var errorMsg = ''
          errorMsg += '<b>' + error.status + '</b>'
          for (var i = 0; i < error.responseJSON.error.length; i++) {
            errorMsg += ' <b>' + error.responseJSON.error[i] + '</b>'
          }
          flash.render('error', errorMsg)
        }
      })
    }
  })
  return MovieModel
})
