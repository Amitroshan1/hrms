from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from flask_apscheduler import APScheduler
from urllib.parse import urlparse, urljoin
import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
scheduler = APScheduler()

class Config:
    SCHEDULER_API_ENABLED = True

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mysql_1234@localhost/saffo_db'
    app.config['MAIL_SERVER'] = 'smtp.office365.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_email@example.com'
    app.config['MAIL_PASSWORD'] = 'your_password'
    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg', 'pdf', 'txt', 'doc', 'docx', 'xls', 'xlsx'}
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
    scheduler.init_app(app)

    # Register your blueprints here
    from .views import views
    from .auth import auth
    from .Amdin_auth import Admin_auth
    from .profile import profile
    from .finance import finance
    from .hr import hr
    from .Updatemanager import manager_bp

    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Admin_auth, url_prefix='/')
    app.register_blueprint(finance, url_prefix='/')
    app.register_blueprint(hr, url_prefix='/')
    app.register_blueprint(manager_bp, url_prefix='/')

    
    from .models.Admin_models import Admin
    from .models.emp_detail_models import Employee
    from .models.family_models import FamilyDetails
    from .models.prev_com import PreviousCompany
    from .models.education import UploadDoc, Education
    from .models.attendance import Punch, LeaveBalance, LeaveApplication
    from .models.manager_model import ManagerContact
    with app.app_context():
        db.create_all()

        # Configure the scheduled job here
    scheduler.add_job(id='update_leave_balances', func=update_leave_balances, trigger='cron', day=3, hour=0, minute=0)

    @app.after_request
    def add_header(response):
        response.cache_control.no_store = True
        return response

    scheduler.start()

    return app

def update_leave_balances():
    from .models.attendance import LeaveBalance
    leave_balances = LeaveBalance.query.all()
    for balance in leave_balances:
        balance.personal_leave_balance += 1
        balance.casual_leave_balance += 0.75
    db.session.commit()
    print(f"Leave balances updated at {datetime.datetime.now()}")

