from flask import Flask, render_template, redirect, url_for, Blueprint, request

homeBlueprint = Blueprint('home', __name__)

@homeBlueprint.route("/")
def home():
    return render_template('home.html')