from flask import Blueprint
from flask import g, request, flash, current_app
from flask import render_template, redirect, url_for, jsonify

from flask.ext.babel import lazy_gettext as _

from ..models import Account, Profile

from ..helpers import login_user, logout_user, require_login
from ..helpers import verify_auth_token
from ..helpers import fill_users

from ..forms import SignupForm, SigninForm, SettingForm


__all__ = ('bp')

bp = Blueprint('account', __name__)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    next_url = request.args.get('next', url_for('.setting'))
    token = request.args.get('token')
    if token:
        user = verify_auth_token(token, 1)
        if not user:
            flash('Invalid or expired token.', 'error')
            return redirect(next_url)
        user.role = 'user'
        user.save()
        login_user(user)
        flash('Your account is verified successfully', 'success')
        return redirect(next_url)

    form = SignupForm()
    if form.validate_on_submit():
        veriy_email = current_app.config.get('VERIFY_EMAIL', False)
        if not veriy_email:
            user = form.save('user')
            login_user(user)
            return jsonify({'stat': 'ok'})

        #do some email verify
    if request.headers.get('X-Requested-With'):
        html = render_template('account/signup.html', form=form)
        return jsonify({'stat': 'fail', 'data': html})
    return render_template('index.html')


@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    next_url = request.args.get('next', '/')
    if g.user:
        return redirect(next_url)
    form = SigninForm()
    if form.validate_on_submit():
        login_user(form.user, form.permanent.data)
        return jsonify({'stat': 'ok'})
    if request.headers.get('X-Requested-With'):
        html = render_template('account/signin.html', form=form)
        return jsonify({'stat': 'fail', 'data': html})
    return render_template('index.html')


@bp.route('/signout', methods=['POST'])
def signout():
    next_url = request.args.get('next', '/')
    logout_user()
    return redirect(next_url)


@bp.route('/setting', methods=['GET', 'POST'])
@require_login
def setting():
    user = g.user
    profile = Profile.get_or_create(user.id)

    form = SettingForm(obj=profile)
    next_url = request.args.get('next', url_for('.setting'))
    if form.validate_on_submit():
        form.populate_obj(profile)
        profile.save()
        return jsonify({'stat': 'ok', 'data': message})

    if request.headers.get('X-Requested-With'):
        html = render_template('account/setting.html', form=form)
        return jsonify({'stat': 'ok', 'data': html})
    return render_template('index.html')


@bp.route('/', methods=['GET'])
def home():
    count = request.args.get('count', 10)
    page = int(request.args.get('page', 0))
    offset = page * count
    users = fill_users(Account.query.offset(offset).limit(count))
    if request.headers.get('X-Requested-With'):
        return jsonify({
            'stat': 'ok',
            'data': users
        })

    return render_template('index.html')
