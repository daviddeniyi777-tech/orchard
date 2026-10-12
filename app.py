import os

from flask import Flask
from dotenv import load_dotenv



from extensions import db, login_manager, migrate

from models import User

from routes.main import main
from routes.auth import auth
from routes.admin import admin
from routes.product import product
from routes.stores import store
from config import ALLOWED_EXTENSIONS, RESEND_FROM_EMAIL, UPLOAD_FOLDER

load_dotenv()

app = Flask(__name__)


# =========================================================
# CONFIGURATION
# =========================================================
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

app.config["SECRET_KEY"] = "gggegeggegeshshshshsjajajjsjshdggegehdnndndbeb"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orchard.db"

app.config["RESEND_API_KEY"] = os.getenv("RESEND_API_KEY")

app.config["RESEND_FROM_EMAIL"] = (
    os.getenv("RESEND_FROM_EMAIL") or RESEND_FROM_EMAIL
)


# =========================================================
# INITIALIZE EXTENSIONS
# =========================================================

db.init_app(app)

login_manager.init_app(app)

migrate.init_app(app, db)


# =========================================================
# REGISTER BLUEPRINTS
# =========================================================

app.register_blueprint(main)

app.register_blueprint(auth)

app.register_blueprint(admin)
app.register_blueprint(product)
app.register_blueprint(store)


# =========================================================
# LOGIN USER LOADER
# =========================================================

@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)