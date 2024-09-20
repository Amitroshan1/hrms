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
from .models.emp_detail_models import Asset
from .models.query import Query
from werkzeug.security import check_password_hash, generate_password_hash
from . import db
from .forms.manager import ChangePasswordForm



auth = Blueprint('auth', __name__)

@auth.app_errorhandler(401)
def unauthorized_error(error):
    flash('You need to be logged in to access this page.', 'error')
    return redirect(url_for('auth.login'))



@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        
        return redirect(url_for('auth.E_homepage'))

    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Admin.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('auth.E_homepage'))  
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
    
   
    emp = Admin.query.filter_by(id=employee.admin_id).first()
    
    
    DOJ = emp.Doj if emp else None

    
    today = date.today()
    punch = Punch.query.filter_by(admin_id=current_user.id, punch_date=today).first()
    
    punch_in_time = punch.punch_in if punch else None
    punch_out_time = punch.punch_out if punch else None
    
    emp_type = emp.Emp_type if emp else None
    circle = emp.circle if emp else None

    
    manager_contact = ManagerContact.query.filter_by(circle_name=circle, user_type=emp_type).first()

    
    news_feeds = NewsFeed.query.filter(
        (NewsFeed.circle == circle) & (NewsFeed.emp_type == emp_type) |
        (NewsFeed.circle == 'All') & (NewsFeed.emp_type == 'All') |
        (NewsFeed.circle == circle) & (NewsFeed.emp_type == 'All') |
        (NewsFeed.circle == 'All') & (NewsFeed.emp_type == emp_type)
    ).order_by(NewsFeed.created_at.desc()).all()

    all_queries = Query.query.all()
    queries_for_emp_type = []

    for query in all_queries:
        
        query_emp_types = query.emp_type.split(',') if query.emp_type else []
        #print(query_emp_types)
        if emp_type in query_emp_types:  # Check if the current employee's emp_type matches any in the query
            queries_for_emp_type.append(query)
    

    show_notification = bool(queries_for_emp_type)


    

   
    return render_template("employee/E_homepage.html", 
                           employee=employee, 
                           punch_in_time=punch_in_time, 
                           punch_out_time=punch_out_time,
                           manager_contact=manager_contact,
                           news_feeds=news_feeds,
                           DOJ=DOJ,
                           show_notification=show_notification,
                        queries_for_emp_type=queries_for_emp_type )






@auth.route('/logout')
@login_required
def logout():
    logout_user()
    form = AdminLoginForm()
    return redirect(url_for('auth.login'))





@auth.route('/my_assets', methods=['GET'])
@login_required  
def my_assets():
    
    emp_id = current_user.id
    
   
    assets = Asset.query.filter_by(admin_id=emp_id).all()
    
    if not assets:
        flash('No assets found for your account.', 'info')
    
    return render_template('employee/my_assets.html', assets=assets)



@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        original_password = form.original_password.data
        new_password = form.new_password.data
        

        # Verify original password
        if not current_user.check_password(original_password):
            flash('Original password is incorrect', 'danger')
            return redirect(url_for('auth.change_password'))

        # Update the password
        current_user.set_password(new_password)
        db.session.commit()

        flash('Your password has been updated successfully', 'success')
        return redirect(url_for('auth.change_password'))  # Redirect to profile or wherever you like

    return render_template('profile/change_password.html',form=form)
