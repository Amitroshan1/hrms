from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from website import login_manager
from datetime import datetime


class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    

    # OAuth2-specific fields
    oauth_provider = db.Column(db.String(50), nullable=False, default='microsoft')
    oauth_id = db.Column(db.String(255), unique=True, nullable=False)  # Stores the unique Microsoft ID
    oauth_token = db.Column(db.Text, nullable=True)  # Access token
    oauth_refresh_token = db.Column(db.Text, nullable=True)  # Refresh token
    oauth_token_expiry = db.Column(db.DateTime, nullable=True)  # Token expiration time

   



   

    employee_details = db.relationship('Employee', back_populates='admin', uselist=False, cascade="all, delete-orphan")
    family_details = db.relationship('FamilyDetails', back_populates='admin', cascade="all, delete-orphan")
    previous_companies = db.relationship('PreviousCompany', back_populates='admin', lazy=True, cascade="all, delete-orphan")
    education_details = db.relationship('Education', back_populates='admin', lazy='dynamic', cascade="all, delete-orphan")
    document_details = db.relationship('UploadDoc', back_populates='admin', lazy='dynamic', cascade="all, delete-orphan")
    leave_applications = db.relationship('LeaveApplication', back_populates='admin', lazy='dynamic', cascade="all, delete-orphan")
    punch_records = db.relationship('Punch', back_populates='admin', lazy='dynamic', cascade="all, delete-orphan")
    assets = db.relationship('Asset', back_populates='admin', cascade="all, delete-orphan")
    payslips = db.relationship('PaySlip', back_populates='admin', cascade="all, delete-orphan")
    queries = db.relationship('Query', back_populates='admin', cascade="all, delete-orphan")
    query_replies = db.relationship('QueryReply', back_populates='admin', cascade="all, delete-orphan")
    # sessions = db.relationship('Session', back_populates='admin', cascade="all, delete-orphan")


    
     # Check if the OAuth2 token is valid
    def is_oauth_token_valid(self):
        return self.oauth_token_expiry and self.oauth_token_expiry > datetime.now()
    


@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))

