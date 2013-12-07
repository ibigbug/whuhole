var $ = require('jquery');
var validate = require('validate-form');
var ajax = require('ajax');
var _ = require('underscore');

var parseForm = require('./view').parseForm;
var render = require('./view').render;


exports.registerEvents = function () {
  /* publish form */
  var form = $('.publish-form')[0];
  if (!form)
    return;
  var validator = validate(form)
    .field('content')
      .is('required', '请输入要发布的内容')
      .is('minimum', 3, '至少3个字')
      .is('maximum', 240, '至多240个字');

  $('.js-publish').on('click', function () {
    validator.validate(function (valid) {
      if (!valid)
        return;
      var url = form.action || location.href;
      var type = form.type || 'POST';
      var data = parseForm(form);
      ajax({
        url: url,
        type: type,
        data: data,
        success: function () {
          $('.message>.header').html('发送成功!');
          $('.message')
            .addClass('success')
            .fadeIn(500)
            .delay(500)
            .fadeOut(0)
            .removeClass('success');
        }
      });
    });
  });

  if ($('.user-flag').length)
    registerScroll('user');
  else
    registerScroll('hole');
};

function registerScroll(type) {
  $(window).on('scroll', _.debounce(function () {
    var page = Math.ceil($('.feed-item').length / 10);
    var sT = $(window).scrollTop(),
        h = $(document).height();
    if ((sT / h) > 0.3) {
      render(type, 10, page);
    }
  }, 200, true));
}
