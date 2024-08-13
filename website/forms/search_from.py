# forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    circle = SelectField('Circle', 
                            choices=[("",'Select Circle'),('nhq', 'NHQ'),('punjab', 'Punjab'),('haryana', 'Haryana'),('noida', 'Noida'),('gurugram','Gurugram'),('pune','Pune'),('banglore','Banglore'),('hydrabad','Hydrabad'),
                                     ('chennai','Chennai'),('kolkata','Kolkata')],
                              validators=[DataRequired()])
    emp_type = SelectField('Employee Type', 
                            choices=[("",'Select Employee Type'),('hr','Human Resource'),('finance','Account & Finanace'), ('employee', 'Software'),('it_department', 'IT Department')],
                              validators=[DataRequired()])
    submit = SubmitField('Search')



class DetailForm(FlaskForm):
    user = SelectField('User', choices=[], coerce=int)
    detail_type = SelectField('Detail Type', choices=[
        
        ('family', 'Family Details'),
        ('emp_details','Employee details'),
        ('document','Document'),
       
        ('previous_company', 'Previous Company'),
        ('education', 'Education'),
        ('attendance', 'Attendance')
        
    ])
    submit = SubmitField('View Details')