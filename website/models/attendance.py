from .. import db
from flask_login import UserMixin


class Punch(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    punch_date = db.Column(db.Date, nullable=False)
    punch_in = db.Column(db.Time, nullable=True)
    punch_out = db.Column(db.Time, nullable=True)
    is_holiday = db.Column(db.Boolean, default=False)  
    
    admin = db.relationship('Admin', back_populates='punch_records')




class LeaveBalance(db.Model):
    __tablename__ = 'leave_balances'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    personal_leave_balance = db.Column(db.Float, default=0.0)
    casual_leave_balance = db.Column(db.Float, default=0.0)
    comp_off_balance = db.Column(db.Float, default=0.0)

    admin = db.relationship('Admin', back_populates='leave_balance')

    

class LeaveApplication(db.Model):
    __tablename__ = 'leave_applications'

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    leave_type = db.Column(db.String(50), nullable=False)
    leave_days = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='Pending')

    admin = db.relationship('Admin', back_populates='leave_applications')

