from flask import Blueprint
from flask import current_app

module = Blueprint('search', __name__)


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
