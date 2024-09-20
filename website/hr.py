from flask import render_template, flash, redirect,Blueprint, session,url_for, current_app,send_from_directory,request
from flask_login import login_required
from .forms.search_from import SearchForm,DetailForm,NewsFeedForm,SearchEmp_Id,AssetForm
from .models.Admin_models import Admin
from . import db
from .models.emp_detail_models import Employee,Asset
from .models.family_models import FamilyDetails
from .models.prev_com import PreviousCompany
from .models.education import UploadDoc, Education
from .models.attendance import Punch, LeaveApplication
from .models.news_feed import NewsFeed
from .forms.attendance import MonthYearForm
from datetime import datetime
import calendar
from werkzeug.utils import secure_filename
import os



hr=Blueprint('hr',__name__)


@hr.route('/hr_dashbord',methods=['GET','POST'])
@login_required
def hr_dashbord():
    today = datetime.today()
    current_day = today.day
    current_month = today.month

    employees_with_anniversaries = Admin.query.filter(
        db.extract('month', Admin.Doj) == current_month,
        db.extract('day', Admin.Doj) == current_day
    ).all()
    

    employees_with_birthdays = Employee.query.filter(
        db.extract('month', Employee.dob) == current_month,
        db.extract('day', Employee.dob) == current_day
    ).all()

    return render_template('HumanResource/hr_dashboard.html',
                           employees_with_anniversaries=employees_with_anniversaries,
                           employees_with_birthdays=employees_with_birthdays)
   

    
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
    form.user.choices = [(admin.id, admin.first_name) for admin in Admin.query.all()] 

    if form.validate_on_submit():
        user_id = form.user.data
        detail_type = form.detail_type.data

        
        session['viewing_user_id'] = user_id
        session['viewing_detail_type'] = detail_type

        
        return redirect(url_for('hr.display_details'))

    return render_template('HumanResource/details.html', form=form)


@hr.route('/display_details', methods=['GET', 'POST'])
@login_required
def display_details():
    form = MonthYearForm()
    user_id = session.get('viewing_user_id')
    detail_type = session.get('viewing_detail_type')
    print(detail_type)

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

    if detail_type == 'Family Details':
        details = FamilyDetails.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'Previous_company':
        details = PreviousCompany.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'Employee Details':
        
        details = Employee.query.filter_by(admin_id=user_id).all()
        
    elif detail_type == 'Education':
        details = Education.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'Attendance':
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
    elif detail_type == 'Document':
        details = UploadDoc.query.filter_by(admin_id=user_id).all()
    elif detail_type == 'Leave Details':
        details = LeaveApplication.query.filter_by(admin_id=user_id).all()   
    

    if admin is None:
        return redirect(url_for('hr.view_details'))

    return render_template('HumanResource/details.html', admin=admin, details=details, detail_type=detail_type, selected_month=month, selected_year=year, form=form, datetime=datetime)



@hr.route('/employee_list', methods=['GET', 'POST'])
@login_required
def employee_list():
    form = SearchForm()
    employees = []

    if form.validate_on_submit():
        emp_type = form.emp_type.data
        circle = form.circle.data

       
        session['emp_type'] = emp_type
        session['circle'] = circle

        
        employees = Admin.query.filter_by(Emp_type=emp_type, circle=circle).all()

    else:
        
        emp_type = session.get('emp_type')
        circle = session.get('circle')

        if emp_type and circle:
            employees = Admin.query.filter_by(Emp_type=emp_type, circle=circle).all()

    return render_template('HumanResource/emp_list.html', form=form, employees=employees)






@hr.route('/news_feed/add', methods=['GET', 'POST'])
@login_required
def add_news_feed():
    form = NewsFeedForm()
    if form.validate_on_submit():
        file = form.file.data
        file_path = None
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

       
        news_feed = NewsFeed(
            title=form.title.data,
            content=form.content.data,
            file_path=filename if file else None,
            circle=form.circle.data,
            emp_type=form.emp_type.data
        )
        db.session.add(news_feed)
        db.session.commit()
        flash('News feed added successfully!', 'success')
        return redirect(url_for('hr.add_news_feed'))

    return render_template('HumanResource/add_news_feed.html', form=form)



@hr.route('/news_feed/<int:news_feed_id>')
@login_required
def view_news_feed(news_feed_id):
    news_feed = NewsFeed.query.get_or_404(news_feed_id)
    return render_template('employee/view_news_feed.html', news_feed=news_feed)



@hr.route('/uploads/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

   


@hr.route('/search_employee', methods=['GET', 'POST'])
def search_employee():
    form = SearchEmp_Id()
    employee = None

    if form.validate_on_submit():
        emp_id = form.emp_id.data
        employee = Admin.query.filter_by(emp_id=emp_id).first()

        if employee is None:
            flash('Employee not found!', 'danger')
        else:
            return render_template('HumanResource/asset_search.html', form=form, employee=employee)

    return render_template('HumanResource/asset_search.html', form=form, employee=employee)


@hr.route('/add_asset/<int:admin_id>', methods=['GET', 'POST'])
def add_asset(admin_id):
    asset_form = AssetForm()
    employee = Admin.query.get(admin_id)

    if asset_form.validate_on_submit():
        photo_filename = None
        if asset_form.image_file.data:
            photo_filename = secure_filename(asset_form.image_file.data.filename)
            asset_form.image_file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename))
        
        new_asset = Asset(
            name=asset_form.name.data,
            description=asset_form.description.data,
            admin_id=employee.id,
            image_file=photo_filename,
            issue_date=asset_form.issue_date.data,
            return_date=asset_form.return_date.data if asset_form.return_date.data else None
        )
        db.session.add(new_asset)
        db.session.commit()
        flash('Asset added successfully!', 'success')

        return redirect(url_for('hr.add_asset', admin_id=admin_id))

    assets = employee.assets if employee else []

    return render_template('HumanResource/assets.html', asset_form=asset_form, employee=employee, assets=assets)



@hr.route('/update_asset/<int:asset_id>', methods=['GET', 'POST'])
def update_asset(asset_id):
    asset = Asset.query.get(asset_id)
    asset_form = AssetForm()

    if request.method == 'GET':
       
        asset_form.name.data = asset.name
        asset_form.description.data = asset.description
        asset_form.image_file.data = asset.image_file 
        asset_form.issue_date.data = asset.issue_date
        asset_form.return_date.data = asset.return_date

    if asset_form.validate_on_submit():
        photo_filename = None
        if asset_form.image_file.data:
            photo_filename = secure_filename(asset_form.image_file.data.filename)
            asset_form.image_file.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], photo_filename))
        
       
        asset.name = asset_form.name.data
        asset.description = asset_form.description.data
        asset.image_file = photo_filename if photo_filename else asset.image_file
        asset.issue_date = asset_form.issue_date.data
        asset.return_date = asset_form.return_date.data if asset_form.return_date.data else None

        db.session.commit()
        flash('Asset updated successfully!', 'success')

        return redirect(url_for('hr.add_asset', admin_id=asset.admin_id))

    return render_template('HumanResource/assets_update.html', asset_form=asset_form, asset=asset)

