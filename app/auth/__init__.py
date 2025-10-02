# ruff: noqa: E402
#explicitly ignoring 'Module level import not at top of file' to avoid circular imports 


from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes as routes