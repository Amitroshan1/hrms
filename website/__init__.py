from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
DB_NAME = 'saffo_db'
csrf = CSRFProtect()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9abf5dc987d54727823bcbf_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mysql_1234@localhost/saffo_db'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['UPLOAD_FOLDER'] = 'website\\static\\uploads'
    app.config['SESSION_PERMANENT'] = True
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    app.config['WTF_CSRF_ENABLED'] = True

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    

    
    login_manager.login_view='Admin_auth.A_homepage'
    login_manager.login_message_category = 'info'

    from .views import views
    from .auth import auth
    from .Amdin_auth import Admin_auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Admin_auth, url_prefix='/')

    from .models.Admin_models import Admin
    from .models.emp_detail_models import Employee

    with app.app_context():
        db.create_all()

    return app
