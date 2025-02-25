from flask import Flask
from routes import bp as main_bp
import os

app: Flask = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

# Set the secret key to a random value
app.secret_key = os.urandom(24)

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
