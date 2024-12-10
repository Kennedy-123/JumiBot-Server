from flask import Flask
from flask_cors import CORS
from blueprint.track_bp import track_bp
app = Flask(__name__)
CORS(app)

# Register blueprint
app.register_blueprint(track_bp)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
