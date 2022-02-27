import argparse
import os
from flask import Flask, jsonify, make_response, Blueprint
from flask_cors import CORS
from routes import request_api


APP = Flask(__name__)

APP_BLUEPRINT = Blueprint('app', __name__, url_prefix='/')
APP.register_blueprint(APP_BLUEPRINT)

APP.register_blueprint(request_api.get_blueprint())


@APP.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({'error': 'Server error'}), 500)


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description='Chainlink-Python-Flask-API'
    )
    PARSER.add_argument('--debug', action='store_true',
                        help='Use flask debug/dev mode with file change reloading')

    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 5000))

    if ARGS.debug:
        print("Running in debug mode")
        CORS = CORS(APP)
        APP.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        APP.run(host='0.0.0.0', port=PORT, debug=False)

    pass
