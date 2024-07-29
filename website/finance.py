from flask import render_template, request, flash, redirect,Blueprint, url_for, current_app as app
from flask_login import current_user, login_required




finance=Blueprint('finance',__name__)


@finance.route('/fin_dashbord',methods=['GET','POST'])
@login_required
def fin_dashbord():
    return render_template('Finance/dashboard.html')