from passIt_V1 import db, create_app

db.create_all(app=create_app())
# passing the create_app result so Flask-SQLAlchemy gets the configuration.