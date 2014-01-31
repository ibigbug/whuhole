from flask import Blueprint
from flask import request
from flask import redirect
from flask import render_template

from ..forms import RegisterForm

from ..models import Account


bp = Blueprint('account', __name__)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = Account()
        form.populate_obj(user)
        user.save()
        return redirect('/')

    return render_template('account/register.html', form=form)
