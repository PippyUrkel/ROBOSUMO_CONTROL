from flask import Flask, Blueprint, render_template, session
views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('base.html')