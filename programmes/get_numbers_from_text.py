def numbers_from_linear(eq):
    eq = (eq.lower()).strip()
    k, b = '', ''
    try:
        eq = eq.split('равно')

        eq[0] = eq[0].replace(' ', '')
        ind = eq[0].find('икс')
        for i in range(ind - 1, -1, -1):
            if not eq[0][i].isalpha():
                k += eq[0][i]
            else:
                break
        for i in range(ind + 3, len(eq[0])):
            if not eq[0][i].isalpha():
                b += eq[0][i]
            else:
                break
    except Exception:
        pass
    if not b:
        b = 0
    if k == '-':
        k = '1-'
    if k == '+':
        k = '1+'
    if not k:
        k = '1'

    return int(k[::-1]), int(b)


def numbers_from_square(eq):
    eq = (eq.lower()).strip()
    a, b, c = '', '', ''
    try:
        eq = eq.split('равно')
        eq[0] = eq[0].replace(' ', '')
        ind = eq[0].find('икс-квадрат')
        for i in range(ind - 1, -1, -1):
            if not eq[0][i].isalpha():
                a += eq[0][i]
            else:
                break
        for i in range(ind + 11, len(eq[0])):
            if not eq[0][i].isalpha():
                b += eq[0][i]
            else:
                break
        ind = eq[0].rfind('икс')
        for i in range(ind + 3, len(eq[0])):
            if not eq[0][i].isalpha():
                c += eq[0][i]
            else:
                break
        print(ind)
    except Exception:
        pass
    if a == '-':
        a = '1-'
    if not a:
        a = '1'
    if not c:
        c = '0'
    if b == '+':
        b = '+1'
    if b == '-':
        b = '-1'
    return int(a[::-1]), int(b), int(c)
