from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from datetime import datetime,timedelta
from flask_wtf.csrf import CSRFProtect
from flask_apscheduler import APScheduler
from urllib.parse import urlparse, urljoin
import datetime
from authlib.integrations.flask_client import OAuth
from datetime import timedelta, datetime
from pytz import timezone
import logging
import os
from flask_session import Session 
from dotenv import load_dotenv




dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

# Initialize extensions
oauth = OAuth()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()
csrf = CSRFProtect()
scheduler = APScheduler()
Session = Session()


class Config:
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=50)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target)) 
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def update_leave_balances():
    """ Updates leave balances for employees every 6 months. """
    from .models.attendance import LeaveBalance
    from .models.Admin_models import Admin  
    from .models.signup import Signup 

    with scheduler.app.app_context():
        leave_balances = LeaveBalance.query.all() # relationship with Signup
        if not leave_balances:
            print("No leave balances found in the database.")
            return

        for balance in leave_balances:
            admin = Admin.query.filter_by(id=balance.admin_id).first()
            signup = Signup.query.filter_by(email=admin.email).first()
            if admin and signup.Doj:
                doj = signup.Doj
                six_months_after_doj = doj + timedelta(days=6*30) 
                
                if datetime.now().date() >= six_months_after_doj:
                    balance.privilege_leave_balance += 1.08
                    balance.casual_leave_balance += 0.67

        try:
            db.session.commit()
            print("Database commit successful.")
        except Exception as e:
            print(f"Database commit failed: {str(e)}")



from datetime import datetime, timedelta
import pytz

def send_reminder_emails():
    from .models.query import Query
    from .common import verify_oauth2_and_send_email
    
    print("Reminder email function started")

    # IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    with scheduler.app.app_context():
        # Get all open queries
        queries = Query.query.filter_by(status='open').all()
        print(f"Found {len(queries)} open queries")

        for query in queries:
            # Make sure query.created_at is timezone-aware in IST
            if query.created_at.tzinfo is None:
                last_activity_time = ist.localize(query.created_at)
            else:
                last_activity_time = query.created_at.astimezone(ist)

            # Calculate time since last activity (query creation or reply)
            time_since_last_activity = now - last_activity_time
            print(f"Query ID {query.id} age since last activity: {time_since_last_activity}")

            # If 3 days or more have passed since last activity, send reminder
            if time_since_last_activity >= timedelta(days=3):
                departments = query.emp_type.split(', ')
                print(f"Reminder needed for query: {query.title}, Departments: {departments}")

                # Assign department email (example)
                if 'Human Resource' in departments:
                    department_email = 'skchaugule@saffotech.com'
                elif 'Accounts' in departments:
                    department_email = 'skchaugule@saffotech.com'
                elif 'IT Department' in departments:
                    department_email = 'skchaugule@saffotech.com'
                else:
                    department_email = 'skchaugule@saffotech.com'

                cc = ['chauguleshubham390@gmail.com']

                admin_email = query.admin.email
                print(f"Sending reminder from admin email: {admin_email}")

                subject = f"Reminder: No response to query '{query.title}' in 3 days"
                body = f"""
                Query Title: {query.title}
                Department(s): {query.emp_type}
                Last Activity At: {last_activity_time.strftime('%Y-%m-%d %H:%M:%S')}
                
                This query has not received any reply or update within 3 days. Please respond ASAP.
                """

                verify_oauth2_and_send_email(admin_email, subject, body, department_email, cc)



def leave_reminder_email():
    from .models.attendance import LeaveApplication
    from .models.Admin_models import Admin
    from .models.signup import Signup
    from .models.manager_model import ManagerContact
    from .common import verify_oauth2_and_send_email

    print("Reminder function started...")

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    with scheduler.app.app_context():
        leaves = LeaveApplication.query.filter_by(status="Pending").all()
        print(f"Found {len(leaves)} leaves..")
        for leave in leaves:

            if leave.created_at.tzinfo is None:
                last_activity_query_time = ist.localize(leave.created_at)
            else:
                last_activity_query_time = leave.created_at.astimezone(ist) #when qyery is create that time will store

            time_since_last_query_activity = now - last_activity_query_time
            print(f"The leave_app id is {leave.id} and age since last activity: {time_since_last_query_activity}")
            if time_since_last_query_activity >= timedelta(days=3):
                user_email = leave.admin.email
                print(f"successful get the user email {user_email}")
                signup_data = Signup.query.filter_by(email=user_email).first()
                # print(f"Successful got the signup data {signup_data}")
                if signup_data:
                    emp_type = signup_data.emp_type
                    circle = signup_data.circle
                    print(f"Employee Type: {emp_type}")
                    print(f"Circle: {circle}")
                else:
                    print("No signup data found.")
                    emp_type = None
                    circle = None
                manager_data = ManagerContact.query.filter_by(circle_name = circle,user_type=emp_type,).first()
                if manager_data:
                    l2_leader = manager_data.l2_email
                    l3_leader = manager_data.l3_email
                    print(f"Get the data of l2 {l2_leader}")
                    print(f"Get the data of l3 {l3_leader}")

                cc = l2_leader
                subject = f"Reminder: No response to leave application ' in 3 days"
                body = f"""
                Hello,

                This is a reminder that a leave application has been pending without any response or update for the past 3 days.

                Timely action on such requests ensures smooth workflow and employesatisfaction. Please review and take the necessary action as soon as possible.

                If you have already addressed this, kindly ignore this message.

                Thank you,
                HR & Admin Team
                """
                verify_oauth2_and_send_email(user_email, subject, body, l3_leader, [cc])
                print("TO:", user_email)
                print("CC:", cc)
                print("BCC:", l3_leader)
                print("Subject :", subject)
                print("Successful get the body structure Body: ", body)


                
                











