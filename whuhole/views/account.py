#coding: utf-8

from flask import Blueprint
from flask import redirect
from flask import request
from flask import g
from flask import flash
from flask import render_template

from ..forms import RegisterForm
from ..forms import LoginForm
from ..forms import ProfileForm

from ..models import Account
from ..models import Profile

from ..helpers import login_user
from ..helpers import logout_user
from ..helpers import login_required


bp = Blueprint('account', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = Account()
        form.populate_obj(user)
        user.set_password()
        user.profile = Profile()
        user.profile.save()
        user.save()

        login_user(user)

        profile = Profile()  # create a profile for the new user
        profile.save()

        return redirect('/')

    return render_template('account/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    next_url = '/'
    form = LoginForm()

    if form.validate_on_submit():
        login_user(form.user)
        return redirect(next_url)

    return render_template('account/login.html', form=form)


@bp.route('/logout', methods=['POST'])
def logout():
    next_url = '/'
    logout_user()
    return redirect(next_url)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    next_url = request.url
    profile = g.user.profile
    form = ProfileForm(obj=profile)
    if form.validate_on_submit():
        form.populate_obj(profile)
        profile.save()
        flash(u'更新成功', 'success')
        return redirect(next_url)

    return render_template('account/profile.html', form=form)
