from flask import Flask
from flask_cors import CORS
from blueprint.track_bp import track_bp
from blueprint.register_bp import register_bp
from blueprint.login_bp import login_bp
from blueprint.logout_bp import logout_bp
from blueprint.subscriptions_bp import subscriptions_bp
from blueprint.callback_bp import callback_bp
from blueprint.check_login_bp import check_login_bp
from blueprint.tracked_product_bp import tracked_product_bp
from blueprint.remove_tracked_product_bp import remove_product_bp
from blueprint.webhook_bp import webhook_bp
from blueprint.cancel_subscription_bp import cancel_subscription_bp
from blueprint.check_subscription_status import check_subscription_status_bp
import os
from dotenv import load_dotenv
from datetime import timedelta
from utils.start_tracking import schedule_tracking
from threading import Thread

# Load the .env file
load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')

# Set the session expiration time globally
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=5)  # 5 days

app.config['SESSION_COOKIE_SECURE'] = True  # Use True if using HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Allow cross-origin cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Protect cookies from being accessed via JavaScript

# Register blueprint
app.register_blueprint(track_bp)
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(subscriptions_bp)
app.register_blueprint(callback_bp)
app.register_blueprint(check_login_bp)
app.register_blueprint(tracked_product_bp)
app.register_blueprint(remove_product_bp)
app.register_blueprint(webhook_bp)
app.register_blueprint(cancel_subscription_bp)
app.register_blueprint(check_subscription_status_bp)

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') == 'production' and os.getenv('RUN_MAIN') == 'true':
        schedule_thread = Thread(target=schedule_tracking, daemon=True)
        schedule_thread.start()
    app.run()
