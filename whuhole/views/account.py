from flask import Blueprint
from flask import redirect
from flask import render_template

from ..forms import RegisterForm
from ..forms import LoginForm

from ..models import Account
from ..models import Profile

from ..helpers import login_user
from ..helpers import logout_user


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
