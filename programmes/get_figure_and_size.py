def figure(req):
    size = []
    object = ''
    for i in req['request']['nlu']['tokens']:
        check = False
        if 'треугольн' in i:
            object = 'треугольник'
            for i in req['request']['nlu']['entities']:
                if i['type'] == 'YANDEX.NUMBER':
                    size.append(i['value'])
                if len(size) == 3:
                    check = True
                    break
        if 'квадр' in i:
            object = 'квадрат'
            for i in req['request']['nlu']['entities']:
                if i['type'] == 'YANDEX.NUMBER':
                    size.append(i['value'])
                    check = True
                    break
        if 'прямоугол' in i:
            object = 'прямоугольник'
            for i in req['request']['nlu']['entities']:
                if i['type'] == 'YANDEX.NUMBER':
                    size.append(i['value'])
                if len(size) == 2:
                    check = True
                    break
        if 'параллелог' in i:
            object = 'параллелограмм'
            for i in req['request']['nlu']['entities']:
                if i['type'] == 'YANDEX.NUMBER':
                    size.append(i['value'])
                if len(size) == 2:
                    check = True
                    break
        if check:
            break
    return size, object

