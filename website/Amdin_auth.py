from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from website import db, mail
from .models.Admin_models import Admin
from .forms.signup_form import AdminSignUpForm, AdminLoginForm, AdminVerifyForm
from urllib.parse import urlparse, urljoin

Admin_auth = Blueprint('Admin_auth', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@Admin_auth.route('/Adminlogin', methods=["GET", "POST"])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('Admin_auth.A_homepage'))  # Redirect if already logged in

    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = Admin.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password) and user.Emp_type == 'admin':
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            return redirect(url_for('Admin_auth.A_homepage'))
        else:
            flash('Invalid login credentials or not an admin.', category='error')

    
    return render_template('admin/Adminlogin.html', form=form,next=request.args.get('next'))

@Admin_auth.route('/Adminlogout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Admin_auth.admin_login'))

@Admin_auth.route('/Admin_dashboard')
@login_required
def A_homepage():
    return render_template("admin/A_Homepage.html")





@Admin_auth.route('/verify', methods=['POST', 'GET'])
def admin_verification():
    form = AdminVerifyForm()
    if form.validate_on_submit():
        emp_id = form.employee_Id.data

        user = Admin.query.filter_by(emp_id=emp_id).first()
        if user:
            if user.Emp_type == 'admin':
                
                return redirect(url_for('Admin_auth.admin_login'))
            else:
                
                flash("Only Admin Allowed", category='error')
        else:
            flash("User not found", category='error')
    return render_template("admin/A_Verify.html", form=form)






@Admin_auth.route("/Adminsign-up", methods=["GET", "POST"])
def admin_sign_up():
    form = AdminSignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password = form.password.data
        mobile = form.mobile.data
        emp_id = form.emp_id.data
        user_type = form.user_type.data

        new_user = Admin(email=email, first_name=first_name, Emp_type=user_type,mobile=mobile, emp_id=emp_id, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created', category='success')
        return redirect(url_for('Admin_auth.admin_login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", category='error')

    return render_template("admin/AdminSign_up.html", form=form)








