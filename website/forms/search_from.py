# forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    circle = SelectField('Circle', 
                            choices=[("",'Select Circle'),('nhq', 'NHQ'), ('noida', 'Noida'),('gurugram','Gurugram'),('pune','Pune'),('banglore','Banglore'),('hydrabad','Hydrabad'),
                                     ('chennai','Chennai'),('kolkata','Kolkata')],
                              validators=[DataRequired()])
    emp_type = SelectField('Employee Type', 
                            choices=[("",'Select Employee Type'),('admin', 'Admin'),('hr','Human Resource'),('finance','Account'), ('employee', 'Employee'),('it_department', 'IT Department')],
                              validators=[DataRequired()])
    submit = SubmitField('Search')



class DetailForm(FlaskForm):
    user = SelectField('User', choices=[], coerce=int)
    detail_type = SelectField('Detail Type', choices=[
        ('family', 'Family Details'),
        ('emp_details','Employee details'),
        ('document','Document'),
        ('leave_bal','Leave Balance'),
        ('previous_company', 'Previous Company'),
        ('education', 'Education'),
        ('attendance', 'Attendance'),
        ('manager_contact', 'Manager Contact')
    ])
    submit = SubmitField('View Details')