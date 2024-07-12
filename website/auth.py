from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models.Admin_models import Admin
from werkzeug.security import check_password_hash
from urllib.parse import urlparse, urljoin

from flask_login import login_user, login_required, logout_user,current_user
from .forms.signup_form import AdminLoginForm

auth = Blueprint('auth', __name__)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return render_template("employee/E_homepage.html")

    form = AdminLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = Admin.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            if user.Emp_type != 'admin':
                login_user(user)
                flash('Logged in successfully!', category='success')
                next_page = request.args.get('next')
                # Redirect to the next page if it's safe
                if next_page and is_safe_url(next_page):
                    return redirect(next_page)
                else:
                    return redirect(url_for('auth.E_homepage'))
            else:
                flash('Not an Employee. Please contact HR or Admin.', category='error')
        else:
            flash('Invalid email or password. Please try again.', category='error')

    # Pass the next parameter to the login form template
    return render_template('employee/login.html', form=form, next=request.args.get('next'))

@auth.route('/E_homepage')
@login_required
def E_homepage():
    return render_template("employee/E_homepage.html")



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    form = AdminLoginForm()
    return redirect(url_for('auth.login'))






