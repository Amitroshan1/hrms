# forms.py
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired,Optional

class SearchForm(FlaskForm):
    circle = SelectField('Circle', 
                            choices=[("",'Select Circle'),('nhq', 'NHQ'),('punjab', 'Punjab'),('haryana', 'Haryana'),('noida', 'Noida'),('gurugram','Gurugram'),('pune','Pune'),('banglore','Banglore'),('hydrabad','Hydrabad'),
                                     ('chennai','Chennai'),('kolkata','Kolkata')],
                              validators=[DataRequired()])
    emp_type = SelectField('Employee Type', 
                            choices=[("",'Select Employee Type'),('hr','Human Resource'),('finance','Accounts & Finanace'), ('employee', 'Software'),('it_department', 'IT Department')],
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





class NewsFeedForm(FlaskForm):
    circle = SelectField('Circle', 
                            choices=[("",'Select Circle'),('all','All'),('nhq', 'NHQ'),('punjab', 'Punjab'),('haryana', 'Haryana'),('noida', 'Noida'),('gurugram','Gurugram'),('pune','Pune'),('banglore','Banglore'),('hydrabad','Hydrabad'),
                                     ('chennai','Chennai'),('kolkata','Kolkata')],
                              validators=[DataRequired()])
    emp_type = SelectField('Employee Type', 
                            choices=[("",'Select Employee Type'),('all','All'),('hr','Human Resource'),('finance','Accounts & Finanace'), ('employee', 'Software'),('it_department', 'IT Department')],
                              validators=[DataRequired()])
    
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    file = FileField('File')
    submit = SubmitField('Post')


class SearchEmp_Id(FlaskForm):
    emp_id = StringField('Employee ID', validators=[DataRequired()])
    submit = SubmitField('Search')


class AssetForm(FlaskForm):
    name = StringField('Asset Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    image_file = FileField('Asset Image') 
    issue_date = DateField('Issue Date', format='%Y-%m-%d') 
    return_date = DateField('Return Date', format='%Y-%m-%d', validators=[Optional()]) 
    submit = SubmitField('Add Asset')



