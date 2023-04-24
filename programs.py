from math import sqrt
from math import pi

def get_divider(a, format=dict()):
    book = {}
    with open('simple_numbers.txt', 'r') as file:
        while True:
            number = int(file.readline())
            if number > a or a == 1:
                break
            while a % number == 0:
                if book.get(number): book[number] += 1
                else: book[number] = 1
                a //= number
    if format == str():
        answer = 'Простые делители: '
        check = True
        for i in book.keys():
            x = book.get(i)
            if i > 0:
                if check:
                    check = False
                else:
                    answer +=', '
            if x > 1:
                answer += f'{i} ^ {x}'
            elif x == 1:
                answer += f'{i}'
        return answer
    if format == dict():
        return book


def sqrt_irrational(a, format=list()):
    global numbers
    book = get_divider(a)
    answer = [1, 1]
    for i in book.keys():
        x = book[i]
        answer[0] *= i ** (x // 2)
        answer[1] *= i ** (x % 2)
    if format == str():
        strn = ''
        if answer[0] == 1:
            if answer[1] == 1:
                return 1
            else:
                return f'корень из {answer[1]}'
        else:
            if answer[1] == 1:
                return answer[0]
            else:
                return f'{answer[0]} корней из {answer[1]}'
    if format == list():
        return answer


def fraction(a, b, format=tuple):
    check1 = False
    check2 = False
    if a < 0:
        check1 = True
        a = abs(a)
    if b < 0:
        check2 = True
        b = abs(b)
    book1 = get_divider(a)
    book2 = get_divider(b)
    for i in book1.keys():
        while book2.get(i) and book1[i] > 0 and book2[i] > 0:
            book1[i] -=1
            book2[i] -=1
    a = 1
    b = 1
    if check1: a = -1
    if check2: b = -1
    for i in book1.keys():
        x = book1[i]
        a *= i ** x
    for i in book2.keys():
        x = book2[i]
        b *= i ** x
    if a < 0 and b < 0:
        a, b = abs(a), abs(b)
    if a > 0 and b < 0:
        a, b = -a, abs(b)
    if format == str():
        if b == 1:
            return a
        return f'{a} / {b}'
    if format == tuple:
        return a, b


def gcd(a, b):
    if a <= 0 or b <= 0:
        return 'ошибка ввода'
    if a % b == 0:return b
    if b % a == 0:return a
    if a > b: return gcd(a % b, b)
    return gcd(b % a, a)


def scm(a, b):
    if a <= 0 or b <= 0:
        return 'ошибка ввода'
    return a * b // gcd(a, b)


def linear_equations(k, b):
    if k == 0:
        if b == 0:
            return 'любое число'
        return 'корней нет'
    return fraction(-b, k, format=str())


def quadratic_equations(a, b, c, format=str()):
    if a == 0:
        return linear_equations(b, c)
    D = b ** 2 - 4 * a * c
    if D == 0:
        if format == str():
            return fraction(-b, 2 * a)
        else:
            return fraction(-b, 2 * a, format=tuple())
    if D < 0:
        if format == str():
            return 'корней нет'
        else:
            return ()
    sqrtD = sqrt_irrational(D)
    if sqrtD[1] == 1:
        sqrtD = sqrtD[0]
        x1 = fraction(-b + sqrtD, 2 * a, format=str())
        x2 = fraction(-b - sqrtD, 2 * a, format=str())
        if format == str():
            return f'корни: {x1}, {x2}'
        else:
            return (x1 ,x2)
    else:
        x1 = (f'{-b} + {sqrtD} / {2 * a}')
        x2 = (f'{-b} - {sqrtD} / {2 * a}')
        if format == str():
            return f'корни: {x1}, {x2}'
        else:
            return (x1 ,x2)
    

def quadratic_function(a, b, c):
    if a == 0:
        linear_function(b, c)
    book = {
            'область определения': 'бесконечность',
            'нули': quadratic_equations(a, b, c, format=tuple()),
            'промежутки знакопостоянства':[0, 0], # список первый элемент когда функция больше нуля, второй когда меньше
            'монотонность' :[0, 0], # список первый элемент - промежутки возрастания, второй - убывания
            'четность': 'четная',
            'периодичность': 'непериодиченская',
            'непрерывность' : 'непрерывная',
            'ограниченность': '',
            'экстримальные значения': '', # набольшее и наименьшие значения функции
            'область значений': 'бесконечность'
        }
    if a > 0:
        if book['нули']:
            zero = book['нули']
            if len(zero) == 1:
                string = f'y > 0 при x != {zero[0]}'
                book['промежутки знакопостоянства'] = string
            else:
                string = f'y > 0 при x < {zero[0]} или x > {zero[1]}; y < 0 при {zero[0]} < x < {zero[1]} '
                book['промежутки знакопостоянства'] = string
                
        else:
            string = f'y > 0 при любом X'
            book['промежутки знакопостоянства'] = string
        string = f'Функция убывает при x <= {fraction(-b/(2*a))}; возрастает при x >= {fraction(-b/(2*a))}'
        book['монотонность'] = string
        book['ограниченность'] = 'ограничена снизу'
        book['экстримальные значения'] = f'наибольшего значения не  существует, наименьшее y={fraction(-b**2 / (4 * a))}'
    if a < 0:
        if book['нули']:
            zero = book['нули']
            if len(zero) == 1:
                string = f'y < 0 при x != {zero[0]}'
                book['промежутки знакопостоянства'] = string
            else:
                string = f'y > 0 при {zero[0]} < x < {zero[1]}; y < 0 при x < {zero[0]} или x > {zero[1]}'
                book['промежутки знакопостоянства'] = string
        else:
            string = f'y < 0 при любом X'
            book['промежутки знакопостоянства'] = string
        string = f'Функция возрастает при x <= {fraction(-b/(2*a))}; убывает при x >= {fraction(-b/(2*a))}'
        book['монотонность'] = string
        book['ограниченность'] = 'ограничена сверху'
        book['экстримальные значения'] = f'наибольшее значение y={fraction(-b**2 / (4 * a))}, наименьшее значенияя не существует'

        
def linear_function(k, b):
    book = {
            'область определения': 'бесконечность',
            'нули': linear_equations(k, b),
            'промежутки знакопостоянства':[0, 0], # список первый элемент когда функция больше нуля, второй когда меньше
            'монотонность' :[0, 0], # список первый элемент - промежутки возрастания, второй - убывания
            'четность': 'нечетная',
            'периодичность': 'непериодиченская',
            'непрерывность' : 'непрерывная',
            'ограниченность': 'неограничена',
            'экстримальные значения': 'наибольшего и наименьшего значений не существует', # набольшее и наименьшие значения функции
            'область значений': 'бесконечность'
        }
    if k == 0:
        return f'прямая y={-b}'
    elif k > 0:
        zero = book['нули']
        string = f'y > 0 при x > {zero}; y < при x < {zero}'
        book['промежутки знакопостоянства'] = string
        book['монотонность'] = f'функция монотонно возрастает'

    elif k < 0:
        zero = book['нули']
        string = f'y > 0 при x < {zero}; y < при x > {zero}'
        book['промежутки знакопостоянства'] = string
        book['монотонность'] = f'функция монотонно убывает'
    return book


def area_of_the_triangle(a, b, c):
    if not (a + b < c and a + c < b and b + c < a): return 'треугольник не существует'
    p = (a + b + c)/ 2
    return sqrt(p * (p - a) * (p - b) * (p - c))


def area_of_the_quadrilateral(a, b, c, d):
    p = (a + b + c + d) / 2
    return sqrt((p - a) * (p - b) * (p - c) * (p - d))


def area_of_the_circle(r):
    return pi * r ** 2

