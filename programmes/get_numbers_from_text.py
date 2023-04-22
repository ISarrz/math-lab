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
        for i in range(ind + 3, len(eq[0])):
            if not eq[0][i].isalpha():
                b += eq[0][i]
        """ind = 0
        for i in range(len(eq[0])):
            if 'икс' in eq[0][i]:
                ind = i
        k += int(eq[0][ind - 1])
        if eq[0][ind - 2] == '-':
            k *= -1
            eq[0] = ''.join(eq[0])
        ind = eq[0].find('икс')
        b += int(eq[0][ind + 3:ind + 5])"""
    except Exception:
        pass
    return int(k[::-1]), int(b)
