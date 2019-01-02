$(document).ready(function () {
  $('#notifications > span').map(function (i, e) {
    var category = $(e).attr('data-category');
    var title = $(e).attr('data-title');
    var message = $(e).attr('data-message');
    new PNotify({
      'title': title,
      'text': message,
      'type': category,
      'styling': 'bootstrap3',
      'hide': true,
      'delay': 10000
    })
  })
})
