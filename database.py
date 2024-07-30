from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """
    Inicialización de la aplicación.
    """
    db.init_app(app)


def config_db(app):
    """
    Configuración de la aplicación.
    """
    with app.app_context():
        db.create_all()

    @app.teardown_request
    def close_session(exception=None):
        """
        Cierra la conexión con de la DB luego de ejecutar la query.
        """
        db.session.close()
