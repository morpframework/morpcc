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
  });

  $('#windowFullScreen').click(function () {
    var elem = document.body;
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) { /* Firefox */
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
      elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE/Edge */
      elem.msRequestFullscreen();
    }
  });

  $(document).on('click', '.modal-link', function (event) {
    var url = $(this).attr('data-url');
    $('#iframe-modal iframe').attr('src', url);
    $('#iframe-modal').modal();
  });

});