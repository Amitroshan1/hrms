from flask import render_template, request, flash, redirect,Blueprint, session,url_for, current_app as app
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .forms.signup_form import AdminSignUpForm
from .forms.search_from import SearchForm,DetailForm
from .models.Admin_models import Admin
from . import db
from .models.Admin_models import Admin
from .models.emp_detail_models import Employee
from .models.family_models import FamilyDetails
from .models.prev_com import PreviousCompany
from .models.education import UploadDoc, Education
from .models.attendance import Punch, LeaveBalance
from .models.manager_model import ManagerContact


hr=Blueprint('hr',__name__)


@hr.route('/hr_dashbord',methods=['GET','POST'])
@login_required
def hr_dashbord():
    return render_template('HumanResource/hr_dashboard.html')



@hr.route("/sign-up", methods=["GET", "POST"])
@login_required
def sign_up():
    form = AdminSignUpForm()

    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password = form.password.data
        mobile = form.mobile.data
        emp_id = form.emp_id.data
        user_type = form.user_type.data
        circle= form.circle.data

        new_user = Admin(email=email,circle=circle, first_name=first_name, Emp_type=user_type,mobile=mobile, emp_id=emp_id, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created', category='success')
        return redirect(url_for('hr.sign_up'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", category='error')

    return render_template("HumanResource/sign_up.html", form=form)







@hr.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        circle = form.circle.data
        emp_type = form.emp_type.data

        admins = Admin.query.filter_by(circle=circle, Emp_type=emp_type).all()

        if not admins:
            flash('No matching entries found', category='error')
            return redirect(url_for('hr.search'))

        # Store the search results in the session
        session['admins'] = [admin.id for admin in admins]
        session['circle'] = circle
        session['emp_type'] = emp_type

        return redirect(url_for('hr.search_results'))

    return render_template('HumanResource/search_form.html', form=form)

@hr.route('/search_results', methods=['GET'])
@login_required
def search_results():
    if 'admins' not in session:
        return redirect(url_for('hr.search'))

    admin_ids = session['admins']
    circle = session['circle']
    emp_type = session['emp_type']

    admins = Admin.query.filter(Admin.id.in_(admin_ids)).all()
    
    detail_form = DetailForm()
    detail_form.user.choices = [(admin.id, admin.first_name) for admin in admins]
        
    return render_template('HumanResource/search_result.html', admins=admins, circle=circle, emp_type=emp_type, form=detail_form)



@hr.route('/view_details', methods=['GET', 'POST'])
@login_required
def view_details():
    form = DetailForm()
    form.user.choices = [(admin.id, admin.first_name) for admin in Admin.query.all()]  # Populate user choices

    if form.validate_on_submit():
        user_id = form.user.data
        detail_type = form.detail_type.data

        admin = Admin.query.get(user_id)
        print(f"Admin ID: {user_id}, Admin: {admin}")  # Debugging line
        details = None

        # Existing logic...

        if admin is None:
            flash('No admin found for the selected user.', 'error')
            return redirect(url_for('hr.search'))

        return render_template('HumanResource/details.html', admin=admin, details=details, detail_type=detail_type)

    return render_template('HumanResource/details.html', form=form)




@hr.route('/display_details', methods=['GET'])
@login_required
def display_details():
    user_id = session.get('viewing_user_id')
    detail_type = session.get('viewing_detail_type')

    if not user_id or not detail_type:
        return redirect(url_for('hr.search'))

    admin = Admin.query.get(user_id)
    details = None

    if detail_type == 'family':
        details = FamilyDetails.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'previous_company':
        details = PreviousCompany.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'emp_details':
        details = Employee.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'education':
        details = Education.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'attendance':
        details = Punch.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'document':
        details = UploadDoc.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'leave_bal':
        details = LeaveBalance.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'manager_contact':
        details = ManagerContact.query.filter_by(admin_id=user_id).all()

    # Check if the admin exists
    if admin is None:
        return redirect(url_for('hr.search'))

    return render_template('HumanResource/details.html', admin=admin, details=details, detail_type=detail_type)
