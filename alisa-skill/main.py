from flask import Flask, request, jsonify
from programs.nod import nod
from programs.equations import *
from programs.get_numbers_from_text import *
from programs.functions import *
from programs.get_figure_and_size import *
from programs.area import *
import logging
from math import sqrt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'math-l'
logging.basicConfig(level=logging.DEBUG)

sessionStorage = {}
skills = ['Умею вычислять квадратный корень числа\n'
          'Пример запроса:\n'
          '   "Найди квадратный корень числа 36"', 'Могу решить приведённое квадратное и линейное уравнения\n'
                                                   'Чтобы вычислить его укажите(скажите):\n'
                                                   '   1)Тип уравнения: линейное, квадратное\n'
                                                   '   2)Уравнение введите через неизвестную "икс"\n'
                                                   'Пример запроса:\n'
                                                   '   "Реши квадратное уравнение 5x^2+7x+8=0"',
          'Нахожу НОД и НОК 2 чисел\n'
          '   Пример запроса:\n'
          '"Найди НОД(НОК) 5 и 342"', 'По заданной квадратичной или линейной функции, рассказываю её свойства.\n'
                                      'Пример запроса:\n'
                                      '   "Расскажи свойства функции y=5x-9"',
          'Умею вычислять площадь круга, треугольника, квадрата, прямоугольника и выпуклого четырехугольника по 4 сторонам\n'
          'Пример запроса:'
          '     "Найди площадь круга с радиусом 9"',
          'Также я умею находить простые делители числа. Просто скажи: "Найди простые делители числа ..."'
          'На этом пока что всё, но мои навыки будут увеличиваться со временем']


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

    if req['session']['new']:  # Первое знакомство
        res['response'][
            'tts'] = 'Привет, что ты хочешь решить\nЕсли хочешь узнать что я умею, просто спроси: "Что ты умеешь?"'
        res['response'][
            'text'] = 'Привет, что ты хочешь решить\nЕсли хочешь узнать что я умею, просто спроси: "Что ты умеешь?"'
        sessionStorage[user_id] = [0, False]
        return

    if sessionStorage.get(user_id, [''])[1]:
        if ('да' in req['request']['nlu']['tokens'] or 'конечно' in req['request']['nlu']['tokens']) and skills[
            sessionStorage[user_id][0]] != skills[-1]:
            res['response']['text'] = skills[sessionStorage[user_id][0]] + '\nПродолжим?'
            sessionStorage[user_id][0] += 1
            return
        else:
            sessionStorage[user_id] = [0, False]
            res['response'][
                'text'] = 'Что ты хочешь решить'
            return

    if ('умеешь' in req['request']['nlu']['tokens'] or 'можешь' in req['request']['nlu']['tokens']) and ('что' in
                                                                                                         req['request'][
                                                                                                             'nlu'][
                                                                                                             'tokens']):
        res['response']['text'] = skills[0] + '\nПродолжим?'
        sessionStorage[user_id] = [1, True]
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
        if number == '' or number < 0:
            res['response']['text'] = f'Ошибка'
        else:
            res['response']['text'] = f'Корень из {number} = {sqrt(number)}.'
        return
    check = False
    for i in req['request']['nlu']['tokens']:
        if 'уравн' in i:
            check = True
    if check:
        try:
            if 'линейное' in req['request']['nlu']['tokens'] or 'линейного' in req['request']['nlu']['tokens']:
                koef = numbers_from_linear(req['request']['command'], pl=1)
                print(koef)
                answer = linear_equations(koef[0], koef[1])
                res['response']['text'] = f'Ответ: {answer}'
            if 'квадратное' in req['request']['nlu']['tokens'] or 'квадратного' in req['request']['nlu']['tokens']:
                koef = numbers_from_square(req['request']['command'], pl=1)
                answer = quadratic_equations(koef[0], koef[1], koef[2])
                res['response']['text'] = f'{answer}'
            if res['response']['text'] == '':
                raise Exception

        except Exception:
            res['response']['text'] = f'Повторите, пожалуйста'
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
        try:
            if object == 'круг':
                answer = area_of_the_circle(size)
            if object == 'треугольник':
                answer = area_of_the_triangle(*size)
            if object == 'квадрат':
                answer = area_of_the_quadrilateral(size[0], size[0], size[0], size[0])
            if object == 'прямоугольник':
                answer = area_of_the_quadrilateral(size[0], size[1], size[1], size[0])
            res['response']['text'] = f'Площадь {object}a = {answer}.'
        except IndexError:
            res['response']['text'] = 'Вы сказали недостаточное количество чисел для вычисления площади'
        except Exception:
            res['response']['text'] = 'Повторите ещё раз пожалуйста'

        return

    res['response']['text'] = 'я тебя не понимаю'


if __name__ == '__main__':
    app.run()
