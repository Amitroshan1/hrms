
from wtforms import SubmitField
from flask_wtf import FlaskForm
from wtforms import  DateField,  DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange



class PunchForm(FlaskForm):
    punch_in = SubmitField('Punch In')
    punch_out = SubmitField('Punch Out')




class LeaveForm(FlaskForm):
    personal_leave_days = DecimalField('Personal Leave ', places=1, validators=[NumberRange(min=0.5, max=13.0)], default=0)
    casual_leave_days = DecimalField('Casual Leave ', places=1, validators=[NumberRange(min=0.5, max=8.0)], default=0)
    comp_off_leave = DecimalField('Optional Leave ', places=1, validators=[NumberRange(min=0.5, max=2)], default=0)
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Apply for Leave')

    
