from flask import Flask, request, jsonify
from programmes.nod import nod
from programmes.equations import *
from programmes.get_numbers_from_text import *
from programmes.functions import *
from programmes.get_figure_and_size import *
from programmes.area import *
import logging
from math import sqrt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'math-l'
logging.basicConfig(level=logging.DEBUG)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['tts'] = 'Привет, что ты хочешь решить'
        res['response']['text'] = 'Привет, что ты хочешь решить'
        return
    if 'нод' in req['request']['original_utterance'].lower():
        try:
            a, b = req['request']['nlu']['entities'][-1]['value'], req['request']['nlu']['entities'][-2]['value']
        except Exception as f:
            res['response']['text'] = f'Повтори пожалуйста'

            return
        res['response']['text'] = f'НОД {a} и {b} = {nod(a, b)}'
        res['response']['tts'] = f'НОД {a} и {b} равен {nod(a, b)}'
        return
    if 'нок' in req['request']['original_utterance'].lower():
        try:
            a, b = req['request']['nlu']['entities'][-1]['value'], req['request']['nlu']['entities'][-2]['value']
        except Exception as f:
            res['response']['text'] = f'Повтори пожалуйста'
            return
        res['response']['text'] = f'НОК {a} и {b} = {a * b / nod(a, b)}'
        res['response']['tts'] = f'НОК {a} и {b} равен {a * b / nod(a, b)}'
        return
    if 'корень' in req['request']['nlu']['tokens']:
        yan = req['request']['nlu']['entities']
        number = ''
        for i in yan:
            if i['type'] == 'YANDEX.NUMBER':
                number = i['value']
        if number == '':
            res['response']['text'] = f'Ошибка'
        else:
            res['response']['text'] = f'Корень из {number} = {sqrt(number)}.'
        return
    if 'уравнение' in req['request']['nlu']['tokens']:
        if 'линейное' in req['request']['nlu']['tokens']:
            koef = numbers_from_linear(req['request']['command'])
            answer = linear_equations(koef[0], koef[1])
            res['response']['text'] = f'Ответ: {answer}'
        if 'квадратное' in req['request']['nlu']['tokens']:
            koef = numbers_from_square(req['request']['command'])
            answer = quadratic_equations(koef[0], koef[1], koef[2])
            res['response']['text'] = f'{answer}'
        return
    if 'множители' in req['request']['nlu']['tokens'] or 'делители' in req['request']['nlu']['tokens']:
        number = 0
        for i in req['request']['nlu']['entities']:
            if i['type'] == 'YANDEX.NUMBER':
                number = i['value']
        answer = get_divider(number)
        answer = ' '.join([str(i) for i in answer.keys()])
        res['response']['text'] = f'Простые делители числа {number}: {answer}'
        return
    if 'свойства' in req['request']['nlu']['tokens'] and 'функции' in req['request']['nlu']['tokens']:
        func = ''
        for i in req['request']['nlu']['tokens']:
            if 'линей' in i:
                func = 'линейная'
                break
            if 'квадра' in i:
                func = 'квадратичная'
                break
        if func == '':
            res['response']['text'] = 'Извини, я пока что не знаю такую функцию'
            return
        elif func == 'линейная':
            k, b = numbers_from_linear(req['request']['original_utterance'].lower())
            answer = linear_function(k, b)
        elif func == 'квадратичная':
            a, b, c = numbers_from_square(req['request']['original_utterance'].lower())
            answer = quadratic_function(a, b, c)
        text = ''
        for i, j in answer.items():
            text += f'{i}: {j};\n'

        res['response']['text'] = text
        return
    if 'площадь' in req['request']['nlu']['tokens']:
        size, object = figure(req)
        if object == 'круг':
            answer = area_of_the_circle(size)
        if object == 'треугольник':
            answer = area_of_the_triangle(*size)
        if object == 'квадрат':
            answer = area_of_the_quadrilateral(size[0], size[0], size[0], size[0])
        if object == 'прямоугольник':
            answer = area_of_the_quadrilateral(size[0], size[1], size[1], size[0])
        res['response']['text'] = f'Площадь {object}a = {answer}.'
        return

    res['response']['text'] = 'я тебя не понимаю'


if __name__ == '__main__':
    app.run()
