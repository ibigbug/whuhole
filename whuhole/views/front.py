from flask import Blueprint
from flask import render_template

from ..models import Topic


bp = Blueprint('front', __name__)


@bp.route('/', methods=['GET'])
def index():
    topics = Topic.query.all()
    return render_template('front/index.html', topics=topics)
