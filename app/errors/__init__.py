# ruff: noqa: E402
#explicitly ignoring 'Module level import not at top of file' to avoid circular imports 


from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers as handlers