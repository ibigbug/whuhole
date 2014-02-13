# coding: utf-8

from flask import Blueprint
from flask import request
from flask import g
from flask import flash
from flask import redirect

from ..models import Topic

from ..helpers import login_required
from ..helpers import update_user

bp = Blueprint('topic', __name__)


@bp.route('/update', methods=["POST"])
@login_required
@update_user
def update():
    topic_content = request.form['topic']
    topic = Topic()
    topic.content = topic_content
    topic.account_id = g.user.id
    topic.save()

    flash(u'发布成功', 'success')
    return redirect('/')
