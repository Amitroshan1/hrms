from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models.Admin_models import Admin
from .models.emp_detail_models import Employee
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .forms.signup_form import AdminLoginForm
from datetime import date
from .models.attendance import Punch
from .models.manager_model import ManagerContact
from .models.news_feed import NewsFeed

auth = Blueprint('auth', __name__)

@auth.app_errorhandler(401)
def unauthorized_error(error):
    flash('You need to be logged in to access this page.', 'error')
    return redirect(url_for('auth.login'))



@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # Redirect based on Emp_type if the user is already logged in
        return redirect(url_for('auth.E_homepage'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Admin.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('auth.E_homepage'))  # Redirect based on Emp_type after successful login
        else:
            flash('Invalid email or password. Please try again.', category='error')

    return render_template('employee/login.html', form=form, next=request.args.get('next'))


@auth.route('/E_homepage')
@login_required
def E_homepage():
    employee = Employee.query.filter_by(admin_id=current_user.id).first()
    if not employee:
        flash("No employee record found for the current user.")
        return render_template("employee/E_homepage.html")
    else:
        emp = Admin.query.filter_by(id=employee.admin_id).first()
    
    today = date.today()
    punch = Punch.query.filter_by(admin_id=current_user.id, punch_date=today).first()

    
    
    punch_in_time = punch.punch_in if punch else None
    punch_out_time = punch.punch_out if punch else None

    emp_type = emp.Emp_type
    circle = emp.circle
    

    manager_contact = ManagerContact.query.filter_by(circle_name=circle, user_type=emp_type).first()

    news_feeds = NewsFeed.query.order_by(NewsFeed.created_at.desc()).all()

    return render_template("employee/E_homepage.html", 
                           employee=employee, 
                           punch_in_time=punch_in_time, 
                           punch_out_time=punch_out_time,
                           manager_contact=manager_contact,
                           news_feeds=news_feeds)





@auth.route('/logout')
@login_required
def logout():
    logout_user()
    form = AdminLoginForm()
    return redirect(url_for('auth.login'))






