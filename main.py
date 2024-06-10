from math import sqrt
import numpy as np

def analysis(x_list, y_list ):
    n = len(x_list)

    # Данyые для таблицы X^2 y^2 xy:
    squared_x = [x ** 2 for x in x_list]
    squared_y = [x ** 2 for x in y_list]
    xy_list = [x * y for x, y in zip(x_list, y_list)]

    sum_x_list = sum(x_list)
    sum_y_list = sum(y_list)
    sum_squared_x = sum(squared_x)
    sum_squared_y = sum(squared_y)
    sum_xy_list = sum(xy_list)

    sum_list = [sum_x_list, sum_y_list, sum_squared_x, sum_xy_list, sum_squared_y]

    # Средние значения:
    average_x_list = sum_x_list/n
    average_y_list = sum_y_list/n
    average_squared_x = sum_squared_x/n
    average_squared_y = sum_squared_y/n
    average_xy_list = sum_xy_list/n

    # Для вычисления r находим , Kxy σx, σy:
    k_xy = average_xy_list - average_x_list * average_y_list
    sigma_x = sqrt(average_squared_x - average_x_list ** 2)
    sigma_y = sqrt(average_squared_y - average_y_list ** 2)
    r = k_xy/(sigma_x * sigma_y)

    # Для нахождения a,b вычисляем систему:
    left_equation = np.array([[sum(x_list), len(x_list)], [sum(squared_x), sum(x_list)]])
    right_equation = np.array([sum(y_list), sum(xy_list)])
    a, b = np.linalg.solve(left_equation, right_equation)

    # Данные для построения графика:
    a_list = [0, 100]
    b_list = [a*i + b for i in a_list]

    result = {
        'x_list': x_list,
        'y_list': y_list,

        'squared_x': squared_x,
        'squared_y': squared_y,
        'xy_list': xy_list,
        'sum_list': sum_list,

        'average_x_list': average_x_list,
        'average_y_list': average_y_list,
        'average_squared_x': average_squared_x,
        'average_squared_y': average_squared_y,
        'average_xy_list': average_xy_list,

        'k_xy': k_xy,
        'sigma_x': sigma_x,
        'sigma_y': sigma_y,
        'r': r,

        'a' : round(a, 3),
        'b': round(b, 3),

        'a_list': a_list,
        'b_list': b_list,
    }

    return result

