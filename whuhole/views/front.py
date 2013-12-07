from flask import Blueprint
from flask import request, g
from flask import render_template, jsonify

from ..forms import StatusForm

__all__ = ['bp']

bp = Blueprint('from', __name__)


@bp.route('/')
def home(view=None):
    form = StatusForm()
    if request.headers.get('X-Requested-With'):
        if g.user:
            html = render_template('snippets/status-form.html', form=form)
        else:
            return render_template('snippets/welcome.html')
        return jsonify({'stat': 'ok', 'data': html})
    return render_template('index.html')