def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")

# Check if critical env variables are set
    if not app.config['SECRET_KEY'] or not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("Missing required environment variables. Check your .env file.")


# ✅ Flask-Session Configuration (MySQL)
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'session'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True  # Secure the session cookies
    app.config['SESSION_KEY_PREFIX'] = 'saffo_session_'
    app.config['SESSION_SERIALIZATION_FORMAT'] = "json"



    
  
    # OAuth2 Configuration
    app.config['SESSION_COOKIE_SECURE'] = True  
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    app.config['OAUTH2_CLIENT_ID'] = os.getenv("OAUTH2_CLIENT_ID")
    app.config['OAUTH2_CLIENT_SECRET'] = os.getenv("OAUTH2_CLIENT_SECRET")
    app.config['OAUTH2_REDIRECT_URI'] = os.getenv("OAUTH2_REDIRECT_URI")
    app.config['OAUTH2_SCOPE'] = [
        "openid", "email", "profile", "offline_access",
        "https://graph.microsoft.com/mail.send",
        "https://graph.microsoft.com/User.Read"
    ]
    # Ensure required env variables are set
    if not all([app.config['OAUTH2_CLIENT_ID'], app.config['OAUTH2_CLIENT_SECRET'], app.config['OAUTH2_REDIRECT_URI']]):
        raise ValueError("Missing OAuth2 environment variables. Please check your .env file.")


    # ✅ Fix OAuth URLs
    app.config['MICROSOFT_AUTH_URL'] = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    app.config['MICROSOFT_TOKEN_URL'] = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    app.config['MICROSOFT_USER_INFO_URL'] = "https://graph.microsoft.com/v1.0/me"

    # Additional configurations
    app.config['UPLOAD_FOLDER'] = 'website/static/uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'png', 'jpeg', 'pdf', 'txt', 'doc', 'docx', 'xls', 'xlsx', 'jfif'}
    app.config['WTF_CSRF_ENABLED'] = True

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    scheduler.init_app(app)
    Session.init_app(app)


    # Import models before initializing migrate
    from .models.Admin_models import Admin
    from .models.emp_detail_models import Employee
    from .models.family_models import FamilyDetails
    from .models.prev_com import PreviousCompany
    from .models.education import UploadDoc, Education
    from .models.attendance import Punch, LeaveBalance, LeaveApplication
    from .models.manager_model import ManagerContact
    from .models.query import Query, QueryReply
    from .models.signup import Signup
    from .models.news_feed import NewsFeed, PaySlip

    migrate.init_app(app, db)  # Now models are loaded, safe to initialize

    with app.app_context():
        db.create_all()

    # Initialize OAuth with the app
    oauth.init_app(app)

    # ✅ Fix OAuth registration
    oauth.register(
        name='microsoft',
        client_id=app.config['OAUTH2_CLIENT_ID'],
        client_secret=app.config['OAUTH2_CLIENT_SECRET'],
        access_token_url=app.config['MICROSOFT_TOKEN_URL'],
        authorize_url=app.config['MICROSOFT_AUTH_URL'],
        client_kwargs={'scope': " ".join(app.config['OAUTH2_SCOPE'])}
    )

    # Register blueprints
    from .views import views
    from .auth import auth
    from .Amdin_auth import Admin_auth
    from .profile import profile
    from .hr import hr
    from .Updatemanager import manager_bp
    from .Aoocunts import Accounts
    from .auth_helper import auth_helper

    app.register_blueprint(profile, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(Admin_auth, url_prefix='/')
    app.register_blueprint(hr, url_prefix='/')
    app.register_blueprint(manager_bp, url_prefix='/')
    app.register_blueprint(Accounts, url_prefix='/')
    app.register_blueprint(auth_helper, url_prefix='/')

    # Scheduler job
    scheduler.add_job(
    id='update_leave_balances',
    func=update_leave_balances,
    trigger='cron',
    day='25-31',      # Runs only between the 25th and 31st
    hour=17,
    minute=55,
    day_of_week='mon' # Ensures it runs only on Mondays
)
    scheduler.add_job(
    id='send_reminder_emails_job',
    func=send_reminder_emails,  # your function name here
    trigger='interval',
    days = 3 # runs every day; adjust as needed
)
    
    scheduler.add_job(
    id='leave_reminder_email()',
    func=leave_reminder_email,  # your function name here
    trigger='interval',
    days = 3 # runs every day; adjust as needed
)





    # After request hook to set cache control
    @app.after_request
    def add_header(response):
        response.cache_control.no_store = True
        return response

    # Start scheduler
    scheduler.start()

    return app

# ✅ Fix logging setup
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Flask application initialized successfully")