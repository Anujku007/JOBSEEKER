from flask import Blueprint, jsonify
from extensions import db
from models.simple_models import User, Job, SavedJob  # Make sure these imports are correct

debug_bp = Blueprint('debug_bp', __name__)

@debug_bp.route('/users')
def debug_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'email': u.email} for u in users])

@debug_bp.route('/tables')
def debug_tables():
    # Simple debug route without complex imports
    return jsonify({'message': 'Debug routes working'})