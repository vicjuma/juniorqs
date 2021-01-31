from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user,logout_user
from app.errors import error

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)
app.register_blueprint(error, url_prefix='/error')

# formula for calculation should be added here
@app.template_filter('convert')
def convert_usd(number):
    return int(number / 108.75)

from app import routes
