from dotenv import load_dotenv
load_dotenv()  # ✅ Load environment variables before anything else

from flask import Flask, render_template, g, request
from config import Config
from extensions import db, login_manager
from datetime import timedelta
import os
import time
import jobapi_client


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # -------------------------------------------------------
    # Session Configuration
    # -------------------------------------------------------
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=1)

    # -------------------------------------------------------
    # Initialize Extensions
    # -------------------------------------------------------
    db.init_app(app)
    login_manager.init_app(app)

    # Login Manager Setup
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.session_protection = "strong"

    # -------------------------------------------------------
    # Load User for Flask-Login
    # -------------------------------------------------------
    from models.simple_models import User

    @login_manager.user_loader
    def load_user(user_id):
        try:
            print(f"🔍 Loading user with ID: {user_id}")
            user = db.session.get(User, int(user_id))  # ✅ SQLAlchemy 2.0 compatible
            print(f"✅ User loaded: {user}")
            return user
        except Exception as e:
            print(f"❌ Error loading user {user_id}: {e}")
            return None

    # -------------------------------------------------------
    # Request Performance Timer
    # -------------------------------------------------------
    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def end_timer(response):
        if hasattr(g, "start_time"):
            g.request_time = round(time.time() - g.start_time, 3)
        return response

    # -------------------------------------------------------
    # Register Blueprints
    # -------------------------------------------------------
    from routes.main_routes import main_bp
    from routes.job_routes import jobs_bp
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")

    # -------------------------------------------------------
    # About Page
    # -------------------------------------------------------
    @app.route("/about")
    def about():
        """Render the About Us page."""
        return render_template("about.html")

    # -------------------------------------------------------
    # Health Check Route (optional)
    # -------------------------------------------------------
    @app.route("/ping")
    def ping():
        """Quick health check endpoint."""
        return {"status": "ok", "message": "JobSeeker backend running", "time": time.ctime()}

    return app


# -------------------------------------------------------
# ✅ Make app globally available for Gunicorn / Render
# -------------------------------------------------------
app = create_app()

# -------------------------------------------------------
# Main Entry Point (for local development)
# -------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            from sqlalchemy import inspect

            print(f"📁 Using database: {app.config['SQLALCHEMY_DATABASE_URI']}")
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print("📊 Database tables:", tables)

            if "user" in tables:
                columns = inspector.get_columns("user")
                print("📋 User table columns:")
                for column in columns:
                    print(f"   - {column['name']} ({column['type']})")
            else:
                print("⚠️ User table not found!")
        except Exception as e:
            print(f"⚠️ Error initializing database: {e}")

    # -------------------------------------------------------
    # Startup Logs
    # -------------------------------------------------------
    print("\n" + "=" * 60)
    print("🚀 JOBSEEKER Flask Application Starting...")
    print(f"🔑 Mantiks API Connected: {bool(os.getenv('MANTIKS_API_KEY'))}")
    print("📍 Access your application at: http://localhost:5000")
    print("🔐 Authentication system ready ✅")
    print("💾 Database initialized successfully ✅")
    print("=" * 60 + "\n")

    try:
        app.run(debug=True, port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped manually. Goodbye!")
