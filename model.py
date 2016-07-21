"""Database for Pencil Me In"""

from flask_sqlalchemy import SQLAlchemy
import bcrypt
import os

from flask import Flask

db = SQLAlchemy()


#Model definitions 
##############################################################################

class User(db.Model):
	"""User info"""

	__tablename__ = 'users'

	user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	email = db.Column(db.String(64), nullable=True)
	password = db.Column(db.String(64), nullable=True)
	first_name = db.Column(db.String(20), nullable=True)
    list_name = db.Column(db.String(20), nullable=True)
    salt = db.Column(db.String(50), nullable=True)

    user_image = db.relationship('UserImage', uselist = False, backref=db.backref("users"))


    def __init__(self, email, password, first_name, list_name):
        """initializer"""

        self.salt = bcrypt.gensalt()
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), self.salt)
        self.first_name = first_name
        self.last_name = last_name

    def verify_password(self, password):
        """verifies user's password"""

        # return self.bcrypt.check_password_hash(secret)
        return self.password == bcrypt.hashpw(password.encode('utf-8'), self.salt.encode('utf-8'))

##############################################################################

class UserImage(db.Model):
    """points to direction of users image"""
    __tablename__ = "user_images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    image = db.Column(db.String(1500), nullable=True)



##############################################################################

class Event(db.Model):
    """User's events"""

    ___tablename___ = 'events'

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_title = db.Column(db.String(100), nullable=True)
    event_date = db.Column(db.String(100), nullable=True)
    study_location = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(100), nullable=True)

    event_image = db.relationship('EventImage', uselist = False, backref=db.backref("events"))
    user = db.relationship('User', backref="events")


##############################################################################

class EventImage(db.Model):
    """points to direction of users image"""
    __tablename__ = "event_images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    image = db.Column(db.String(1500), nullable=True)


##############################################################################

class Event_Request(db.Model):
	"""User's events request"""

	___tablename___ = 'event_requests'

	event_request_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
	user_id =  db.Column(db.Integer, db.ForeignKey('users.user_id'))
	event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
	accepted = db.Column(db.Boolean, nullable = True)

    user = db.relationship('User', backref="event_requests")
    event = db.relationship('Event', backref="event_requests")


##############################################################################
 #Helper functions

def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///pencilmein'
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    print "Connected to DB."
    # creates tables in project db
    db.create_all()


	















