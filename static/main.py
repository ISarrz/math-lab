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


@app.route('/<name>')
@app.route('/index/<name>')
def index(name):
    return render_template('index.html', title=name)

@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', prof=prof)

@app.route('/list_prof/<type>')
def list_prof(type):
    list = ["инженер-исследователь",
            "пилот",
            "строитель",
            "экзобиолог",
            "врач",
            "инженер по терраформированию",
            "климатолог",
            "специалист по радиационной защите",
            "астрогеолог",
            "гляциолог",
            "инженер жизнеобеспечения",
            "метеоролог",
            "оператор марсохода",
            "киберинженер",
            "штурман",
            "пилот дронов"
            ]
    return render_template('list_prof.html', type = type, list=list)

@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    book = {"title": "Ответ",
            "surname": "Watny",
            "name": "Mark",
            "education": "Выше среднего",
            "profession": "штурман марсохода",
            "sex": "male",
            "motivation": "Всегда мечтал застрять на марсе!",
            "ready": True
            }
    return render_template('auto_answer.html', book=book)

class LoginForm(FlaskForm):
    id_au = StringField('id астронавта', validators=[DataRequired()])
    password_au = PasswordField('Пароль астронавта', validators=[DataRequired()])
    id_ca = StringField('id капитана', validators=[DataRequired()])
    password_ca = PasswordField('Пароль капитана', validators=[DataRequired()])
    submit = SubmitField('Доступ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return 'ok'
    return render_template('login.html', title='Аварийный доступ', form=form)

@app.route('/distribution')
def distribution():
    list=[
        "Ридли Скотт",
        "Энди Уир",
        "Венката Капур",
        "Тедди Сандерс",
        "Шон Бин"
    ]
    return render_template('distribution.html', title='Размещение', list=list)

@app.route('/table/<int:age>/<sex>')
def table(age, sex):
    return render_template('table.html', title='Каюта', age=age, sex=sex)

@app.route('/galery', methods=['GET', 'POST'])
def galery():
    IMG_FOLDER = os.path.join('static', 'img')
    app.config['UPLOAD_FOLDER'] = IMG_FOLDER
    with open('static/val.txt', 'r') as file:
        count = int(file.readline().strip())
    list = []
    for i in range(2, count + 1):
        list.append(os.path.join(app.config['UPLOAD_FOLDER'], f'{i}.jpg'))
    
    if request.method == 'POST':
        f = request.files['file']
        count += 1
        with open('static/val.txt', 'w') as file:
            file.write(str(count))
        f.save(f'static/img/{count}.jpg')
        return "Форма отправлена"
    return render_template('galery.html', title='Галерея', list=list)

@app.route('/member')
def member():
    IMG_FOLDER = os.path.join('static', 'img')
    app.config['UPLOAD_FOLDER'] = IMG_FOLDER
    with open("templates/members.json", "rt", encoding="utf8") as f:
        members = json.loads(f.read())['members']
    members = members[randint(0, len(members) - 1)]
    members['photo'] = os.path.join(app.config['UPLOAD_FOLDER'], f'{members["photo"]}')
    members['prof'] = ', '.join(sorted(members['prof']))
    print(render_template('members.html', members=members, title='Личная карточка'))
    return render_template('members.html', members=members, title='Личная карточка')



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')