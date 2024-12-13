from flask import Flask
from flask_cors import CORS
from blueprint.track_bp import track_bp
from blueprint.register_bp import register_bp
from blueprint.login_bp import login_bp
from blueprint.logout_bp import logout_bp
import os
from dotenv import load_dotenv
from datetime import timedelta

# Load the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')  # Required for session signing

# Set the session expiration time globally
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=432000)  # 5 days

# Register blueprint
app.register_blueprint(track_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
