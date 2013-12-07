from flask import Blueprint
from flask import request
from flask import jsonify, render_template

from ..forms import StatusForm
from ..models import Status, StatusLike

from ..helpers import require_login
from ..helpers import fill_statuses


__all__ = ['bp']

bp = Blueprint('hole', __name__)


@bp.route('/', methods=['GET'])
def index():
    if request.headers.get('X-Requested-With'):
        count = request.args.get('count', 10)
        page = int(request.args.get('page', 1))
        offset = page * count
        statuses = Status.query.order_by(
            Status.created.desc()).offset(offset).limit(count)
        statuses = fill_statuses(statuses)
        return jsonify({
            'stat': 'ok',
            'data': statuses
        })

    return render_template('index.html')


@bp.route('/', methods=['POST'])
@require_login
def post():
    form = StatusForm()
    if form.validate_on_submit():
        status = form.save()
        return jsonify({
            'stat': 'ok',
            'data': status.to_dict('id', 'content')
        })
    return jsonify({'stat': 'fail', 'data': form.errors})

@bp.route('/like/<int:status_id>', methods=['POST'])
@require_login
def like():
    like = StatusLike.query.filter_by(
        account_id=g.user.id,
        status_id=status_id
    ).first()

    if like:
        like.delete()
    else:
        like = StatusLike()
        like.account_id = g.user.id
        like.status_id = status_id
        like.save()

    return jsonify({'stat': 'ok'})
