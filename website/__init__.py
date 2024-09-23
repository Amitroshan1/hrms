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
    app.config['SECRET_KEY'] = 'ajsgfkjsgfkgsdfkgsdajsbfjkkjhbh'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:saffodev2024@localhost/saffo_production'

    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'yourmailoutlook.com'
    app.config['MAIL_PASSWORD'] = 'amitskdh'
    app.config['MAIL_DEFAULT_SENDER'] = 'yourmailoutlook.com'
    

    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg', 'pdf', 'txt', 'doc', 'docx', 'xls', 'xlsx','jfif'}
    app.config['SESSION_PERMANENT'] = True
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
    app.config['WTF_CSRF_ENABLED'] = True

    mail.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    scheduler.init_app(app)

   
    from .views import views
    from .auth import auth
    from .Amdin_auth import Admin_auth
    from .profile import profile

    from .hr import hr
    from .Updatemanager import manager_bp
    from .Aoocunts import Accounts

    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Admin_auth, url_prefix='/')
    
    app.register_blueprint(hr, url_prefix='/')
    app.register_blueprint(manager_bp, url_prefix='/')
    app.register_blueprint(Accounts, url_prefix='/')

    from .models.Admin_models import Admin
    from .models.emp_detail_models import Employee
    from .models.family_models import FamilyDetails
    from .models.prev_com import PreviousCompany
    from .models.education import UploadDoc, Education
    from .models.attendance import Punch, LeaveBalance, LeaveApplication
    from .models.manager_model import ManagerContact
    from .models.query import Query,QueryReply

    with app.app_context():
        db.create_all()

        
        scheduler.add_job(id='update_leave_balances', func=update_leave_balances, trigger='cron', hour=17, minute=55)

    @app.after_request
    def add_header(response):
        response.cache_control.no_store = True
        return response

    scheduler.start()

    return app

def update_leave_balances():
    from .models.attendance import LeaveBalance
    from .models.Admin_models import Admin  

    with scheduler.app.app_context():
        leave_balances = LeaveBalance.query.all()

        if not leave_balances:
            print("No leave balances found in the database.")

        for balance in leave_balances:
            admin = Admin.query.filter_by(id=balance.admin_id).first() 
            if admin and admin.Doj:
                doj = admin.Doj
                six_months_after_doj = doj + timedelta(days=6*30) 
                
                if datetime.datetime.now().date() >= six_months_after_doj:
                    balance.privilege_leave_balance += 1.08
                    balance.casual_leave_balance += 0.67

        try:
            db.session.commit()
            print("Database commit successful.")
        except Exception as e:
            print(f"Database commit failed: {str(e)}")


