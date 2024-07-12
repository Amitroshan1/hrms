from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField,SelectField,FileField,DateField
from wtforms.validators import *
from flask_wtf.file import FileAllowed
from website.models.Admin_models import Admin



class Employee_Details(FlaskForm):
    Photo = FileField('Employee Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    name = StringField('Full_Name', 
                         validators=[DataRequired()], 
                         render_kw={"placeholder": "Enter your Name"})
    
    email = StringField('Email_Id', 
                        validators=[DataRequired(), Email()], 
                        render_kw={"placeholder": "Enter your Email_Id"})
    
    FatherName=StringField('Father Name', 
                         validators=[DataRequired()], 
                         render_kw={"placeholder": "Enter your Father Name"})
    
    MotherName=StringField('Mother Name', 
                         validators=[DataRequired()], 
                         render_kw={"placeholder": "Enter your Mother Name"})
    

    Marital_status = SelectField('Marital Status', 
                            choices=[('married', 'Married'), ('unmarried', 'Unmarried')],
                              validators=[DataRequired()])
    
    Spousename=StringField('Spouse Name', 
                         validators=[Optional()], 
                         render_kw={"placeholder": "Enter your Spouse Name"})
    
    DOB=DateField("Date Of Birth",format='%Y-%m-%d', validators=[InputRequired()])



    emp_id = StringField('Employee ID', 
                        validators=[DataRequired()], 
                        render_kw={"placeholder": "Enter your Employee_ID"})
    

    mobile = StringField('Mobile Number', 
                         validators=[DataRequired(), Length(min=10, max=10)], 
                         render_kw={"placeholder": "Enter your Mobile number"})
    
    Gender = SelectField('Gender', 
                            choices=[('male', 'Male'), ('female', 'Female')],
                              validators=[DataRequired()])
    
    Emergency_mobile = StringField('Emergency Number', 
                         validators=[DataRequired(), Length(min=10, max=10)], 
                         render_kw={"placeholder": "Enter your Emergency Conatct Number"})
    
    Caste = StringField('Caste', 
                             validators=[DataRequired(), Length(min=2, max=150)], 
                             render_kw={"placeholder": "Enter your Caste"})
    
    Nationality = StringField('Nationality', 
                             validators=[DataRequired(), Length(min=2, max=150)], 
                             render_kw={"placeholder": "Enter your Nationality"})
    
    Language = StringField('Language', 
                             validators=[DataRequired(), Length(min=2, max=150)], 
                             render_kw={"placeholder": "Enter the Language"})
    
    Religion = StringField('Religion', 
                             validators=[DataRequired(), Length(min=2, max=150)], 
                             render_kw={"placeholder": "Enter your Full_Name"})
    
    Blood_Group = StringField('Blood Group', 
                             validators=[DataRequired(), Length(min=2, max=150)], 
                             render_kw={"placeholder": "Enter your Full_Name"})
    
    permanent_address_line1 = StringField('Address Line 1', validators=[DataRequired()])
    permanent_address_line2 = StringField('Address Line 2')
    permanent_address_line3 = StringField('Address Line 3')
    permanent_pincode = StringField('Pincode', validators=[DataRequired()])
    permanent_district = StringField('District', render_kw={'readonly': True})
    permanent_state = StringField('State', render_kw={'readonly': True})

    present_address_line1 = StringField('Address Line 1', validators=[DataRequired()])
    present_address_line2 = StringField('Address Line 2')
    present_address_line3 = StringField('Address Line 3')
    present_pincode = StringField('Pincode', validators=[DataRequired()])
    present_district = StringField('District', render_kw={'readonly': True})
    present_state = StringField('State', render_kw={'readonly': True})

    submit = SubmitField('Save')
    
    
    
    
    
    
    

    

    

    