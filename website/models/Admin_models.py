from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from website import login_manager


class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'


    id= db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120),unique=True)
    password = db.Column(db.String(150),nullable=False)
    first_name= db.Column(db.String(150),nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)  
    emp_id = db.Column(db.String(10), unique=True, nullable=False)
    Emp_type = db.Column(db.String(50), nullable=False, default='employee')

    employee_details = db.relationship('Employee', back_populates='admin', uselist=False)

    

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_admin(admin_id):
    return Admin.query.get(int(admin_id))
