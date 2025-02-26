from flask import Flask
import os
from routes import bp as main_bp


class AppConfig:
    UPLOAD_FOLDER: str = 'uploads'
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16 MB
    SECRET_KEY: bytes = os.urandom(24)


def create_app(config_class: None) -> Flask:
    app: Flask = Flask(__name__)

    # Load default configuration from a class
    app.config.from_object(AppConfig)

    if config_class:
        app.config.from_object(config_class)

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    app.register_blueprint(main_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
