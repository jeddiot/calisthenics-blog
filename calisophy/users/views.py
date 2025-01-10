from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

from calisophy import db
from calisophy.models import User, BlogPost
from calisophy.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from calisophy.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

@users.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        # Check if the email is already registered
        email_exists = User.query.filter_by(email=form.email.data).first()
        if email_exists:
            flash("Email is already in use. Please choose a different one.", 'danger')

        # Check if the username is already taken
        username_exists = User.query.filter_by(username=form.username.data).first()
        if username_exists:
            flash("Username is already taken. Please choose a different one.", 'danger')
        
        # If either email or username exists, redirect back to register page
        if email_exists or username_exists:
            return redirect(url_for('users.register'))

        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registrated successfully.", 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form = form)

@users.route('/logout')
@login_required # return to login page if not logged in
def logout():
    logout_user()
    flash("Logged out successfully.", 'success')
    return redirect(url_for('core.index'))

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Retrieve user by username
        # user = User.query.filter_by(username=form.username.data).first()
        user = User.query.filter_by(email = form.email.data).first()

        if user is None:
            # If the email does not exist in the database
            flash('Invalid username or password', 'danger')
            return redirect(url_for('users.login'))

        # If the email exists but the password is incorrect
        if not user.check_password(form.password.data):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('users.login'))
        
        # Check password only if user exists
        if user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next = request.args.get('next')  # The page the user was visiting before logging in

            if not next or next[0] == '/':
                next = url_for('core.index')
            
            return redirect(next)

    return render_template('login.html', form=form)

@users.route('/account', methods = ['GET', 'POST'])
@login_required 
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User account updated.', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename = 'profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image = profile_image, form = form)

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author = user).order_by(BlogPost.date.desc()).paginate(page = page, per_page = 5)
    return render_template('user_blog_posts.html', blog_posts = blog_posts, user = user)