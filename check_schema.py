from app import create_app
from extensions import db
from sqlalchemy import inspect

def check_schema():
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("📊 CURRENT DATABASE SCHEMA:")
        print("=" * 50)
        
        for table_name in tables:
            print(f"\n📋 Table: {table_name}")
            columns = inspector.get_columns(table_name)
            for column in columns:
                print(f"   └─ {column['name']} ({column['type']})")
            
            # Print foreign keys
            foreign_keys = inspector.get_foreign_keys(table_name)
            for fk in foreign_keys:
                print(f"   └─ FK: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")

if __name__ == "__main__":
    check_schema()