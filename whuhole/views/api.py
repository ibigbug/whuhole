from flask import BluePrint

from ..models import topic

bp = BluePrint(__name__)

@bp.route('/topic/add', methods=['PUT'])
def topic_add():
    pass
