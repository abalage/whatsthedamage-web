from flask import Flask
from routes import bp as main_bp
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the secret key to a random value
app.secret_key = os.urandom(24)

app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run(debug=True)
