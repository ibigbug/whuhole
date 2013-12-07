var ajax = require('ajax');
var _ = require('underscore');
var $ = require('jquery');


exports.viewUser = function (username) {
  console.log(username);
};

exports.signout = function () {
  ajax({
    type: 'POST',
    url: '/-/user/signout',
    success: function () {
      location.href = '/';
    }
  });
};

exports.registerSigninEvents = function () {
  $('.js-mainarea').on('click', '.js-login', _.debounce(function () {
    var form = $('.login-form')[0];
    $(form).addClass('loading');
    var data = $(form).serialize();
    ajax({
      type: 'POST',
      url: '/-/user/signin',
      data: data,
      dataType: 'json',
      success: function (json) {
        if (json.stat === 'ok') {
          location.href = '/';
        }
        else {
          $('.js-mainarea').html(json.data);
        }
      }
    });
  }, 3000, true));
};

exports.registerSignupEvents = function () {
  $('.js-signup').on('click', _.debounce(function () {
    var form = $('.signup-form')[0];
    $(form).addClass('loading');
    var data = $(form).serialize();
    ajax({
      type: 'POST',
      url: '/-/user/signin',
      data: data,
      dataType: 'json',
      success: function (json) {
        if (json.stat === 'ok') {
          location.href = '/';
        }
        else {
          $('.js-mainarea').html(json.data);
        }
      }
    });
  }, 3000, true));
};

exports.registerSettingEvents = function () {
  $('.js-setting').on('click', _.debounce(function () {
    var form = $('.setting-form')[0];
    $(form).addClass('loading');
    var data = $(form).serialize();
    ajax({
      type: 'POST',
      url: '/-/user/signin',
      data: data,
      dataType: 'json',
      success: function (json) {
        console.log(json.data);
      }
    });
  }, 3000, true));
};
