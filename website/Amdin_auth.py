from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from website import db
from .models.Admin_models import Admin
from .forms.signup_form import AdminSignUpForm

from .models.attendance import LeaveBalance



Admin_auth = Blueprint('Admin_auth', __name__)


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
        circle = form.circle.data

        
        new_user = Admin(
            email=email,
            circle=circle,
            first_name=first_name,
            Emp_type=user_type,
            mobile=mobile,
            emp_id=emp_id,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            Doj=form.Doj.data 
        )
        db.session.add(new_user)
        db.session.commit()

       
        new_leave_balance = LeaveBalance(admin_id=new_user.id)
        db.session.add(new_leave_balance)
        db.session.commit()

        flash('Account created successfully!', category='success')
        return redirect(url_for('Admin_auth.admin_sign_up'))
    else:
        # Handle form errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", category='error')

    return render_template("admin/AdminSign_up.html", form=form)










