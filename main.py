from flask import Flask, request, jsonify
from pprint import pprint
from programmes.nod import nod
from programmes.equations import *
from programmes.get_numbers_from_text import numbers_from_linear
import logging

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
    if 'уравнение' in req['request']['nlu']['tokens']:
        if 'линейное' in req['request']['nlu']['tokens']:
            koef = numbers_from_linear(req['request']['command'])
            answer = linear_equations(koef[0], koef[1])
            res['response']['text'] = f'Ответ {answer}'
        return

    res['response']['text'] = 'я тебя не понимаю'


if __name__ == '__main__':
    app.run()