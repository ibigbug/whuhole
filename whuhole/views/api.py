from flask import Blueprint
from flask import request
from flask import g
from flask import redirect
from flask import jsonify

from ..models import Reply

from ..helpers import login_required

bp = Blueprint('api', __name__)


@bp.route('/topic/latest')
def topic_by_time():
    pass


@bp.route('/user/latest')
def user_by_time():
    pass


@bp.route('/topic/<int:topic_id>/reply', methods=['POST'])
@login_required
def topic_reply(topic_id):
    reply = Reply()
    reply.content = request.form.get('reply')
    reply.account_id = g.user.id
    reply.topic_id = topic_id
    reply.save()
    reply.topic.reply_count += 1
    reply.topic.save()
    if request.is_xhr:
        return jsonify(stat='ok')
    return redirect('/')
