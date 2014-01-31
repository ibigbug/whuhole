from flask import Blueprint
from flask import request

from ..models import topic

bp = Blueprint('api', __name__)

@bp.route('/topic/add', methods=['GET', 'PUT'])
def topic_add():
    if request.method == 'GET':
        return 'aaa'
