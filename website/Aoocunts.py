from flask import *
from flask_login import login_required,current_user
from .forms.search_from import SearchForm,DetailForm
from .forms.manager import PaySlipForm
from .models.news_feed import PaySlip
import os
from werkzeug.utils import secure_filename
from .models.Admin_models import Admin
from . import db
from .models.query import Query, QueryReply
from .forms.query_form import QueryForm, QueryReplyForm,PasswordForm

from .common import verify_password_and_send_email,send_email_from_company




Accounts = Blueprint('Accounts', __name__)



@Accounts.route('/Acc_dashbord',methods=['GET','POST'])
@login_required
def Acc_dashbord():
    queries = Query.query.all()
    return render_template('Accounts/Acc_dashboard.html', queries=queries)
    

@Accounts.route('/Acc_search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        circle = form.circle.data
        emp_type = form.emp_type.data
        

        admins = Admin.query.filter_by(circle=circle, Emp_type=emp_type).all()
        

        if not admins:
            flash('No matching entries found', category='error')
            return redirect(url_for('Accounts.search'))

        
        session['admins'] = [admin.id for admin in admins]
        session['circle'] = circle
        session['emp_type'] = emp_type

        return redirect(url_for('Accounts.search_results'))

    return render_template('Accounts/search_form.html', form=form)


@Accounts.route('/Acc_search_results', methods=['GET'])
@login_required
def search_results():
    if 'admins' not in session:
        return redirect(url_for('Accounts.Acc_search'))

    admin_ids = session['admins']
    circle = session['circle']
    emp_type = session['emp_type']

    admins = Admin.query.filter(Admin.id.in_(admin_ids)).all()
    
    detail_form = DetailForm()
    detail_form.user.choices = [(admin.id, admin.first_name) for admin in admins]
        
    return render_template('Accounts/search_result.html', admins=admins, circle=circle, emp_type=emp_type, form=detail_form)



@Accounts.route('/add_payslip/<int:admin_id>', methods=['GET', 'POST'])
@login_required
def add_payslip(admin_id):
    form = PaySlipForm()
    employee = Admin.query.get_or_404(admin_id)

    if form.validate_on_submit():
        file_path = None
        if form.payslip_file.data:
            filename = secure_filename(form.payslip_file.data.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.payslip_file.data.save(file_path)

        new_payslip = PaySlip(
            admin_id=employee.id,
            month=form.month.data,
            year=form.year.data,
            file_path=filename  
        )

        db.session.add(new_payslip)
        db.session.commit()

        email=employee.email
        
       
        account_email='demoaountsaffo4353@outlook.com'
        password ='Demo@1234'
        subject=f'payslip of Month {form.month.data} Uploded'
        body=f'Dear {employee.first_name},\n\n'
        body+=f'This mail is to inform you that Playslip of month {form.month.data} generated.\nPlease find the Payslip in HRMS \n \n  '
        body+='Thanks\n Accounts'

        send_email_from_company(account_email,password,subject,body,email,cc_emails=None)

        flash('PaySlip added successfully! and Mail has Been Send', 'success')
        return redirect(url_for('Accounts.search_results'))

    return render_template('Accounts/add_payslip.html', form=form, employee=employee)







@Accounts.route('/payslips', methods=['GET'])
@login_required
def view_payslips():
    payslips = PaySlip.query.filter_by(admin_id=current_user.id).order_by(PaySlip.year.desc(), PaySlip.month.desc()).all()

    if not payslips:
        flash('No PaySlips available', 'warning')
        return render_template('Accounts/view_payslips.html', payslips=payslips)  # Redirect to the dashboard or any other relevant page

    return render_template('Accounts/view_payslips.html', payslips=payslips)


@Accounts.route('/download_payslip/<int:payslip_id>', methods=['GET'])
@login_required
def download_payslip(payslip_id):
    payslip = PaySlip.query.get_or_404(payslip_id)


    if payslip.admin_id != current_user.id:
        flash('You are not authorized to download this PaySlip', 'danger')
        return redirect(url_for('Accounts.view_payslips'))

   
    
    file_path = os.path.join('C:\\Users\\Admin\\Desktop\\saffo_HR_app\\website\\static\\uploads', payslip.file_path)



   
    if not os.path.exists(file_path):
        flash('The requested file does not exist.', 'danger')
        return redirect(url_for('Accounts.view_payslips'))
 
    return send_file(file_path, as_attachment=True)





@Accounts.route('/create_query', methods=['GET', 'POST'])
@login_required
def create_query():
    form = QueryForm()
    password_form = PasswordForm()

    if 'query_data' in session and password_form.validate_on_submit():
        

        
        query_data = session.pop('query_data')
        
        
        new_query = Query(
            admin_id=current_user.id,
            emp_type=query_data['emp_type'],
            title=query_data['title'],
            query_text=query_data['query_text']
        )
        db.session.add(new_query)
        db.session.commit()

        
        depart = new_query.emp_type
        department= depart.split(',')
        

        
        
        if len(department) > 1:
            
            
            if department[0] == 'Human Resource':
                
                department_email = 'hr@saffotech.com'
                cc = 'accounts@saffotech.com'
                
            else:
                department_email = 'accounts@saffotech.com'
                cc = 'hr@saffotech.com'
                
        else:
            
            if department[0] == 'Human Resource':
                department_email = 'hr@saffotech.com'
                cc = None
               
            else:
                department_email = 'accounts@saffotech.com'
                cc = None
                

        
        subject = f"New Query Created: {new_query.title}"
        body = f"A new query has been raised by {current_user.first_name}.\n\n"
        body += f"Department: {new_query.emp_type}\n\nQuery Title: {new_query.title}\n\n"
        body += f"Query Details: {new_query.query_text}\n\nPlease address this query at your earliest convenience."

    
        if verify_password_and_send_email(current_user, password_form.password.data, subject, body, department_email, cc):
            flash('Your query has been created and email notification sent to the department.', 'success')
        else:
            flash('Password verification failed or email could not be sent.', 'error')

        return redirect(url_for('Accounts.create_query'))

    elif form.validate_on_submit():
       

        
        session['query_data'] = {
            'emp_type': ', '.join(form.emp_type.data),
            'title': form.title.data,
            'query_text': form.query_text.data
        }

       
        return render_template('Accounts/verify_password.html',form=password_form)

 
    user_queries = Query.query.filter_by(admin_id=current_user.id).order_by(Query.created_at.desc()).all()
    
    return render_template('Accounts/create_query.html', form=form, queries=user_queries)


    


@Accounts.route('/query/<int:query_id>/chat', methods=['GET', 'POST'])
@login_required
def chat_query(query_id):
    
    selected_query = Query.query.get_or_404(query_id)
    
    
    form = QueryReplyForm()  
    replies = QueryReply.query.filter(QueryReply.query_id == query_id).order_by(QueryReply.created_at.asc()).all()

 
    if form.validate_on_submit():
        reply_text = form.reply_text.data 

        if reply_text:
            new_reply = QueryReply(
                query_id=query_id,
                admin_id=current_user.id,
                reply_text=reply_text
            )
            db.session.add(new_reply)
            db.session.commit()
            
            return redirect(url_for('Accounts.chat_query', query_id=query_id))

    return render_template('Accounts/chat.html', query=selected_query, replies=replies, form=form)





@Accounts.route('/emp_type_queries')
@login_required
def view_emp_type_queries():
    emp_type = current_user.Emp_type
    
    
    queries_for_emp_type = Query.query.filter(
        Query.emp_type.ilike(f'%{emp_type}%') 
    ).all()

    
    for query in queries_for_emp_type:
        admin_details = Admin.query.filter_by(id=query.admin_id).first()
        query.admin_details = admin_details  

    return render_template('Accounts/view_emp_type_queries.html', queries=queries_for_emp_type)





@Accounts.route('/delete_query/<int:query_id>', methods=['GET', 'POST'])
@login_required
def close_query(query_id):
    form = PasswordForm()  
    
   
    query = Query.query.filter_by(id=query_id).first()
    replies = QueryReply.query.filter_by(query_id=query_id).all()



    body_chat = f"Query Title: {query.title}\n"
    body_chat += f"Department: {query.emp_type}\n\n"
    body_chat += "Chat History:\n"
    
    for reply in replies:
        admin = Admin.query.filter_by(id=reply.admin_id).first()
        body_chat += f"{admin.first_name}: {reply.reply_text} (on {reply.created_at})\n"
    
    body_chat += "\nIssue resolved. Closing this query."

    if not query:
        flash('Query not found.', 'error')
        return redirect(url_for('Accounts.create_query'))

    if form.validate_on_submit():
       
        subject = f"Satisfied with query: {query.title}"
        body = body_chat

        department = [query.emp_type]
        if len(department)>1:
            if department[0] == 'Human Resource' :
                department_email= 'HumanResourcesaffo@outlook.com'
                cc='demoaountsaffo4353@outlook.com'
            else:
                department_email= 'demoaountsaffo4353@outlook.com'
                cc='HumanResourcesaffo@outlook.com'
        else:
            if department[0] == 'Human Resource' :
                department_email= 'HumanResourcesaffo@outlook.com'
                cc=None
            else:
                department_email= 'demoaountsaffo4353@outlook.com'
                cc=None

    
        if verify_password_and_send_email(current_user, form.password.data, subject, body, department_email,cc):
            
            db.session.delete(query)

            db.session.commit()
            flash('Query resolved and deleted successfully. Notification sent to departments.', 'success')
            return redirect(url_for('Accounts.create_query'))
        else:
            flash('Failed to send email.', 'error')

    return render_template('Accounts/close_query.html', form=form)



