var $ = require('bootstrap');
$('.js-logout').click(function () {
  var url = $(this).data('url');

  var logout_xhr = $.ajax({
    type: 'POST',
    url: url
  }).done(function () {
    location.reload();
  });;
});
