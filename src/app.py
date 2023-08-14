from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from config import config
from database import db
from routes import Auth

app = Flask(__name__)
app.config.from_object(config['development'])

bcrypt = Bcrypt(app)
mail = Mail(app)
jwt = JWTManager(app)

if __name__ == '__main__':
    # database connection
    with app.app_context():
        db.init_app(app)
        # db.drop_all()
        db.create_all()

    # register
    app.register_blueprint(Auth.blueprint, url_prefix='/v1/api/auth')    

    app.run()