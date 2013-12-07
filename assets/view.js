var ajax = require('ajax');
var $ = require('jquery');
var _ = require('underscore');
var moment = require('moment');

moment.lang('zh-cn');


/* fetch status */

var cache = {};

function query(qs, fn) {
  var url = qs.url || '/hole/',
  options = {
    url: url,
    type: 'GET',
    success: fn
  };

  if (qs.data)
    options.data = qs.data;

  ajax(options);
}

exports.query = query;

// helpers 
var currentColor = 'blue';
function changeColor(view) {
  var colors = {
    home: 'blue',
    hole: 'red',
    user: 'teal',
    signin: 'purple'
  };
  $('.ng-changeColor')
    .removeClass(_.values(colors).join(' '))
    .addClass(colors[view]);
  currentColor = colors[view];
}


exports.render = function (type, count, page, fn) {
  /**
  @property type 
  @type String
  @default '/user/'
  */
  var qs = {}, tpl;
  qs.data = {};

  var urlMap;

  if (type === 'login-form' ||
      type === 'signup-form' ||
      type === 'setting-form') {
    urlMap = {
      'login-form': '/-/user/signin',
      'signup-form': '/-/user/signup',
      'setting-form': '/-/user/setting'
    };
    qs.url = urlMap[type];
    fn = function (json) {
      cache.formHTML = json.data;
      $('.js-mainarea').html(json.data);
      changeColor('signin');

      _.isFunction(count) && count();
    };
  }
  else if (type === 'status-form') {
    urlMap = {
      'status-form': '/',
    };
    qs.url = urlMap[type];

    if (cache.formHTML && !(/username/.test(cache.formHTML))) {
      $('.js-mainarea').html(cache.formHTML);
      if (_.isFunction(page))
        page();
      return changeColor(count);
    }

    else {
      fn = function (json) {
        cache.formHTML = json.data;
        $('.js-mainarea').html(json.data);
        changeColor(count);
        if (_.isFunction(page))
          page();
      };
    }

    return query(qs, fn);
  }

  else if (type === 'user' ||
           type === 'hole' ||
           type === 'home') {

    exports.render('status-form', type, count);

    type = type === 'home' ? 'hole' : type;  // show recent status in home
    urlMap = {
      'user': '/-/user/',
      'hole': '/-/hole/'
    };
    qs.url = urlMap[type];
    fn = null;
  }

  if (!fn && _.isFunction(page))
    fn = page;
  else if (_.isNumber(page))
    qs.data.page = page;

  if (_.isNumber(count))
    qs.data.count = count;


  if (!fn) {
    // default callback
    var classMap = {
      user: 'user-flag list divided',
      hole: 'hole-flag feed'
    };
    if (($('.user-flag').length && type !== 'user') ||
        ($('.hole-flag').length && type !== 'hole'))
      $('.js-dynamicarea').html('');
    $('.js-dynamicarea')
      .removeClass(_.values(classMap).join(' '))
      .addClass(classMap[type]);
    tpl = require('./templates/' + type);
    fn = function (json) {
      if (!(_.isObject(json)) || !(json.data)) return;
      if (!json.data.length)
        return noMore();
      if (json.data[0].created) {
        _.each(json.data, function (item) {
          item.created = moment.utc(item.created, 'YYYY-MM-DD HH:mm:ss')
          .fromNow();
        });
      }
      var html = _.template(tpl, {data: json.data});
      $('.js-dynamicarea').html(html);
    };
  }

  query(qs, fn);
};


exports.parseForm = function parseForm(form) {
  var ret = {};
  Array.prototype.slice.call(form)
  .filter(function (node) { return node.name; })
  .map(function (node) {
    ret[node.name] = node.value;
  });

  return ret;
};


function noMore() {
  $(window).off('scroll');
  $('.js-message')
    .html('没有更多了...')
    .addClass('info')
    .fadeIn(300);
}
