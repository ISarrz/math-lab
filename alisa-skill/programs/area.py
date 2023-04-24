from math import sqrt
from math import pi


def area_of_the_triangle(a, b, c):
    if not (a + b > c and a + c > b and b + c > a): return 'треугольник не существует'
    p = (a + b + c)/ 2
    return sqrt(p * (p - a) * (p - b) * (p - c))


def area_of_the_quadrilateral(a, b, c, d):
    p = (a + b + c + d) / 2
    return sqrt((p - a) * (p - b) * (p - c) * (p - d))


def area_of_the_circle(r):
    return pi * r[0] ** 2