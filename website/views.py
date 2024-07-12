from flask import render_template, request, flash, redirect,Blueprint, url_for, current_app as app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from . import views
from .forms.Emp_details import Employee_Details
from .models.emp_detail_models import Employee
from . import db

views=Blueprint('views',__name__)


@views.route('/')
def home():
    return render_template('home.html')

@views.route('/employee_details',methods=['GET','POST'])
@login_required
def emp_profile():
    form=Employee_Details()
    return render_template("admin/profile/emp_det.html",form=form)


@views.route('/emp_det', methods=['GET', 'POST'])
@login_required
def employee_det():
    form = Employee_Details()
    if form.validate_on_submit():
        filename = None
        if form.Photo.data:
            filename = secure_filename(form.Photo.data.filename)
            form.Photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_employee = Employee(
            admin_id=current_user.id, 
            photo_filename=filename,
            name=form.name.data,
            email=form.email.data,
            father_name=form.FatherName.data,
            mother_name=form.MotherName.data,
            marital_status=form.Marital_status.data,
            spouse_name=form.Spousename.data,
            dob=form.DOB.data,
            emp_id=form.emp_id.data,
            mobile=form.mobile.data,
            gender=form.Gender.data,
            emergency_mobile=form.Emergency_mobile.data,
            caste=form.Caste.data,
            nationality=form.Nationality.data,
            language=form.Language.data,
            religion=form.Religion.data,
            blood_group=form.Blood_Group.data,
            permanent_address_line1=form.permanent_address_line1.data,
            permanent_address_line2=form.permanent_address_line2.data,
            permanent_address_line3=form.permanent_address_line3.data,
            permanent_pincode=form.permanent_pincode.data,
            permanent_district=form.permanent_district.data,
            permanent_state=form.permanent_state.data,
            present_address_line1=form.present_address_line1.data,
            present_address_line2=form.present_address_line2.data,
            present_address_line3=form.present_address_line3.data,
            present_pincode=form.present_pincode.data,
            present_district=form.present_district.data,
            present_state=form.present_state.data
        )
        
        db.session.add(new_employee)
        db.session.commit()
        
        flash('Employee details saved successfully!', 'success')
        return redirect(url_for('Admin_auth.A_homepage'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", category='error')
    
    return render_template('admin/profile/emp_det.html', form=form)
