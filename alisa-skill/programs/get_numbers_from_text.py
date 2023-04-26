def numbers_from_linear(eq, pl=0):
    eq = (eq.lower()).strip()
    k, b = '', ''
    try:
        if 'равно' not in eq:
            raise Exception
        eq = eq.split('равно')

        eq[pl] = eq[pl].replace(' ', '')
        ind = eq[pl].find('икс')
        for i in range(ind - 1, -1, -1):
            if not eq[pl][i].isalpha():
                k += eq[pl][i]
            else:
                break
        for i in range(ind + 3, len(eq[0])):
            if not eq[pl][i].isalpha():
                b += eq[pl][i]
            else:
                break
    except Exception:
        try:
            eq = eq.split('=')
            eq[pl] = eq[pl].replace(' ', '')
            ind = eq[pl].find('x')
            if ind == -1:  # проверка на алфавит
                ind = eq[pl].find('х')
            for i in range(ind - 1, -1, -1):
                if not eq[pl][i].isalpha():
                    k += eq[pl][i]
                else:
                    break
            for i in range(ind + 1, len(eq[0])):
                if not eq[pl][i].isalpha():
                    b += eq[pl][i]
                else:
                    break
        except Exception:
            pass
    if b == '':
        b = '0'
    if k == '-':
        k = '1-'
    if k == '+':
        k = '1+'
    if k == '':
        k = '1'

    return int(k[::-1]), int(b)


def numbers_from_square(eq, pl=0):
    eq = (eq.lower()).strip()
    a, b, c = '', '', ''
    try:
        if 'равно' not in eq:
            raise Exception
        eq = eq.split('равно')
        eq[pl] = eq[pl].replace(' ', '')
        ind = eq[pl].find('икс-квадрат')
        for i in range(ind - 1, -1, -1):
            if not eq[pl][i].isalpha():
                a += eq[pl][i]
            else:
                break
        for i in range(ind + 11, len(eq[0])):
            if not eq[pl][i].isalpha():
                b += eq[pl][i]
            else:
                break
        ind = eq[pl].rfind('икс')
        for i in range(ind + 3, len(eq[0])):
            if not eq[pl][i].isalpha():
                c += eq[pl][i]
            else:
                break
    except Exception:
        try:
            eq = eq.split('=')
            eq[pl] = eq[pl].replace(' ', '')
            ind = eq[pl].find('x^2')
            if ind == -1:  # проверка на алфавит
                ind = eq[pl].find('х^2')
            for i in range(ind - 1, -1, -1):
                if not eq[pl][i].isalpha():
                    a += eq[pl][i]
                else:
                    break
            for i in range(ind + 3, len(eq[0])):
                if not eq[pl][i].isalpha():
                    b += eq[pl][i]
                else:
                    break
            ind = eq[pl].rfind('x')
            if ind == -1:  # проверка на алфавит
                ind = eq[pl].rfind('х')
            for i in range(ind + 1, len(eq[0])):
                if not eq[pl][i].isalpha():
                    c += eq[pl][i]
                else:
                    break
        except Exception:
            pass
    if a == '-':
        a = '1-'
    if not a:
        a = '1'
    if not c:
        c = '0'
    if c == '':
        c = '0'
    if b == '+':
        b = '+1'
    if b == '-':
        b = '-1'
    return int(a[::-1]), int(b), int(c)
