from app import app
from db import db
db.init_app(app)
tables_created = False

# Function to create tables before the first request
@app.before_request
def create_tables_if_needed():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True
