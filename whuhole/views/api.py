from flask import Blueprint
from flask import request

from ..models import Topic

bp = Blueprint('api', __name__)

@bp.route('/topic/latest')
def topic_by_time():
    pass


@bp.route('/user/latest')
def user_by_time():
    pass
