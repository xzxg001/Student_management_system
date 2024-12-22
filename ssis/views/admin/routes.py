from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.helpers import url_for
from . import admin
from .utils import admin_found,register_user, is_invitation_code_valid

@admin.route('/', methods=['GET', 'POST'])
def login() -> str:
    return render_template('/admin/login.html')


@admin.route('/login', methods=['POST'])
def verify() -> str:
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if admin_found(username, password):
            return redirect(url_for('student.students'))
    return redirect(url_for('admin.login'))


@admin.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        invitation_code = request.form['invitation_code']
        
        if password != password2:
            flash("Passwords do not match.", "danger")
            return redirect(url_for('admin.register'))
        
        if not is_invitation_code_valid(invitation_code):
            flash("Invalid invitation code.", "danger")
            return redirect(url_for('admin.register'))
        
        if register_user(username, password):
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('admin.login'))
        else:
            flash("Registration failed. Username may be taken.", "danger")
            return redirect(url_for('admin.register'))
    
    return render_template('admin/register.html')
