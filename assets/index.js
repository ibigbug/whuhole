var $ = require('bootstrap');
var moment = require('moment');


$('.timeago').each(function (index, element) {
  $(element).html(moment($(this).attr('datetime')).fromNow());
});

$('.js-logout').click(function () {
  var url = $(this).data('url');

  $.ajax({
    type: 'POST',
    url: url
  }).done(function () {
    location.reload();
  });
});

$('.js-like').click(function () {
  var url = $(this).data('url');
  $.ajax({
    type: 'POST',
    url: url
  }).done(function () {
    location.reload();
  });
});
