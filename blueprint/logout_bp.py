from flask import jsonify, Blueprint, session

logout_bp = Blueprint('logout', __name__, url_prefix='/logout-user')


@logout_bp.route('/', methods=['POST'])
def logout_user():
    try:
        # Clear the session data
        session.clear()

        # Optionally, you can return a success response
        return jsonify({'success': True, 'message': 'Logged out successfully'}), 200
    except Exception as e:
        # Handle any errors during logout
        return jsonify({'success': False, 'message': str(e)}), 500
