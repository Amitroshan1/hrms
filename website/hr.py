from flask import render_template, request, flash, redirect,Blueprint, url_for, current_app as app
from flask_login import current_user, login_required



hr=Blueprint('hr',__name__)


@hr.route('/hr_dashbord',methods=['GET','POST'])
@login_required
def hr_dashbord():
    return render_template('HumanResource/hr_dashboard.html')


