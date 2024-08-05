from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models.Admin_models import Admin
from .models.emp_detail_models import Employee
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .forms.signup_form import AdminLoginForm
from datetime import date
from .models.attendance import Punch
from . import is_safe_url

auth = Blueprint('auth', __name__)
@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        
        if current_user.Emp_type == 'employee':
            return redirect(url_for('auth.E_homepage'))  
        elif current_user.Emp_type == 'hr':
            return redirect(url_for('auth.HR_homepage')) 
        elif current_user.Emp_type == 'finance':
            return redirect(url_for('auth.fin_homepage')) 
        else:
            flash('Invalid user type. Please contact support.', category='error')
            return redirect(url_for('auth.login'))  

    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Admin.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)  
            
            if user.Emp_type == 'employee':
                return redirect(url_for('auth.E_homepage'))
            elif user.Emp_type == 'admin':
                flash('Admin users cannot log in here.', category='error')
                return redirect(url_for('auth.login'))  
            elif user.Emp_type == 'hr':
                return redirect(url_for('auth.HR_homepage'))  
            elif user.Emp_type == 'finance':
                return redirect(url_for('auth.fin_homepage')) 
            else:
                flash('Unknown user type. Please contact support.', category='error')
                return redirect(url_for('auth.login'))

        else:
            flash('Invalid email or password. Please try again.', category='error')

    return render_template('employee/login.html', form=form, next=request.args.get('next'))

@auth.route('/E_homepage')
@login_required
def E_homepage():
    employee = Employee.query.filter_by(admin_id=current_user.id).first()
    
    today = date.today()
    punch = Punch.query.filter_by(admin_id=current_user.id, punch_date=today).first()
    
    punch_in_time = punch.punch_in if punch else None
    punch_out_time = punch.punch_out if punch else None
    
    return render_template("employee/E_homepage.html", 
                           employee=employee, 
                           punch_in_time=punch_in_time, 
                           punch_out_time=punch_out_time)

@auth.route('/hr_homepage')
@login_required
def HR_homepage():
    employee = Employee.query.filter_by(admin_id=current_user.id).first()
    
    today = date.today()
    punch = Punch.query.filter_by(admin_id=current_user.id, punch_date=today).first()
    
    punch_in_time = punch.punch_in if punch else None
    punch_out_time = punch.punch_out if punch else None

    return render_template("HumanResource/hr_homepage.html", 
                           employee=employee, 
                           punch_in_time=punch_in_time, 
                           punch_out_time=punch_out_time)

@auth.route('/account_homepage')
@login_required
def fin_homepage():
    employee = Employee.query.filter_by(admin_id=current_user.id).first()
    
    today = date.today()
    punch = Punch.query.filter_by(admin_id=current_user.id, punch_date=today).first()
    
    punch_in_time = punch.punch_in if punch else None
    punch_out_time = punch.punch_out if punch else None

    return render_template("Finance/acc_homepage.html", 
                           employee=employee, 
                           punch_in_time=punch_in_time, 
                           punch_out_time=punch_out_time)




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    form = AdminLoginForm()
    return redirect(url_for('auth.login'))






