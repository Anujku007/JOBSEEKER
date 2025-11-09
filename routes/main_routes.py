from flask import Blueprint, render_template, request
from flask_login import current_user

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    print(f"🏠 Home page accessed - User: {current_user.is_authenticated}")
    if current_user.is_authenticated:
        print(f"   👤 User: {current_user.email}")
    else:
        print("   👤 No user logged in")
    
    # If there are query parameters, it means a form was submitted via GET
    if request.args:
        print(f"   ⚠️  GET parameters detected: {request.args}")
        print("   ⚠️  This suggests forms are submitting via GET instead of POST")
    
    return render_template('index.html')