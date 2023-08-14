from flask import Blueprint
from controllers.Auth import AuthController

blueprint = Blueprint('auth_blueprint', __name__)

blueprint.route('/signup', methods=['POST'])(AuthController().signup)
blueprint.route('/signin', methods=['POST'])(AuthController().signin)
blueprint.route('/code', methods=['GET'])(AuthController().send_code)
blueprint.route('/refresh', methods=['GET'])(AuthController().refresh)