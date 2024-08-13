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
from .forms.attendance import MonthYearForm
from datetime import datetime
import calendar


hr=Blueprint('hr',__name__)


@hr.route('/hr_dashbord',methods=['GET','POST'])
@login_required
def hr_dashbord():
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

    return render_template('HumanResource/hr_dashboard.html', form=form)
    








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

        # Store selected user_id and detail_type in session
        session['viewing_user_id'] = user_id
        session['viewing_detail_type'] = detail_type

        # Redirect to display_details route to fetch and display the details
        return redirect(url_for('hr.display_details'))

    return render_template('HumanResource/details.html', form=form)




@hr.route('/display_details', methods=['GET', 'POST'])
@login_required
def display_details():
    form = MonthYearForm()
    user_id = session.get('viewing_user_id')
    detail_type = session.get('viewing_detail_type')

    if not user_id or not detail_type:
        return redirect(url_for('hr.view_details'))

    admin = Admin.query.get(user_id)
    details = None

    if form.validate_on_submit():
        month = int(form.month.data)
        year = int(form.year.data)
    else:
        month = datetime.now().month
        year = datetime.now().year

    if detail_type == 'family':
        details = FamilyDetails.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'previous_company':
        details = PreviousCompany.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'emp_details':
        details = Employee.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'education':
        details = Education.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'attendance':
        num_days = calendar.monthrange(year, month)[1]
        details = [{'punch_date': f'{year}-{month:02d}-{day:02d}', 'punch_in': 'Leave', 'punch_out':'Leave'} for day in range(1, num_days + 1)]
        punches = Punch.query.filter(
            Punch.punch_date.between(f'{year}-{month:02d}-01', f'{year}-{month:02d}-{num_days}')
        ).filter_by(admin_id=user_id).all()
        for punch in punches:
            for detail in details:
                if detail['punch_date'] == punch.punch_date.strftime('%Y-%m-%d'):
                    detail['punch_in'] = punch.punch_in
                    detail['punch_out'] = punch.punch_out
    elif detail_type == 'document':
        details = UploadDoc.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'leave_bal':
        details = LeaveBalance.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'manager_contact':
        details = ManagerContact.query.filter_by(admin_id=user_id).all()

    if admin is None:
        return redirect(url_for('hr.view_details'))

    return render_template('HumanResource/details.html', admin=admin, details=details, detail_type=detail_type, selected_month=month, selected_year=year, form=form, datetime=datetime)