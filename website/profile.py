from flask import render_template, flash, redirect,Blueprint, send_from_directory, url_for, current_app as app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import os
from .models.family_models import FamilyDetails
from .forms.Emp_details import Employee_Details
from .models.emp_detail_models import Employee
from . import db
from .forms.education import EducationForm,UploadDocForm
from .models.education import Education,UploadDoc
from .forms.family_details import Family_details
from .forms.previous_company import Previous_company
from .models.prev_com import PreviousCompany

profile=Blueprint('profile',__name__)




@profile.route('/emp_details',methods=['GET','POST'])
@login_required
def emp_profile():
    form=Employee_Details()
    return render_template("profile/emp_det.html",form=form)


@profile.route('/emp_det2', methods=['GET', 'POST'])
@login_required
def empl_det():
    employee = Employee.query.filter_by(admin_id=current_user.id).first()
    form = Employee_Details(obj=employee) 
    
    if form.validate_on_submit():
        if form.Photo.data:
            filename = secure_filename(form.Photo.data.filename)
            form.Photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = employee.photo_filename if employee else None
        
        if employee:
            
            form.populate_obj(employee)
            employee.photo_filename = filename
            db.session.commit()
            flash('Employee details updated successfully!', 'success')
        else:
            
            new_employee = Employee(
                admin_id=current_user.id, 
                photo_filename=filename,
                name=form.name.data,
                email=form.email.data,
                father_name=form.father_name.data,
                mother_name=form.mother_name.data,
                marital_status=form.marital_status.data,
                spouse_name=form.spouse_name.data,
                dob=form.dob.data,
                emp_id=form.emp_id.data,
                designation=form.designation.data,
                mobile=form.mobile.data,
                gender=form.gender.data,
                emergency_mobile=form.emergency_mobile.data,
                caste=form.caste.data,
                nationality=form.nationality.data,
                language=form.language.data,
                religion=form.religion.data,
                blood_group=form.blood_group.data,
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
        
        return redirect(url_for('auth.E_homepage'))
    
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {getattr(form, field).label.text}: {error}", category='error')
    
    return render_template('profile/emp_det.html', form=form)


@profile.route('/family_det')
@login_required
def fam_det():
    family_members = FamilyDetails.query.filter_by(admin_id=current_user.id).all()
    return render_template('profile/E_Family_details.html',family_members = family_members)


@profile.route('/family_details', methods=['GET', 'POST'])
@login_required
def family_details():
    form = Family_details()
    
    if form.validate_on_submit():
        photo_filename = None
        if form.Photo.data:
            photo_filename = secure_filename(form.Photo.data.filename)
            form.Photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

        new_family_member = FamilyDetails(
            admin_id=current_user.id,
            photo_filename=photo_filename,
            name=form.name.data,
            email=form.email.data,
            dob=form.dob.data,
            age=int(form.age.data),
            relation=form.relation.data,
            occupation=form.occupation.data,
            income=form.Income.data,
            address=form.Address.data,
            remarks=form.Remarks.data,
            
        )
        
        db.session.add(new_family_member)
        db.session.commit()
        
        flash('Family member details saved successfully!', 'success')
        return redirect(url_for('profile.fam_det'))  
   
    return render_template('profile/form_E_FAM.html', form=form)



@profile.route('/previous_company', methods=['GET', 'POST'])
@login_required
def previous_company():
    form = Previous_company()
    if form.validate_on_submit():
        new_company = PreviousCompany(
            admin_id=current_user.id,
            com_name=form.com_name.data,
            designation=form.designation.data,
            doj=form.doj.data,
            dol=form.dol.data,
            reason=form.reason.data,
            salary=form.salary.data,
            uan=form.uan.data,
            pan=form.pan.data,
            contact=form.contact.data,
            name_contact=form.name_contact.data,
            pf_num=form.pf_num.data,
            address=form.address.data
        )
        db.session.add(new_company)
        db.session.commit()
        flash('Previous company details saved successfully!', 'success')
        return redirect(url_for('profile.previous_company'))

    previous_companies = PreviousCompany.query.filter_by(admin_id=current_user.id).all()
    return render_template('profile/previous_company.html', form=form, previous_companies=previous_companies)




@profile.route('/education', methods=['GET', 'POST'])
@login_required
def education():
    form = EducationForm()
    education = Education.query.filter_by(admin_id=current_user.id).all()

    if form.validate_on_submit():
        if form.doc_file.data:
            filename = secure_filename(form.doc_file.data.filename)
            form.doc_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        new_education = Education(
            admin_id=current_user.id,
            qualification=form.qualification.data,
            institution=form.institution.data,
            board=form.board.data,
            start=form.start.data,
            end=form.end.data,
            marks=form.marks.data,
            doc_file=filename
        )
        db.session.add(new_education)
        db.session.commit()
        flash('Education details added successfully!', 'success')
        return redirect(url_for('profile.education'))

    return render_template('profile/education.html', form=form, education=education)


@profile.route('/delete_education/<int:education_id>', methods=['POST'])
@login_required
def delete_education(education_id):
    education = Education.query.get_or_404(education_id)
    if education.admin_id != current_user.id:
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('profile.education'))
    
    db.session.delete(education)
    db.session.commit()
    flash('Education detail deleted successfully!', 'success')
    return redirect(url_for('profile.education'))







@profile.route('/upload_doc', methods=['GET', 'POST'])
@login_required
def upload_docs():
    form = UploadDocForm()
    upload_doc = UploadDoc.query.filter_by(admin_id=current_user.id).all()

    if form.validate_on_submit():
        if form.doc_file.data:
            filename = secure_filename(form.doc_file.data.filename)
            form.doc_file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        new_upload_doc = UploadDoc(
            admin_id=current_user.id,
            doc_name=form.doc_name.data,
            doc_number=form.doc_number.data,
            issue_date=form.issue_date.data,
            doc_file=filename
        )
        db.session.add(new_upload_doc)
        db.session.commit()
        flash('Document uploaded successfully!', 'success')
        return redirect(url_for('profile.upload_docs'))

    return render_template('profile/upload_doc.html', form=form, upload_doc=upload_doc)


@profile.route('/delete_document/<int:doc_id>', methods=['POST'])
@login_required
def delete_document(doc_id):
    document = UploadDoc.query.get_or_404(doc_id)
    if document.admin_id != current_user.id:
        flash('You do not have permission to delete this item.', 'danger')
        return redirect(url_for('profile.upload_docs'))
    
    # Delete the file from the filesystem if it exists
    if document.doc_file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], document.doc_file)
        if os.path.exists(file_path):
            os.remove(file_path)
    
    db.session.delete(document)
    db.session.commit()
    flash('Document deleted successfully!', 'success')
    return redirect(url_for('profile.upload_docs'))


