from flask import Flask
from .config import Config

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)

    from .models import db

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)
    return app

app = create_app()

if __name__ == "__main__":
    db.create_all()
    app.run()