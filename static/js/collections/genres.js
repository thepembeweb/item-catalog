define(['underscore', 'backbone', 'models/genre'], function (
  _,
  Backbone,
  Genre
) {
  var GenresCollection = Backbone.Collection.extend({
    // Reference to this collection's model.
    model: Genre,

    // Save all of the todo items under the `"todos"` namespace.
    url: '/genres',

    parse: function (response) {
      return response.collection
    }
  })

  return GenresCollection
})
