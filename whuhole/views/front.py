from flask import Blueprint
from flask import render_template
from flask import g

from ..models import Topic


bp = Blueprint('front', __name__)


@bp.route('/', methods=['GET'])
def index():
    topics = Topic.query.all()
    liked_id_list = [like.topic_id for like in g.user.like.all()]
    return render_template('front/index.html', topics=topics,
                           liked_id_list=liked_id_list)
