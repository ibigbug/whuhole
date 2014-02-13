from flask import Blueprint
from flask import request
from flask import render_template
from flask import g

from ..models import Topic
from ..models import Account

from ..forms import ProfileForm


bp = Blueprint('front', __name__)


@bp.route('/', methods=['GET'])
def index():
    topics = Topic.query.order_by('created desc').all()
    if g.user:
        liked_id_list = [like.topic_id for like in g.user.like.all()]
    else:
        liked_id_list = []
    return render_template('front/index.html', topics=topics,
                           liked_id_list=liked_id_list)


@bp.route('/users', defaults=dict(page=1))
@bp.route('/users/page/<int:page>')
def user_list(page):
    pagination = Account.query.order_by('updated desc').paginate(page)
    return render_template('front/user-list.html', pagination=pagination)


@bp.route('/users/<int:user_id>')
def user_profile(user_id):
    user = Account.query.filter_by(id=user_id).first_or_404()
    form = ProfileForm(obj=user.profile)
    return render_template('front/user-profile.html', user=user,form=form)
