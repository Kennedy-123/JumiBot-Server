from flask import Blueprint, jsonify

monitor = Blueprint('monitor', __name__)


@monitor.route('/ping', methods=['GET'])
def ping():
    print('checked')
    return jsonify({'message': 'Server is active'}), 200