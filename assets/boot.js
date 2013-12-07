(function (window, document, undefined) {
  var page = require('page');
  var top = require('top');
  var $ = require('semantic-ui');
  
  var common = require('./view');

  // to top
  top();


  /* page route */
  page('/', function () {
    var cb = require('./logined').registerEvents;
    common.render('home', cb);
    activeTab('home');
  });

  page('/-/view/user/:username', function (ctx) {
    var username = ctx.params.username;
    var user = require('./user');
    user.viewUser(username);
  });

  page('/-/:view/:operation?', function (ctx) {
    var view = ctx.params.view;
    var operation = ctx.params.operation;
    if (operation) {
      var user = require('./user');
      if (operation === 'signout') {
        return user.signout();
      }

      else if (operation === 'signin') {
        common.render('login-form', user.registerSigninEvents);
        activeTab('signin');
      }
      else if (operation === 'signup') {
        common.render('signup-form', user.registerSignupEvents);
        activeTab('signin');
      }

      else if (operation === 'setting') {
        common.render('setting-form', user.registerSettingEvents);
        activeTab('signin');
      }
    }

    else {
      var cb = require('./logined').registerEvents;
      common.render(view, cb);
      activeTab(view);
    }
  });

  page();

  function activeTab(tab) {
    $('.nav-item').removeClass('active');
    $('.nav-' + tab).addClass('active');
  }

})(window, document);
