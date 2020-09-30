import json
from datetime import timedelta, datetime

from .models.database.sql_models import Message, Room

from flask import Flask, render_template, redirect, url_for, Blueprint, request
from Wavelength import db

apiBlueprint = Blueprint('api', __name__)

@apiBlueprint.route("/create")
def create():
    room = Room()
    db.session.add(room)
    db.session.commit()

    return room.token, 200