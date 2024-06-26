from .login import logins
from .stuff import stuffs

def register_blueprints(app):
    app.register_blueprint(logins)
    app.register_blueprint(stuffs)