from flask import render_template, app, flash
from flask import Flask, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField 
from wtforms.validators import DataRequired
from flask import Flask, render_template
import os
import json
from random import randint



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/math-lab')
def index():
    return render_template('index.html')


@app.route('/math-lab/contacts')
def contacts():
    return render_template('contacts.html')


@app.route('/math-lab/info')
def info():
    return render_template('info.html')






if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')