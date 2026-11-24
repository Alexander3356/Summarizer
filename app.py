
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import Config
from models.conn import db
from models.model import Summary, User
from modules.auth import get_current_user

from blueprints.frontend import frontend_bp
from blueprints.api import api_bp



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db)

    csrf = CSRFProtect(app)
    csrf.exempt(api_bp)

    app.register_blueprint(frontend_bp)
    app.register_blueprint(api_bp)

    @app.context_processor
    def inject_globals():
        return {'current_user': get_current_user()}

    @app.errorhandler(404)
    def not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
