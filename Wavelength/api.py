import json
from datetime import timedelta, datetime

from .models.database.sql_models import Message, Room

from flask import Flask, render_template, redirect, url_for, Blueprint, request
from Wavelength import db
from flask_cors import CORS, cross_origin

apiBlueprint = Blueprint('api', __name__)

@apiBlueprint.route("/create")
@cross_origin()
def create():
    room = Room()
    db.session.add(room)
    db.session.commit()

    return room.token, 200
