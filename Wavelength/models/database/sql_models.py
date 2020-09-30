from datetime import datetime
from uuid import uuid4
from enum import Enum


from Wavelength import db

########## Datatable Models ##########

class Message(db.Model):
    """model for User datatable"""

    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(32), primary_key=False, autoincrement=False, unique=True, nullable=False)

    name = db.Column(db.String(16), primary_key=False, autoincrement=False, unique=True, nullable=False) 
    photo_url = db.Column(db.String(512), primary_key=False, autoincrement=False, unique=True, nullable=False)
    sent_datetime = db.Column(db.DateTime(), primary_key=False, index=True, nullable=False, default=datetime.now())
    text = db.Column(db.Text(64), primary_key=False, autoincrement=False, unique=True, nullable=False)
    
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))

    def __init__(self, firstname, lastname, email, birthday, sex, password, phone, credit=None, membership=None):
        code = uuid4().hex
        while (self.query.filter_by(code=code).all() != []):
            code = uuid4().hex
        self.code = code


class Room(db.Model):
    """model for User datatable"""

    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(32), primary_key=False, autoincrement=False, unique=True, nullable=False)

    token = db.Column(db.String(6), primary_key=False, autoincrement=False, unique=True, nullable=False)

    create_day_time = db.Column(db.DateTime(), primary_key=False, index=True, nullable=False, default=datetime.now())
    video_url = db.Column(db.String(512), primary_key=False, autoincrement=False, nullable=True)

    time_stamp_set_datetime = db.Column(db.DateTime(), primary_key=False, index=True, nullable=False, default=datetime.now())
    time_stamp = db.Column(db.BigInteger(), primary_key=False, index=False, nullable=False, default=0)

    messages = db.relationship('Message', lazy='dynamic')

    is_playing = db.Column(db.Boolean(), index=True, nullable=False, default=False)


    def __init__(self): 
        while (self.query.filter_by(code=token).all() != []):
            token = uuid4().hex
        self.token = token
        code = uuid4().hex
        while (self.query.filter_by(code=code).all() != []):
            code = uuid4().hex
        self.code = code


