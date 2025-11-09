from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models.simple_models import User
from forms.auth_forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        print("🔁 User already authenticated, redirecting to home")
        return redirect(url_for('main_bp.home'))
    
    form = RegistrationForm()
    
    print(f"🔍 REGISTER ROUTE - Method: {request.method}")
    
    if form.validate_on_submit():
        print("✅ FORM VALIDATION SUCCESSFUL!")
        print(f"📝 Form data: {form.data}")
        
        try:
            # Check if user already exists
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                print("❌ Email already exists:", form.email.data)
                flash('Email already registered. Please use a different email.', 'error')
                return render_template('auth/register.html', form=form)

            # Generate unique username
            base_username = form.email.data.split('@')[0]
            username = base_username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1

            # Create new user
            user = User(
                username=username,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            print(f"✅ USER CREATED: {user.email}, ID: {user.id}")

            # Auto-login after registration
            session.permanent = True
            login_user(user, remember=True)
            print(f"🔑 USER LOGGED IN: {user.email}")
            
            flash(f'Account created successfully! Welcome, {user.first_name}!', 'success')
            return redirect(url_for('main_bp.home'))

        except Exception as e:
            db.session.rollback()
            flash('Error creating account. Please try again.', 'error')
            print(f"❌ REGISTRATION ERROR: {e}")
    
    elif request.method == 'POST':
        print("❌ FORM VALIDATION FAILED!")
        print(f"📝 Form errors: {form.errors}")
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("🔁 User already authenticated, redirecting to home")
        return redirect(url_for('main_bp.home'))
    
    form = LoginForm()
    
    print(f"🔍 LOGIN ROUTE - Method: {request.method}")
    
    if form.validate_on_submit():
        print("✅ FORM VALIDATION SUCCESSFUL!")
        print(f"📝 Form data: {form.data}")
        
        try:
            user = User.query.filter_by(email=form.email.data).first()
            print(f"🔍 Looking for user: {form.email.data}")
            print(f"👤 User found: {user}")
            
            if user:
                print(f"🔑 Checking password for user: {user.email}")
                if user.check_password(form.password.data):
                    # Set session as permanent
                    session.permanent = True
                    # Login user with remember me
                    login_user(user, remember=form.remember_me.data)
                    print(f"✅ LOGIN SUCCESSFUL: {user.email}")
                    
                    next_page = request.args.get('next')
                    flash(f'Welcome back, {user.first_name}!', 'success')
                    return redirect(next_page) if next_page else redirect(url_for('main_bp.home'))
                else:
                    flash('Login failed. Please check your email and password.', 'error')
                    print("❌ PASSWORD INCORRECT")
            else:
                flash('Login failed. Please check your email and password.', 'error')
                print("❌ USER NOT FOUND")

        except Exception as e:
            flash('Error during login. Please try again.', 'error')
            print(f"❌ LOGIN ERROR: {e}")
    
    elif request.method == 'POST':
        print("❌ FORM VALIDATION FAILED!")
        print(f"📝 Form errors: {form.errors}")
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    print(f"👋 User logging out: {current_user.email}")
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main_bp.home'))