from flask import Blueprint
from flask import render_template


bp = Blueprint('front', __name__)


@bp.route('/', methods=['GET'])
def home_page():
    return render_template('front/index.html')
