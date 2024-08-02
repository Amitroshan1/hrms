from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from website import login_manager


class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    emp_id = db.Column(db.String(10), unique=True, nullable=False)
    Emp_type = db.Column(db.String(50), nullable=False, default='employee')
    circle=db.Column(db.String(50), nullable=False, default=None)
    
    
    employee_details = db.relationship('Employee', back_populates='admin', uselist=False)
    family_details = db.relationship('FamilyDetails', back_populates='admin', cascade="all, delete-orphan")
    previous_companies = db.relationship('PreviousCompany', back_populates='admin', lazy=True)
    education_details = db.relationship('Education', back_populates='admin', lazy='dynamic')
    document_details = db.relationship('UploadDoc', back_populates='admin', lazy='dynamic')
    leave_balance = db.relationship('LeaveBalance', back_populates='admin', uselist=False)
    leave_applications = db.relationship('LeaveApplication', back_populates='admin', lazy='dynamic')

    punch_records = db.relationship('Punch', back_populates='admin', lazy='dynamic')


    

    

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))
