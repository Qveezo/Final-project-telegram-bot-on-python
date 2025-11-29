from aiogram import Bot, Dispatcher, types, executor  # pip install --force-reinstall -v "aiogram==2.25.2"
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from sympy import *
from sympy.calculus.util import continuous_domain
import requests
# from cairosvg import svg2png
import math
from math import radians
import numpy as np
from scipy.integrate import quad
from scipy.misc import derivative as der
from sdamgia import SdamGIA
from PIL import Image, ImageDraw
import sqlite3
from datetime import *
# from config import TOKEN_API
import random
# import cairo
# import cairosvg
import os

# Документация по AIOGRAM
# https://docs.aiogram.dev/en/latest/contributing.html#guides


bot = Bot('Очень классный токен')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("/calculator"))

sdamgia = SdamGIA()
subject = 'math'



def generate_task() -> list:
    topic = random.randint(1, 12)
    # sdamgia.get_problem_by_topic(subject, topic)
    cat: dict = sdamgia.get_catalog(subject)[topic - 1]
    cat1: dict = cat['categories'][random.randint(0, len(cat['categories']) - 1)]
    ll = sdamgia.get_category_by_id(subject, cat1['category_id'])
    idtask = ll[random.randint(0, len(ll) - 1)]
    # print(topic, idtask)
    print(1)
    scr:int = 0
    if(topic >= 1 and topic <= 4 or topic == 6 or topic == 7 or topic == 10): scr = 1
    elif(topic == 5 or topic == 8 or topic == 9 or topic == 11 or topic == 12): scr = 2
    return [sdamgia.get_problem_by_id(subject, idtask)['answer'],
            sdamgia.get_problem_by_id(subject, idtask)['condition'], scr]


connection = sqlite3.connect('data.db')
cursor = connection.cursor()

calculatorkb = InlineKeyboardMarkup(row_width=3)
calculatorkb.row(InlineKeyboardButton(text="Производная", callback_data='derivative'),
                 InlineKeyboardButton(text="Интеграл", callback_data='integral'),
                 InlineKeyboardButton(text="Разложение в ряд Тейлора", callback_data='taylorseq'))
calculatorkb.row(InlineKeyboardButton(text="Предел", callback_data='lim'),
                 InlineKeyboardButton(text="Диффуры", callback_data='diffequation'),
                 InlineKeyboardButton(text="Асимптоты", callback_data='asymptotes'))
calculatorkb.row(InlineKeyboardButton(text="Длина кривой", callback_data='lencur'),
                 InlineKeyboardButton(text="Полное исследование", callback_data='full'),
                 InlineKeyboardButton(text="Факториал", callback_data='fact'))
calculatorkb.row(InlineKeyboardButton(text='Логарифм', callback_data='log'),
                 InlineKeyboardButton(text='НОК', callback_data='NOK'),
                 InlineKeyboardButton(text='Степень', callback_data='elevation'))
calculatorkb.row(InlineKeyboardButton(text='Корень', callback_data='sqrt'))


ikb = InlineKeyboardMarkup(row_width=3)  # Установка количества столбцов у клавиатуры
# Создание кнопок (в теории можно было сделать списочное выражение
# [InlineKeyboardButton(text=str(i), callback_data='problem'+str(i) for i in range(1, 20)]
# Но сомневаюсь, нужно ли постоянно запускать такой цикл боту)
ib1 = InlineKeyboardButton(text='1', callback_data='problem1')
ib2 = InlineKeyboardButton(text='2', callback_data='problem2')
ib3 = InlineKeyboardButton(text='3', callback_data='problem3')
ib4 = InlineKeyboardButton(text='4', callback_data='problem4')
ib5 = InlineKeyboardButton(text='5', callback_data='problem5')
ib6 = InlineKeyboardButton(text='6', callback_data='problem6')
ib7 = InlineKeyboardButton(text='7', callback_data='problem7')
ib8 = InlineKeyboardButton(text='8', callback_data='problem8')
ib9 = InlineKeyboardButton(text='9', callback_data='problem9')
ib10 = InlineKeyboardButton(text='10', callback_data='problem10')
ib11 = InlineKeyboardButton(text='11', callback_data='problem11')
ib12 = InlineKeyboardButton(text='12', callback_data='problem12')
ib13 = InlineKeyboardButton(text='13', callback_data='problem13')
ib14 = InlineKeyboardButton(text='14', callback_data='problem14')
ib15 = InlineKeyboardButton(text='15', callback_data='problem15')
ib16 = InlineKeyboardButton(text='16', callback_data='problem16')
ib17 = InlineKeyboardButton(text='17', callback_data='problem17')
ib18 = InlineKeyboardButton(text='18', callback_data='problem18')
ib19 = InlineKeyboardButton(text='19', callback_data='problem19')

ikb.add(ib1, ib2, ib3, ib4, ib5, ib6, ib7, ib8, ib9, ib10, ib11, ib12, ib13, ib14, ib15, ib16, ib17, ib18, ib19)


def PNGdraw(name: str, startpos: float, endpos: float, expression, dependvar: str = 'x', mast: int = 50,
            mastcoord: float = 1.0):
    width, height = 860, 480
    image = Image.new("RGB", (width, height), "black")
    maxiY: float = 0.0
    miniY: float = 0.0
    draw = ImageDraw.Draw(image)
    # y axe
    draw.line([(430, 25), (430, 400)], fill="white", width=1)
    draw.line([(431, 25), (431, 400)], fill="grey", width=1)
    # x axe
    draw.line([(25, 230), (835, 230)], fill="white", width=1)
    draw.line([(25, 231), (835, 231)], fill="grey", width=1)
    # arrow on y axe
    draw.line([(430, 25), (425, 35)], fill="white", width=1)
    draw.line([(430, 25), (435, 35)], fill="white", width=1)
    draw.line([(430, 25 + 2), (425, 35 + 2)], fill="grey", width=1)
    draw.line([(430, 25 + 2), (435, 35 + 2)], fill="grey", width=1)
    # arrow on x axe
    draw.line([(835, 230), (825, 225)], fill="white", width=1)
    draw.line([(835, 230), (825, 235)], fill="white", width=1)
    draw.line([(835 - 2, 230), (825 - 2, 225)], fill="grey", width=1)
    draw.line([(835 - 2, 230), (825 - 2, 235)], fill="grey", width=1)
    # draw numbers on y axe
    count: int = (230 - 40) // mast
    for i in range(count):
        draw.line([(425, -(i + 1) * mast + 230), (435, -(i + 1) * mast + 230)], fill="white", width=1)
        draw.line([(425, -(i + 1) * mast + 230 + 1), (435, -(i + 1) * mast + 230 + 1)], fill="grey", width=1)
    count = (400 - 230) // mast
    for i in range(count):
        draw.line([(425, (i + 1) * mast + 230), (435, (i + 1) * mast + 230)], fill="white", width=1)
        draw.line([(425, (i + 1) * mast + 230 + 1), (435, (i + 1) * mast + 230 + 1)], fill="grey", width=1)
    # draw numbers on x axe
    count = (835 - 430 - 40) // mast
    for i in range(count):
        draw.line([((i + 1) * mast + 430, 225), ((i + 1) * mast + 430, 235)], fill="white", width=1)
        draw.line([((i + 1) * mast + 430 + 1, 225), ((i + 1) * mast + 430 + 1, 235)], fill="grey", width=1)
    for i in range(count):
        draw.line([(-(i + 1) * mast + 430, 225), (-(i + 1) * mast + 430, 235)], fill="white", width=1)
        draw.line([(-(i + 1) * mast + 430 + 1, 225), (-(i + 1) * mast + 430 + 1, 235)], fill="grey", width=1)
    # draw graph
    pixelsfor1: float = mast / mastcoord
    maxiY = (230 - 40) / pixelsfor1
    miniY = -(400 - 230) / pixelsfor1
    print(maxiY, miniY)
    stepf: float = 0.03
    for x in np.arange(startpos, endpos, stepf):
        try:
            firstpt: float = expression.subs(dependvar, x) * pixelsfor1
            lastpt: float = expression.subs(dependvar, x + stepf) * pixelsfor1

            # print(continuous_domain(expression, Symbol('x'), Interval(x, x+stepf)))
            if (miniY <= firstpt / pixelsfor1 <= maxiY and miniY <= lastpt / pixelsfor1 <= maxiY):
                if (continuous_domain(expression, Symbol('x'), Interval(x, x + stepf))):
                    draw.line([(430 + x * pixelsfor1, 230 - firstpt), (430 + (x + stepf) * pixelsfor1, 230 - lastpt)],
                              fill="white", width=1)
        except:
            pass
    image.save(name)


class CurrentState(StatesGroup):
    square_a = State()
    square_d = State()
    rect_a = State()
    rect_b = State()
    triang_a = State()
    triang_h = State()
    trape_a = State()
    trape_b = State()
    trape_c = State()
    trape_f = State()
    trape_g = State()
    rhomb_q = State()
    rhomb_w = State()
    rhomb_a = State()
    rhomb_s = State()
    rhomb_z = State()
    rhomb_x = State()
    circle_square_a = State()
    right_triang_q = State()
    right_triang_w = State()
    right_triang_a = State()
    right_triang_s = State()
    right_triang_z = State()
    right_triang_x = State()
    right_triang_c = State()
    pyra_apof_a = State()
    pyra_n1 = State()
    pyra_apof_s = State()
    pyra_n2 = State()
    pyra_n = State()


class Ege:
    ege_1_task = dict()
    ege_1_ans = str()
    ege_2_task = dict()
    ege_2_ans = str()
    ege_3_task = dict()
    ege_3_ans = str()
    ege_4_task = dict()
    ege_4_ans = dict()
    ege_5_task = dict()
    ege_5_ans = str()
    ege_6_task = dict()
    ege_6_ans = str()
    ege_7_task = dict()
    ege_7_ans = str()
    ege_8_task = dict()
    ege_8_ans = str()
    ege_9_task = dict()
    ege_9_ans = str()
    ege_10_ans = str()
    ege_10_task = dict()
    ege_11_task = dict()
    ege_11_ans = str()
    ege_12_task = dict()
    ege_12_ans = str()
    ege_13_task = dict()
    ege_14_task = dict()
    ege_15_task = dict()
    ege_16_task = dict()
    ege_17_task = dict()
    ege_18_task = dict()
    ege_19_task = dict()


class EgeState(StatesGroup):
    ege_1_ans = State()
    ege_2_ans = State()
    ege_3_ans = State()
    ege_4_ans = State()
    ege_5_ans = State()
    ege_6_ans = State()
    ege_7_ans = State()
    ege_8_ans = State()
    ege_9_ans = State()
    ege_10_ans = State()
    ege_11_ans = State()
    ege_12_ans = State()


ege_1_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_1_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                          callback_data='problem1'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_1_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_1_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                          callback_data='problem1-solution'),
                     InlineKeyboardButton(text='Другой вариант этого задания',
                                          callback_data='problem1'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_2_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_2_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                          callback_data='problem2'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_2_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_2_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                          callback_data='problem2-solution'),
                     InlineKeyboardButton(text='Другой вариант этого задания',
                                          callback_data='problem2'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_3_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_3_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                          callback_data='problem3'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_3_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_3_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                          callback_data='problem3-solution'),
                     InlineKeyboardButton(text='Другой вариант этого задания',
                                          callback_data='problem3'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_4_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_4_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание',
                                            callback_data='problem4'),
                       InlineKeyboardButton(text='Назад', callback_data='back'))
ege_4_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_4_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                            callback_data='problem4-solution'),
                       InlineKeyboardButton(text='Другой вариант этого задания',
                                            callback_data='problem4'),
                       InlineKeyboardButton(text='Назад', callback_data='back'))


ege_5_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_5_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                          callback_data='problem5'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_5_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_5_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                          callback_data='problem5-solution'),
                     InlineKeyboardButton(text='Другой вариант этого задания',
                                          callback_data='problem5'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_6_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_6_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                          callback_data='problem6'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_6_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_6_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                          callback_data='problem6-solution'),
                     InlineKeyboardButton(text='Другой вариант этого задания',
                                          callback_data='problem6'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_7_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_7_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задания еще раз',
                                            callback_data='problem7'),
                       InlineKeyboardButton(text='Назад', callback_data='back'))

ege_7_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_7_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                            callback_data='problem7-solution'),
                       InlineKeyboardButton(text='Другой вариант этого задания',
                                            callback_data='problem7'),
                       InlineKeyboardButton(text='Назад', callback_data='back'))


ege_8_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_8_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                            callback_data='problem8'),
                       InlineKeyboardButton(text='Назад', callback_data='back'))

ege_8_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_8_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                            callback_data='problem8-solution'),
                       InlineKeyboardButton(text='Другой вариант этого задания',
                                            callback_data='problem8'),
                       InlineKeyboardButton(text='Назад', callback_data='back'))


ege_9_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_9_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                            callback_data='problem9'),
                       InlineKeyboardButton(text='Назад', callback_data='back'))

ege_9_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_9_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                            callback_data='problem9-solution'),
                       InlineKeyboardButton(text='Другой вариант этого задания',
                                            callback_data='problem9'),
                       InlineKeyboardButton(text='Назад', callback_data='back'))


ege_10_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_10_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                             callback_data='problem10'),
                        InlineKeyboardButton(text='Назад', callback_data='back'))

ege_10_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_10_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                          callback_data='problem10-solution'),
                     InlineKeyboardButton(text='Другой вариант этого задания',
                                          callback_data='problem10'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_11_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_11_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                          callback_data='problem11'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_11_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_11_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                          callback_data='problem11-solution'),
                     InlineKeyboardButton(text='Другой вариант этого задания',
                                          callback_data='problem11'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_12_right_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_12_right_ans_kb.add(InlineKeyboardButton(text='Решить похожее задание еще раз',
                                          callback_data='problem12'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_12_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_12_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                          callback_data='problem12-solution'),
                     InlineKeyboardButton(text='Другой вариант этого задания',
                                          callback_data='problem12'),
                     InlineKeyboardButton(text='Назад', callback_data='back'))


ege_13_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_13_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                             callback_data='problem13-solution'),
                        InlineKeyboardButton(text='Другой вариант этого задания',
                                             callback_data='problem13'),
                        InlineKeyboardButton(text='Назад', callback_data='back'))

ege_14_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_14_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                             callback_data='problem14-solution'),
                        InlineKeyboardButton(text='Другой вариант этого задания',
                                             callback_data='problem14'),
                        InlineKeyboardButton(text='Назад', callback_data='back'))


ege_15_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_15_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                             callback_data='problem15-solution'),
                        InlineKeyboardButton(text='Другой вариант этого задания',
                                             callback_data='problem15'),
                        InlineKeyboardButton(text='Назад', callback_data='back'))

ege_16_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_16_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                             callback_data='problem16-solution'),
                        InlineKeyboardButton(text='Другой вариант этого задания',
                                             callback_data='problem16'),
                        InlineKeyboardButton(text='Назад', callback_data='back'))


ege_17_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_17_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                             callback_data='problem17-solution'),
                        InlineKeyboardButton(text='Другой вариант этого задания',
                                             callback_data='problem17'),
                        InlineKeyboardButton(text='Назад', callback_data='back'))

ege_18_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_18_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                             callback_data='problem18-solution'),
                        InlineKeyboardButton(text='Другой вариант этого задания',
                                             callback_data='problem18'),
                        InlineKeyboardButton(text='Назад', callback_data='back'))

ege_19_wrong_ans_kb = InlineKeyboardMarkup(row_width=2)
ege_19_wrong_ans_kb.add(InlineKeyboardButton(text='Показать ответ и решение',
                                             callback_data='problem19-solution'),
                        InlineKeyboardButton(text='Другой вариант этого задания',
                                             callback_data='problem19'),
                        InlineKeyboardButton(text='Назад', callback_data='back'))


solve_task_list = InlineKeyboardMarkup(row_width=3)
solve_task_list.add(InlineKeyboardButton(text='Площадь квадрата', callback_data='square-square'),
                    InlineKeyboardButton(text='Площадь прямоугольника', callback_data='rect-square'),
                    InlineKeyboardButton(text='Площадь треугольника', callback_data='triang-square'),
                    InlineKeyboardButton(text='Площадь пирамиды', callback_data='pyra-square'),
                    InlineKeyboardButton(text='Площадь трапеции', callback_data='trape-square'),
                    InlineKeyboardButton(text='Площадь ромба', callback_data='rhomb-square'),
                    InlineKeyboardButton(text='Площадь круга', callback_data='circle-square'),
                    InlineKeyboardButton(text='Высота трапеции', callback_data='trape-height'),
                    InlineKeyboardButton(text='Площадь прямоугольного треугольника',
                                         callback_data='right-triang-square')
                    )

square_area_kb = InlineKeyboardMarkup(row_width=2)
square_area_kb.add(InlineKeyboardButton(text='Сторона квадрата', callback_data='square-square-a'),
                   InlineKeyboardButton(text='Диагональ квадрата', callback_data='square-square-d'))

trape_square_kb = InlineKeyboardMarkup(row_width=2)
trape_square_kb.add(InlineKeyboardButton(text='Основания трапеции', callback_data='trape-square-a'),
                    InlineKeyboardButton(text='Средняя линия трапеции', callback_data='trape-square-b'))

rhomb_square_kb = InlineKeyboardMarkup(row_width=3)
rhomb_square_kb.add(InlineKeyboardButton(text='Диагонали ромба', callback_data='rhomb-square-a'),
                    InlineKeyboardButton(text='Сторона и синус угла ромба', callback_data='rhomb-square-b')).add(
    InlineKeyboardButton(text='Cтрона и высота ромба', callback_data='rhomb-square-c'))

right_triang_square_kb = InlineKeyboardMarkup(row_width=3)
right_triang_square_kb.add(InlineKeyboardButton(text='Катеты', callback_data='right-triang-square-a'),
                           InlineKeyboardButton(text='Гипотенуза и высота', callback_data='right-triang-square-b')).add(
    InlineKeyboardButton(text='Сторона, гипотенуза и синус угла', callback_data='right-triang-square-c'))

pyra_square_kb = InlineKeyboardMarkup(row_width=1)
pyra_square_kb.add(InlineKeyboardButton(text='Найти площадь поверхности пирамиды', callback_data='pyra-square-a'))


class TrigonometryState(StatesGroup):
    degree_into_sin = State()
    degree_into_tg = State()
    degree_into_cos = State()
    radian_into_degree = State()
    degree_into_radian = State()
    reduction_formulas = State()


back_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.add(KeyboardButton('Назад'))

infokb = InlineKeyboardMarkup(row_width=3)
infokb.add(InlineKeyboardButton(text='Список комманд', callback_data='cmd-list'),
           InlineKeyboardButton(text='Чем наш бот лучше конкуретов', callback_data='bot-advantages'),
           InlineKeyboardButton(text='Техподдержка', callback_data='tech-support'),
           InlineKeyboardButton(text='Об авторах', callback_data='authors'))


class Requested:
    # choosearg:bool = False
    # listarg:list = list()
    def __init__(self, name: str):
        self.name = name
        # self.active = False

    def calculate(self, func: str, args: list) -> str:
        if (self.name == 'derivative'):
            x = symbols(args[1])
            funccpy: str = func
            try:
                for i in range(int(args[0])):
                    try:
                        derivative: str = simplify(diff(sympify(funccpy), x))
                    except:
                        return "Не удалось продифференцировать"
                    if (str(derivative)[0:10] == "Derivative"):
                        return "Не удалось продифференцировать"
                    funccpy = derivative
            except:
                return "Ошибка"
            answer: str = str(args[0]) + " Производная функции " + str(func) + f" по d{args[1]}^{args[0]} равна " + str(derivative)
            return answer
        elif (self.name == 'integral'):
            x = symbols(args[0])
            try:
                integral: str = simplify(integrate(sympify(func), x))
            except:
                return "Не удалось проинтегрировать или не существует элементарной первообразной"
            if (str(integral)[0:8] == "Integral"):
                return "Не удалось проинтегрировать или не существует элементарной первообразной"
            answer: str = "Интеграл функции " + func + f" по d{args[0]} равен " + str(integral) + " + C"
            return answer
        elif (self.name == 'lim'):
            x = symbols(args[0])
            if (args[1] == "oo" or args[1] == "-oo" or args[1] == '+oo'):
                limit_result = simplify(limit(sympify(func), x, args[1]))
                return "Предел равен " + str(limit_result)
            else:
                limit_result = simplify(limit(sympify(func), x, int(args[1])))
                left_limit = simplify(limit(sympify(func), x, 0, dir='-'))
                right_limit = simplify(limit(sympify(func), x, 0, dir='+'))
            if(args[1][0] == '-'):
                return "Предел равен " + str(left_limit)
            if(args[1][0] == '+'):
                return "Предел равен " + str(right_limit)
            if (left_limit == right_limit == limit_result):
                return "Предел равен " + str(limit_result)
            print(limit_result, left_limit, right_limit)
            return 'Предела не существует.'

        elif (self.name == 'taylorseq'):

            x = symbols(args[0])
            try:
                initpt: int = int(args[2])
                count: int = int(args[1])
                exfunc = sympify(func)
                answ = exfunc.subs(x, initpt)

                for i in range(2, count + 1):
                    answ += exfunc.diff(x, i - 1).subs(x, initpt) * ((x - initpt) ** (i - 1)) / math.factorial(i - 1)
                # answ = simplify(answ)
                if (str(answ) == "nan"): return "Неопределено"
                return "Приближенная функция: " + str(answ)
            except:
                return "Ошибка"
        elif (self.name == "asymptotes"):
            x = symbols(args[0])
            asms: set = set()
            if (simplify(limit(sympify(func), x, +oo)) != +oo and simplify(
                    limit(sympify(func), x, +oo) != -oo)):                asms.add(
                "y = " + str(simplify(limit(sympify(func), x, +oo))))
            if (simplify(limit(sympify(func), x, -oo)) != +oo and simplify(
                    limit(sympify(func), x, -oo) != -oo)):                asms.add(
                "y = " + str(simplify(limit(sympify(func), x, -oo))))

            numerator, denominator = sympify(func).as_numer_denom()
            vertical_asymptotes = solve(denominator, x)
            for i in vertical_asymptotes:                asms.add("x = " + str(i))
            ans: str = "Функция имеет асимптоты:"
            grr: bool = False

            for i in asms:
                grr = True
                ans += (" " + i + " ")
            print(asms)
            if (not (grr)):
                return "Функция не имеет асимптот"
            return ans
        elif (self.name == "factorial"):
            x: int = int(func)
            ans: int = 1
            for i in range(1, x + 1):
                ans *= i
            return f"Факториал {func} равен {ans}"
        elif self.name == 'logarithm':
            try:
                x: int = int(func.split(',')[0])
                a: int = int(func.split(',')[1])
                if a > 0 and a != 1 and x > 0:
                    ans = str(math.log(x, a))
                    return f"Логарифм числа {x} по основанию {a} это {ans}"
                return 'Ошибка'
            except:
                return 'Ошибка'
        elif self.name == 'lengthcurve':
            resp = list(str(args[0]).split())
            x_func_str = resp[0]
            y_func_str = resp[1]
            t_start = int(resp[2])
            t_end = int(resp[3])

            def curve_length(x_func_str, y_func_str, t_start, t_end, num_points=1000):
                # Компиляция строковых представлений функций в лямбда-выражения
                x_func = eval(f"lambda t: {x_func_str}")
                y_func = eval(f"lambda t: {y_func_str}")

                def integrand(t):
                    dx_dt = der(x_func, t, dx=1e-6)
                    dy_dt = der(y_func, t, dx=1e-6)
                    return np.sqrt(dx_dt ** 2 + dy_dt ** 2)
        elif (self.name == 'lcm'):
            x: int = int(func.split(',')[0])
            y: int = int(func.split(',')[1])
            greater = max(x, y)
            while True:
                if ((greater % x == 0) and (greater % y == 0)):
                    lcm = greater
                    break
                greater += 1
            return "НОК равно " + str(lcm)
        elif self.name == 'elevation':
            try:
                a: float = float(func.split(',')[0])
                n: float = float(func.split(',')[1])
                ans: float = float(pow(a, n))
                return f'Число {a} в степени {n} = {ans}'
            except:
                return 'Ошибка'
        elif self.name == 'sqrt':
            try:
                a: float = float(func.split(',')[0])
                n: float = float(func.split(',')[1])
                if a >= 0 and n != 0:
                    ans: float = float(simplify(f'{a} ** (1/{n})'))
                    return f'Корень степени {n} числа {a} = {ans}'
                return 'Ошибка'
            except:
                return 'Ошибка'
        elif self.name == 'diffequation':
            try:
                x = symbols(args[0])
                f = Function(args[1])(x)
                equation = func
                equation = equation.replace('^', '**')
                equation = equation.replace(f"d{args[1]}/d{args[0]}", f"f.diff(x)")
                for i in range(1, 101):
                    equation = equation.replace(f"d**{i}{args[1]}/d{args[0]}**{i}", f"f.diff(x, {i})")
                equation = equation.replace(args[0], 'x')
                equation = equation.replace(args[1], 'f')
                print(equation)
                eq_sympy = Eq(eval(equation), 0)
                solution = dsolve(eq_sympy, f)
                return str(solution)[3:-1:].replace(',', ' =')
            except:
                return str('Ошибка')
        elif (self.name == 'fullanalysis'):
            x = symbols(args[0])
            f = sympify(func)
            varik = ""
            try:
                der = simplify(diff(sympify(func), x))
            except:
                der = 'Производная не найдена'
            critical_points = ""
            try:
                zeros = solve(f, x)
            except:
                zeros = "Нули функции не найдены"
            try:
                zerosX = f.subs(x, 0)
            except:
                zerosX = "Значение функции в нуле не найдены"
            try:
                zeroder = solve(der, x)
            except:
                zeroder = "Точки нули производных не найдены"
            try:
                solgr = solve_univariate_inequality(der > 0, x)
            except:
                solgr = "Промежутки роста функции не найдены"
            try:
                solls = solve_univariate_inequality(der < 0, x)
            except:
                solls = "Промежутки падения функции не найдены"
            if f.subs(x, -x) == f:
                varik = "Четная"
            elif f.subs(x, -x) == -f:
                varik = "Нечетная"
            else:
                varik = "Ни четная, ни нечетная"

            PNGdraw("lll.png", float(args[1]), float(args[2]), sympify(func), str(args[0]), int(args[3]),
                    float(args[4]))
            photo = open('lll.png', 'rb')
            print(photo, "График функции", varik, der, zeros, zerosX, zeroder, solgr, solls)
            return [photo, "График функции", varik, der, zeros, zerosX, zeroder, solgr, solls]


requested: list = list()

requested.append(Requested("derivative"))
requested.append(Requested("integral"))
requested.append(Requested("partderivative"))
requested.append(Requested("taylorseq"))
requested.append(Requested("lim"))
requested.append(Requested("diffequation"))
requested.append(Requested("asymptotes"))
requested.append(Requested("lengthcurve"))
requested.append(Requested("fullanalysis"))
requested.append(Requested("factorial"))
requested.append(Requested('logarithm'))
requested.append(Requested("lcm"))
requested.append(Requested('elevation'))
requested.append(Requested('sqrt'))

teorems_back_kb = InlineKeyboardMarkup(row_width=1)
kb = ReplyKeyboardMarkup(resize_keyboard=True)
teorems_kb = InlineKeyboardMarkup(row_width=14)

teorems_kb1 = InlineKeyboardButton(text='Квадрат', callback_data='f_Кв')
teorems_kb2 = InlineKeyboardMarkup(text='Куб', callback_data='f_Куб')
teorems_kb3 = InlineKeyboardMarkup(text='Ромб', callback_data='f_Ромб')
teorems_kb4 = InlineKeyboardMarkup(text='Пирамида', callback_data='f_Пирам')
teorems_kb5 = InlineKeyboardMarkup(text='Треугольник', callback_data='f_Треугл')
teorems_kb6 = InlineKeyboardMarkup(text='Параллелограмм', callback_data='f_Параллгр')
teorems_kb7 = InlineKeyboardMarkup(text='Трапеция', callback_data='f_Трапец')
teorems_kb8 = InlineKeyboardMarkup(text='Конус', callback_data='f_Конус')
teorems_kb9 = InlineKeyboardMarkup(text='Окружность', callback_data='f_Окр')
teorems_kb10 = InlineKeyboardMarkup(text='Сфера', callback_data='f_Сф')
teorems_kb11 = InlineKeyboardMarkup(text='Прямогульник', callback_data='f_Прям')
teorems_kb12 = InlineKeyboardMarkup(text='Параллелипипед', callback_data='f_Параллпд')
teorems_kb13 = InlineKeyboardMarkup(text='n-угольная призма', callback_data='f_n-при')
teorems_kb14 = InlineKeyboardMarkup(text='Правильный n-угольник', callback_data='f_n-угл')
teorems_back_kb1 = InlineKeyboardMarkup(text='Назад', callback_data='f_back')

kb.add(KeyboardButton('ЕГЭ')).add(KeyboardButton('Формулы-Теоремы')).add(KeyboardButton('Решить задачу')).add(
    KeyboardButton('Калькулятор')).add(KeyboardButton('Информация')).add(KeyboardButton('Тригонометрия')).add(
    KeyboardButton('Игра “кто быстрей решит задачу”')).add(KeyboardButton('Таблица лидеров')).add(KeyboardButton('Профиль пользователя'))
teorems_kb.add(teorems_kb1, teorems_kb2).add(teorems_kb3, teorems_kb4).add(teorems_kb5, teorems_kb6).add(teorems_kb7,
                                                                                                         teorems_kb8).add(
    teorems_kb9, teorems_kb10).add(teorems_kb11, teorems_kb12).add(teorems_kb13).add(teorems_kb14)
teorems_back_kb.add(teorems_back_kb1)


def get_task(category_id: int) -> dict:
    """
    Функция принимает номер задания из ЕГЭ по математике и возвращает случайное задание
    в виде словаря
    :param category_id: номер задания
    """
    problems = {category_id: 1}
    test = sdamgia.generate_test(subject, problems)
    task_id = sdamgia.get_test_by_id(subject, test)[0]
    task = sdamgia.get_problem_by_id(subject, task_id)
    return task


async def message_url(task: dict, message: types.CallbackQuery | types.Message) -> None:
    """
    Функция отправляет в чат сообщение с ссылкой на конкретное задание
    :param task: задание - словарь, получаемый функцией get_task()
    :param message: просто передать callback_query
    """
    url = task.get('url')
    await bot.send_message(chat_id=message.from_user.id,
                           text='В случае некорректного'
                                ' отображения условия или'
                                ' решения, воспользуйтесь '
                                f'данной ссылкой: {url}')


@dp.message_handler(text='Назад')
async def cmd_back(message: types.Message or types.CallbackQuery):
    await bot.send_message(chat_id=message.from_user.id, text='Выберите команду:', reply_markup=kb)


@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Добро пожаловать!', reply_markup=kb)
    await message.delete()  # Удалить сообщение пользователя

@dp.message_handler(commands=['register'])
async def start_func(message: types.Message):
    try:
        cursor.execute("""INSERT INTO Players VALUES (?, 0, 0, 0, 0, 0, 0)""", (message.chat.id,))
        connection.commit()
        await bot.send_message(chat_id=message.from_user.id, text='Регистрация прошла успешно!', reply_markup=kb)
    except:
        await bot.send_message(chat_id=message.from_user.id, text='Вы уже зарегистированы!', reply_markup=kb)
    await message.delete()  # Удалить сообщение пользователя

@dp.message_handler(commands=['Калькулятор'])
async def calc_func(message: types.Message):
    await message.answer(text='Калькулятор. Выберите опцию:', reply_markup=calculatorkb)
    await message.delete()


@dp.callback_query_handler(lambda query: query.data == "derivative")
async def derivative_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Напишите порядок и зависимую переменную.', reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if(i.name == 'derivative'):
    # Requested.choosearg = True
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, TRUE, "", "derivative")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "integral")
@dp.message_handler(text=['Интеграл'])
async def integral_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Напишите зависимую переменную.', reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if(i.name == 'integral'):
    # Requested.choosearg = True
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, TRUE, "", "integral")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "lim")
@dp.message_handler(text=['Предел'])
async def integral_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Напишите зависимую переменную предельного перехода и ее предел.',
                         reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if(i.name == 'lim'):
    # Requested.choosearg = True
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, TRUE, "", "lim")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "taylorseq")
@dp.message_handler(text=['Разложение в ряд Тейлора'])
async def integral_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Напишите зависимую перменную, число слагаемых и начальную точку.',
                         reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if(i.name == 'taylorseq'):
    # Requested.choosearg = True
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, TRUE, "", "taylorseq")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "asymptotes")
@dp.message_handler(text=['Асимптоты'])
async def integral_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Напишите зависимую переменную.', reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if(i.name == 'asymptotes'):
    # Requested.choosearg = True
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, TRUE, "", "asymptotes")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "fact")
@dp.message_handler(text=['Факториал'])
async def fact_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Напишите подфакториальное число', reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if(i.name == 'factorial'):
    # Requested.choosearg = False
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, FALSE, "", "factorial")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "log")
@dp.message_handler(text=['Логарифм'])
async def log_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Напишите аргумент (число, которое нужно получить при возведении в логарифм) и '
                              'основания логарифма через запятую.',
                         reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if i.name == 'logarithm':
    # Requested.choosearg = False
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, FALSE, "", "logarithm")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "lencur")
@dp.message_handler(text=['Длина кривой'])
async def curve_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(
        text='Напишите две параметрические функции и границы кривой через пробел в формате (фукнция1 функция2 граница1 граница2).',
        reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if i.name == 'lengthcurve':
    # Requested.choosearg = True
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, TRUE, "", "lengthcurve")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "NOK")
@dp.message_handler(text=['НОК'])
async def lcm_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Напишите два числа через запятую.',
                         reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if(i.name == 'lcm'):
    # Requested.choosearg = False
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, FALSE, "", "lcm")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "elevation")
async def elev_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Отправьте число и степень, в которую необходимо возвести'
                              ' число через запятую', reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if i.name == 'elevation':
    # Requested.choosearg = False
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, FALSE, "", "elevation")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "sqrt")
async def sqrt_func(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Отправьте число и степень извлечения корня через запятую")
    #await message.answer(text='Отправьте число и степень извлечения корня через запятую',
    #                     reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if i.name == 'sqrt':
    # Requested.choosearg = False
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (callback_query.message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, FALSE, "", "sqrt")""", (callback_query.message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "diffequation")
async def diffequation_func(callback_query):
    message:types.Message = callback_query.message
    await message.answer(text='Отправьте имя аргумента и функцию',
                         reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if i.name == 'diffequation':
    # Requested.choosearg = True
    # i.active = True
    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, TRUE, "", "diffequation")""", (message.chat.id,))
        connection.commit()


@dp.callback_query_handler(lambda query: query.data == "full")
async def fullanal_func(callback_query):

    message:types.Message = callback_query.message
    cursor.execute("""SELECT id FROM Players WHERE subscr == 1 AND id == ?""", (message.chat.id,))
    ids:list = cursor.fetchall()
    if(len(ids) == 0):
        await message.answer(text='Подписку оформляем!', reply_markup=kb)
        return
    await message.answer(
        text='Отправьте название аргумента, старт ОО, конец ОО, масштаб(пикселей на 1 ед.) и масштаб 1 ед.',
        reply_markup=types.ReplyKeyboardRemove())
    # for i in requested:
    # if i.name == 'fullanalysis':
    # Requested.choosearg = True
    # i.active = True

    cursor.execute("""SELECT id FROM ActiveCalc""")
    ids = cursor.fetchall()
    flag: bool = False
    for idus in ids:
        if (message.chat.id == idus[0]):
            flag = True

            break
    if (not flag):
        cursor.execute("""INSERT INTO ActiveCalc VALUES (?, TRUE, "", "fullanalysis")""", (message.chat.id,))
        connection.commit()


@dp.message_handler()
async def selection_of_commands(message: types.Message):
    if message.text[:14] == "ADMIN_32040912":
        userid:int = int(message.text[15:])
        try:
            cursor.execute("""UPDATE Players SET subscr = 1 WHERE id = ?""", (userid,))
            await bot.send_message(chat_id=message.from_user.id,
                               text='Подписка выдана пользователю ' + str(userid), reply_markup=kb)
        except:
             await bot.send_message(chat_id=message.from_user.id,
                               text='Ошибка выдачи подписки', reply_markup=kb)
        return
    if message.text == 'ЕГЭ':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Выберите номер из ЕГЭ по математике:', reply_markup=ikb)
        return
    if message.text == 'Формулы-Теоремы':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Выберите фигуру:',
                               reply_markup=teorems_kb)
        return
    if message.text == 'Решить задачу':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Выберите задачу:', reply_markup=solve_task_list)
        return
    if message.text == 'Калькулятор':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Что вы хотите вычислить?', reply_markup=calculatorkb)
        await message.delete()
        return
    if message.text == 'Информация':
        await bot.send_message(chat_id=message.from_user.id,
                               text="Что вы хотите узнать?", reply_markup=infokb)
        return
    if message.text == 'Тригонометрия':
        keyboard = types.ReplyKeyboardMarkup()
        button_1 = types.KeyboardButton(text="Формулы приведения")
        keyboard.add(button_1)
        button_2 = "Синус угла по градусу"
        keyboard.add(button_2)
        button_3 = "Косинус угла по градусу"
        keyboard.add(button_3)
        button_4 = "Тангенс угла по градусу"
        keyboard.add(button_4)
        button_5 = "Перевод из радиан в градусы"
        keyboard.add(button_5)
        button_6 = "Перевод из градусов в радианы"
        keyboard.add(button_6)
        await bot.send_message(chat_id=message.from_user.id,
                               text='Выберете задачу:', reply_markup=keyboard)
        return
    if message.text == 'Синус угла по градусу':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Таблинчные углы: \n'
                                    '30°: 1/2\n'
                                    '45°: √2/2\n'
                                    '60°: √3/2\n'
                                    'Отправьте градус угла: ', reply_markup=back_kb)
        await TrigonometryState.degree_into_sin.set()
        return
    if message.text == 'Тангенс угла по градусу':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Таблинчные углы: \n'
                                    '30°: √3/3\n'
                                    '45°: 1\n'
                                    '60°: √3\n'
                                    'Отправьте градус угла: ', reply_markup=back_kb)
        await TrigonometryState.degree_into_tg.set()
        return
    if message.text == 'Косинус угла по градусу':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Таблинчные углы: \n'
                                    '30°: √3/2\n'
                                    '45°: 1\n'
                                    '60°: 1/2\n'
                                    'Отправьте градус угла: ', reply_markup=back_kb)
        await TrigonometryState.degree_into_cos.set()
    if message.text == 'Перевод из радиан в градусы':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Стандартные значения: \n'
                                    '0: 0\n'
                                    '1.57: 90\n'
                                    '3.14: 180\n'
                                    'Отправьте число радиан: ', reply_markup=back_kb)
        await TrigonometryState.radian_into_degree.set()
        return
    if message.text == 'Перевод из градусов в радианы':
        await bot.send_message(chat_id=message.from_user.id,
                               text='Стандартные значения: \n'
                                    '0: 0\n'
                                    '1.57: 90\n'
                                    '3.14: 180\n'
                                    'Отправьте число градусов: ', reply_markup=back_kb)
        await TrigonometryState.degree_into_radian.set()
        return
    if message.text == "Формулы приведения":
        await bot.send_message(chat_id=message.from_user.id,
                               text="Формулы приведения\n"
                                    "Правило состоит из трех последовательных шагов (например sin(p/2+a)):\n"
                                    "1. Определим в какой координатной четверти будет лежать угол. Знак функции в координатной четверти будет означать положительный или отрицательный угол. Например: sin(p/2+a) лежит во 2 четверти, где синус положителен.\n"
                                    "2. Если к искомому углу мы прибавляем p/2 или 3p/2, то функция будет меняться, если прибуаляем p или 3p, то функци я остается прежней. Например: sin(p/2+a), прибавляем p/2, значит функция меняется с sin на cos.\n"
                                    "3. В результате получаем sin(p/2+a)=cos(a). \n"
                                    "Таблица формул приведения: \n"
                                    "https://optim.tildacdn.com/tild3231-6135-4637-b563-326162393235/-/format/webp/1.jpg",
                               reply_markup=back_kb)
        await TrigonometryState.reduction_formulas.set()
        return
    if message.text == 'Таблица лидеров':
        cursor.execute("""SELECT * FROM Players ORDER BY score DESC""")
        leaders:list = cursor.fetchall()
        print(leaders)
        await bot.send_message(chat_id=message.from_user.id,
                               text='Таблица Лидеров:')
        ans:str = ''
        count:int = 1
        for i in leaders[:5]:
            user = await bot.get_chat(i[0])
            st:str = user.first_name + " " + user.last_name
            ans+=f"{count}. {st} : {i[1]} очков\n"
            count+=1
        await bot.send_message(chat_id=message.from_user.id,
                               text=ans)

        return
    if message.text == "Профиль пользователя":
        cursor.execute("""SELECT * FROM Players WHERE id = ?""", (message.chat.id,))
        ids = cursor.fetchall()
        if(len(ids) == 0):
            await bot.send_message(chat_id=message.from_user.id, text="Вы пока еще не зарегестрированы(")
        else:
            user = await bot.get_chat(message.from_user.id)
            st:str = user.first_name + " " + user.last_name
            tempor:int = random.randint(1, 3)
            ans:str = ""
            if(tempor == 1): ans += "Вот и вы, "
            elif(tempor == 2): ans += "Ваше дело, "
            else: ans += "Это снова вы, "
            ans += (st + ",\n")
            ans += "Количество очков: " + str(ids[0][1]) + '\n'
            ans += "Провели в играх: "  + str(ids[0][2]) + " секунд" + '\n'
            ans += "Всего игр: "  + str(ids[0][3]) + '\n'
            ans += "Кол-во выигрышей: "  + str(ids[0][4]) + '\n'
            ans += "Кол-во проигрешей: "  + str(ids[0][5]) + '\n'
            cursor.execute("""SELECT * FROM Players ORDER BY score DESC""")
            leaders:list = cursor.fetchall()
            k:int = 0
            for i in range(len(leaders)):
                if(leaders[i][0] == message.chat.id):
                    k = i + 1
                    break
            ans += "Место в таблице лидеров: " + str(k)
            await bot.send_message(chat_id=message.from_user.id, text=ans)

        return
    if message.text == 'Игра “кто быстрей решит задачу”':
        await message.delete()
        cursor.execute("""SELECT id FROM ActiveFinders""")
        ids = cursor.fetchall()
        flag: bool = False
        for idus in ids:
            if (message.chat.id == idus[0]):
                flag = True

                break
        cursor.execute("""SELECT id_player1 FROM ActivePlayers""")
        ids = cursor.fetchall()
        for idus in ids:
            if (message.chat.id == idus[0]):
                flag = True

                break
        cursor.execute("""SELECT id_player2 FROM ActivePlayers""")
        ids = cursor.fetchall()
        for idus in ids:
            if (message.chat.id == idus[0]):
                flag = True

                break
        if (not flag):
            cursor.execute("""INSERT INTO ActiveFinders VALUES (?)""", (message.chat.id,))
            connection.commit()
            cursor.execute("""SELECT id FROM Players""")
            idspl:list = cursor.fetchall()
            fl:bool = True
            for i in idspl:
                if(i[0]==message.chat.id):
                    fl = False
                    break
            print(fl)
            if(fl):
                cursor.execute("""INSERT INTO Players VALUES (?, 0, 0, 0, 0, 0, 0)""", (message.chat.id,))
                connection.commit()
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Поиск противника...')
        else:
            return
        cursor.execute("""SELECT * FROM ActiveFinders""")
        usrs = cursor.fetchall()

        if (len(usrs) == 2):
            print(message.from_user.id, usrs)
            cursor.execute("""DELETE FROM ActiveFinders""")
            connection.commit()
            now = datetime.now()
            delta = now - datetime(2022, 1, 1)
            seconds = delta.total_seconds()
            taski: list = generate_task()

            connection.commit()
            if (message.from_user.id == usrs[0][0]):
                user1 = message.from_user.id
                user2 = usrs[1][0]
                cursor.execute("""INSERT INTO ActivePlayers VALUES (?, ?, ?, ?, ?)""",
                               (message.chat.id, usrs[1][0], int(seconds), taski[0], taski[2],))
            elif (message.from_user.id == usrs[1][0]):
                user1 = message.from_user.id
                user2 = usrs[0][0]
                cursor.execute("""INSERT INTO ActivePlayers VALUES (?, ?, ?, ?, ?)""",
                               (message.chat.id, usrs[0][0], int(seconds), taski[0], taski[2],))
            connection.commit()
            await bot.send_message(chat_id=user1,
                                   text='Противник найден: ' + str(user2))
            await bot.send_message(chat_id=user2,
                                   text='Противник найден: ' + str(user1))

            await bot.send_message(chat_id=user1,
                                   text=taski[1]['text'])
            await bot.send_message(chat_id=user1,
                                   text=taski[1]['images'])
            await bot.send_message(chat_id=user2,
                                   text=taski[1]['text'])
            await bot.send_message(chat_id=user2,
                                   text=taski[1]['images'])

        return

    tmps1: bool = False
    # for i in requested:
    # if (i.active):
    # tmps1 = True
    # break
    cursor.execute("""SELECT * FROM ActiveCalc WHERE id = ?""", (message.chat.id,))
    thisuser = cursor.fetchall()
    print(thisuser)
    if (thisuser != []):
        tmps1 = True
    if (tmps1):
        chsarg: bool = thisuser[0][1]
        args: str = thisuser[0][2]
        req: str = thisuser[0][3]
        # return

        if (chsarg):
            # Requested.choosearg = False
            cursor.execute("""UPDATE ActiveCalc SET chsarg = FALSE WHERE id = ?""", (message.chat.id,))
            connection.commit()
            cursor.execute("""UPDATE ActiveCalc SET args = ? WHERE id = ?""", (message.text, message.chat.id,))
            connection.commit()
            # Requested.listarg = list(message.text.split(', '))
            if (req == 'derivative'):
                await message.answer(text='Напишите функцию.')
            elif (req == 'integral'):
                await message.answer(text='Напишите подынтегральную функцию.')
            elif (req == 'lim'):
                await message.answer(text='Напишите функцию.')
            elif (req == 'taylorseq'):
                await message.answer(text='Напишите функцию.')
            elif (req == 'asymptotes'):
                await message.answer(text='Напишите функцию.')
            elif (req == 'diffequation'):
                await message.answer(text='Напишите уравнение в виде F(...) = 0.')
            elif (req == 'fullanalysis'):
                await message.answer(text='Напишите функцию в явном виде.')

            return

    chsarg: bool = False
    args: str = ""
    req: str = ""
    try:
        chsarg = thisuser[0][1]
        args = thisuser[0][2]
        req = thisuser[0][3]
    except:
        pass
    for i in requested:
        if (i.name == req):

            var = i.calculate(message.text, args.split(", "))

            if (str(type(var)) == '<class \'str\'>'):
                await message.answer(text=var, reply_markup=kb)
            elif (str(type(var)) == '<class \'list\'>'):
                await bot.send_photo(message.chat.id, var[0], caption=var[1])
                answer: str = "Функция: " + str(var[2]) + '\n'
                answer += "1 Производная: " + str(var[3]) + '\n'
                answer += "Нули функции: " + str(var[4]) + '\n'
                answer += "Значение функции в нуле: " + str(var[5]) + '\n'
                answer += "Нули производной: " + str(var[6]) + '\n'
                answer += "Промежутки роста: " + str(var[7]) + '\n'
                answer += "Промежутки падения: " + str(var[8])
                await message.answer(text=answer, reply_markup=kb)

            # i.active = False
            # Requested.listarg = list()
            cursor.execute("""DELETE FROM ActiveCalc WHERE id = ?""", (message.chat.id,))
            connection.commit()
            return
    cursor.execute("""SELECT * FROM ActivePlayers WHERE id_player1 = ? OR id_player2 = ?""",
                   (message.chat.id, message.chat.id,))
    thisuser = cursor.fetchall()
    if len(thisuser) == 0:
        await message.answer(text="Простите, я вас не понимаю")
        return
    scr:int = thisuser[0][4]
    if (thisuser != []):
        if (message.text == thisuser[0][3]):
            now = datetime.now()
            delta = now - datetime(2022, 1, 1)
            seconds = delta.total_seconds()
            idlose:int = 0
            idwin:int = 0
            await message.answer(text=f"Правильно! Молодец! Время решения: {int(seconds - thisuser[0][2])} sec")
            if (message.chat.id == thisuser[0][0]):
                idlose = int(thisuser[0][1])
                idwin = int(thisuser[0][0])
                try:
                    await bot.send_message(int(thisuser[0][1]), "Обогнали тебя(")
                except:
                    pass
            else:
                idlose = int(thisuser[0][0])
                idwin = int(thisuser[0][1])
                try:
                    await bot.send_message(int(thisuser[0][0]), "Обогнали тебя(")
                except:
                    pass
            print(message.chat.id)
            cursor.execute("""DELETE FROM ActivePlayers WHERE id_player1 = ? OR id_player2 = ?""",
                           (int(message.chat.id), int(message.chat.id),))
            connection.commit()
            cursor.execute("""UPDATE Players SET overtaked = overtaked + 1 WHERE id = ?""", (idlose,))
            cursor.execute("""UPDATE Players SET correct = correct + 1 WHERE id = ?""", (idwin,))
            cursor.execute("""UPDATE Players SET sum_answer_time = sum_answer_time + ? WHERE id = ?""", (int(seconds - thisuser[0][2]),idwin,))
            cursor.execute("""UPDATE Players SET sum_answer_time = sum_answer_time + ? WHERE id = ?""", (int(seconds - thisuser[0][2]),idlose,))
            cursor.execute("""UPDATE Players SET score = score + ? WHERE id = ?""", (scr,idwin,))
            cursor.execute("""UPDATE Players SET score = score - ? WHERE id = ?""", (scr,idlose,))
            cursor.execute("""UPDATE Players SET count_answers = count_answers + 1 WHERE id = ?""", (idlose,))
            cursor.execute("""UPDATE Players SET count_answers = count_answers + 1 WHERE id = ?""", (idwin,))
            connection.commit()
        else:
            await message.answer(text="Неправильно! Давай решай нормально!")
        return
    await message.answer(text="Простите, я вас не понимаю")


@dp.message_handler(state=CurrentState.square_a)
async def calculate_square_square_a(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['square_a'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {int(data['square_a']) ** 2}", reply_markup=back_kb,
                                   parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.square_d)
async def calculate_square_square_d(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['square_d'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {float(int(data['square_d']) ** 2 / 2)}", reply_markup=back_kb,
                                   parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.rect_a)
async def calculate_rect_square_a(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['rect_a'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте длину второй стороны:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.rect_b)
async def calculate_rect_square_b(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['rect_b'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {int(data['rect_a']) * int(data['rect_b'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.triang_a)
async def calculate_triang_square_a(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['triang_a'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'Отправьте высоту:', reply_markup=back_kb)
            await CurrentState.next()


@dp.message_handler(state=CurrentState.triang_h)
async def calculate_triang_square_h(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['triang_h'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {int(data['triang_a']) * int(data['triang_h']) / 2}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.pyra_apof_a)
async def calculate_pyra_apof_a(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['pyra_apof_a'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text="Отправьте периметр основания:", reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.pyra_n1)
async def calculate_pyra_n1(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['pyra_n1'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте количество сторон основания пирамиды:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.pyra_apof_s)
async def calculate_pyra_apof_s(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['pyra_apof_s'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте длину бокового ребра пирамиды:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.pyra_n2)
async def calculate_pyra_n2(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['pyra_n2'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте синус плоского угла при вершине пирамиды:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.pyra_n)
async def calculate_pyra_n(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['pyra_n'] = message.text
            data['pyra_n3'] = (float(data['pyra_apof_a']) * float(data['pyra_n1']) + int(data['pyra_apof_s']) * float(
                data['pyra_n2']) * float(data['pyra_n'])) / 2
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['pyra_n3'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
            # print(data['pyra_osn_square'], data['pyra_bok_square'])
        await state.finish()


@dp.message_handler(state=CurrentState.trape_a)
async def calculate_trape_a(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['trape_a'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте длину стороны меньшего основания трапеции:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.trape_b)
async def calculate_trape_b(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['trape_b'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте длину высоты трапеции:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.trape_c)
async def calculate_trape_c(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['trape_c'] = message.text
            data['trape_d'] = (int(data['trape_a']) + int(data['trape_b'])) / 2 * int(data['trape_c'])
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['trape_d'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.trape_f)
async def calculate_trape_f(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['trape_f'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте длину высоты трапеции:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.trape_g)
async def calculate_trape_g(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['trape_g'] = message.text
            data['trape_d'] = int(data['trape_f']) * int(data['trape_g'])
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['trape_d'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.rhomb_q)
async def calculate_rhomb_q(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['rhomb_q'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте длину второй диагонали ромба:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.rhomb_w)
async def calculate_rhomb_w(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['rhomb_w'] = message.text
            data['rhomb_e'] = (int(data['rhomb_q']) * (int(data['rhomb_w']))) / 2
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['rhomb_e'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.rhomb_a)
async def calculate_rhomb_a(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['rhomb_a'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте синус угла ромба (десятичная дробь):', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.rhomb_s)
async def calculate_rhomb_s(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['rhomb_s'] = message.text
            data['rhomb_d'] = (int(data['rhomb_a']) ** 2 * (float(data['rhomb_s'])))
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['rhomb_d'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.rhomb_z)
async def calculate_rhomb_z(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['rhomb_z'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте высоту, опущенную к стороне ромба:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.rhomb_x)
async def calculate_rhomb_x(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['rhomb_x'] = message.text
            data['rhomb_c'] = (int(data['rhomb_z']) * int((data['rhomb_x'])))
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['rhomb_c'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.right_triang_q)
async def calculate_right_triang_q(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['right_triang_q'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте второй катет:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.right_triang_w)
async def calculate_right_triang_w(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['right_triang_w'] = message.text
            data['right_triang_e'] = (int(data['right_triang_q']) * int(data['right_triang_w']) / 2)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['right_triang_e'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.right_triang_a)
async def calculate_right_triang_a(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['right_triang_a'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте высоту, проведенную от прямого угла:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.right_triang_s)
async def calculate_right_triang_s(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['right_triang_s'] = message.text
            data['right_triang_d'] = (int(data['right_triang_a']) * int(data['right_triang_s']) / 2)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['right_triang_d'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.right_triang_z)
async def calculate_right_triang_z(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['right_triang_z'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте синус угла прямоугольного треугольника:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.right_triang_x)
async def calculate_right_triang_x(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['right_triang_x'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text='Отправьте приележащий к углу катет:', reply_markup=back_kb)
        await CurrentState.next()


@dp.message_handler(state=CurrentState.right_triang_c)
async def calculate_right_triang_c(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['right_triang_c'] = message.text
            data['right_triang_v'] = (
                        int(data['right_triang_z']) * float(data['right_triang_x']) * int(data['right_triang_c']) / 2)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {((data['right_triang_v']))}",
                                   reply_markup=back_kb, parse_mode="HTML")
        await state.finish()


@dp.message_handler(state=CurrentState.circle_square_a)
async def calculate_circle_square_a(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['circle_square_a'] = message.text
            data['circle_square_s'] = (int(data['circle_square_a']) ** 2 * 3.14)
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f"<b>Ответ:</b> {(data['circle_square_s'])}",
                                   reply_markup=back_kb, parse_mode="HTML")
            print(data['pyra_osn_square'], data['pyra_bok_square'])
        await state.finish()


@dp.message_handler(state=TrigonometryState.degree_into_sin)
async def trigonometry_degree_into_sin(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['degree_into_sin'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Ответ: </b>{sin(rad(int(data["degree_into_sin"])))}\n'
                                        f'<b>Альтернативный ответ: '
                                        f'</b>{round(math.sin(radians(int(data["degree_into_sin"]))), 3)}',
                                   reply_markup=back_kb, parse_mode='HTML')
            await state.finish()


@dp.message_handler(state=TrigonometryState.degree_into_tg)
async def trigonometry_degree_into_tg(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['degree_into_tg'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Ответ: </b>{tan(rad(int(data["degree_into_tg"])))}\n'
                                        f'<b>Альтернативный ответ: '
                                        f'</b>{round(math.tan(math.radians(int(data["degree_into_tg"]))), 3)}',
                                   reply_markup=back_kb, parse_mode='HTML')
            await state.finish()


@dp.message_handler(state=TrigonometryState.degree_into_cos)
async def trigonometry_degree_into_cos(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['degree_into_cos'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Ответ: </b>{cos(rad(int(data["degree_into_cos"])))}\n'
                                        f'<b>Альтернативный ответ: '
                                        f'</b>{round(math.cos(radians(int(data["degree_into_cos"]))), 3)}',
                                   reply_markup=back_kb, parse_mode='HTML')
            await state.finish()



@dp.message_handler(state=TrigonometryState.radian_into_degree)
async def trigonometry_radian_into_degree(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['radian_into_degree'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Ответ: </b>{math.degrees(int(data["radian_into_degree"]))}\n',
                                   reply_markup = back_kb, parse_mode = 'HTML')
            await state.finish()


@dp.message_handler(state=TrigonometryState.degree_into_radian)
async def trigonometry_degree_into_radian(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['degree_into_radian'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Ответ: </b>{math.radians(int(data["degree_into_radian"]))}\n',
                                   reply_markup = back_kb, parse_mode = 'HTML')
            await state.finish()


@dp.message_handler(state=TrigonometryState.reduction_formulas)
async def trigonometry_reduction_formulas(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['reduction_formulas'] = message.text
            await bot.send_message(chat_id=message.from_user.id,
                                   text=f'<b>Ответ: </b>{int(data["reduction_formulas"])}\n',
                                   reply_markup = back_kb, parse_mode = 'HTML')
            await state.finish()


@dp.message_handler(state=EgeState.ege_1_ans)
async def check_ege_1_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_1_ans'] = message.text
            if data['user_ege_1_ans'] == Ege.ege_1_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_1_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_1_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_2_ans)
async def check_ege_2_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_2_ans'] = message.text
            if data['user_ege_2_ans'] == Ege.ege_2_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_2_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_2_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_3_ans)
async def check_ege_3_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_3_ans'] = message.text
            if data['user_ege_3_ans'] == Ege.ege_3_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_3_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_3_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_4_ans)
async def check_ege_4_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_4_ans'] = message.text
            if data['user_ege_4_ans'] == Ege.ege_4_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_4_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно', reply_markup=ege_4_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_5_ans)
async def check_ege_5_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_5_ans'] = message.text
            if data['user_ege_5_ans'] == Ege.ege_5_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_5_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_5_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_6_ans)
async def check_ege_6_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_6_ans'] = message.text
            if data['user_ege_6_ans'] == Ege.ege_6_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно', reply_markup=ege_6_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно', reply_markup=ege_6_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_7_ans)
async def check_ege_7_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_7_ans'] = message.text
            if data['user_ege_7_ans'] == Ege.ege_7_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_7_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_7_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_8_ans)
async def check_ege_8_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_8_ans'] = message.text
            if data['user_ege_8_ans'] == Ege.ege_8_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_8_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_8_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_9_ans)
async def check_ege_9_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_9_ans'] = message.text
            if data['user_ege_9_ans'] == Ege.ege_9_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_9_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_9_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_10_ans)
async def check_ege_10_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_10_ans'] = message.text
            if data['user_ege_10_ans'] == Ege.ege_10_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_10_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_10_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_11_ans)
async def check_ege_11_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_11_ans'] = message.text
            if data['user_ege_11_ans'] == Ege.ege_11_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_11_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_11_wrong_ans_kb)
            await state.finish()


@dp.message_handler(state=EgeState.ege_12_ans)
async def check_ege_12_ans(message: types.Message, state: FSMContext):
    if message.text == 'Назад':
        await state.finish()
        await cmd_back(message)
    else:
        async with state.proxy() as data:
            data['user_ege_12_ans'] = message.text
            if data['user_ege_12_ans'] == Ege.ege_12_ans:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили верно.', reply_markup=ege_12_right_ans_kb)
            else:
                await bot.send_message(chat_id=message.from_user.id,
                                       text='Вы ответили неверно.', reply_markup=ege_12_wrong_ans_kb)
            await state.finish()


@dp.callback_query_handler()
async def callback_query_handler(callback_query: types.CallbackQuery):
    if callback_query.data == 'back':
        await cmd_back(callback_query)
    if callback_query.data == 'f_back':
        await callback_query.message.delete()
        await callback_query.message.answer(text='Выберите фигуру:', reply_markup=teorems_kb)
    if callback_query.data == 'cmd-list':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Список команд:\n\n'
                                    '/start - запуск/перезапуск бота\n'
                                    '/derivative - вычислить производную\n'
                                    '/integral - вычислить интеграл\n'
                                    '/taylorseq - разложение в ряд Тейлора\n'
                                    '/lim - вычислить предел функции\n'
                                    '/diffequation - решить приведённое дифференциальное уравнение\n'
                                    '/asymptotes - вычислить асимптоты функции\n'
                                    '/lengthcurve - вычислить длину кривой\n'
                                    '/fullanalysis - полный анализ\n'
                                    '/factorial - вычислить факториал\n'
                                    '/logarithm - вычислить логарифм\n'
                                    '/lcm - вычислить наименьшее общее кратное\n'
                                    '/hcf - вычислить наибольший общий делитель\n'
                                    '/elevation - возведение в степень\n'
                                    '/sqrt - вычисление корня')
    if callback_query.data == 'tech-support':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Если у вас есть вопросы или предложения, как можно улучшить бота свяжитесь по номеру телефона +71234567891')
    if callback_query.data == 'problem8':
        await callback_query.message.delete()
        task = get_task(8)
        Ege.ege_8_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_8_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_8_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup = back_kb)
            await EgeState.ege_8_ans.set()
    if callback_query.data == 'problem1':
        await callback_query.message.delete()
        task = get_task(1)
        Ege.ege_1_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_1_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_1_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_1_ans.set()
    if callback_query.data == 'problem1-solution':
        await callback_query.message.delete()
        task = Ege.ege_1_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem2':
        await callback_query.message.delete()
        task = get_task(2)
        Ege.ege_2_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_2_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_2_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_2_ans.set()
    if callback_query.data == 'problem2-solution':
        await callback_query.message.delete()
        task = Ege.ege_2_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem3':
        await callback_query.message.delete()
        task = get_task(3)
        Ege.ege_3_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_3_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_3_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_3_ans.set()
    if callback_query.data == 'problem3-solution':
        await callback_query.message.delete()
        task = Ege.ege_3_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem4':
        await callback_query.message.delete()
        task = get_task(4)
        Ege.ege_4_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_4_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_4_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_4_ans.set()
    if callback_query.data == 'problem4-solution':
        await callback_query.message.delete()
        task = Ege.ege_4_task
        task_solution_text = task.get('solution').get('text')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem5':
        await callback_query.message.delete()
        task = get_task(5)
        Ege.ege_5_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_5_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_5_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_5_ans.set()
    if callback_query.data == 'problem5-solution':
        await callback_query.message.delete()
        task = Ege.ege_5_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem6':
        await callback_query.message.delete()
        task = get_task(6)
        Ege.ege_6_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_6_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_6_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_6_ans.set()
    if callback_query.data == 'problem6-solution':
        await callback_query.message.delete()
        task = Ege.ege_6_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem7':
        await callback_query.message.delete()
        task = get_task(7)
        Ege.ege_7_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_7_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_7_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_7_ans.set()
    if callback_query.data == 'problem7-solution':
        await callback_query.message.delete()
        task = Ege.ege_7_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem8-solution':
        await callback_query.message.delete()
        task = Ege.ege_8_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem9':
        await callback_query.message.delete()
        task = get_task(9)
        Ege.ege_9_task = task
        task_condition_text = task.get('condition').get('text')  # .replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_9_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_9_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_9_ans.set()
    if callback_query.data == 'problem9-solution':
        await callback_query.message.delete()
        task = Ege.ege_9_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem10':
        await callback_query.message.delete()
        task = get_task(10)
        Ege.ege_10_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_10_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_10_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_10_ans.set()
    if callback_query.data == 'problem10-solution':
        await callback_query.message.delete()
        task = Ege.ege_10_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem11':
        await callback_query.message.delete()
        task = get_task(11)
        Ege.ege_11_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_11_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_11_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_11_ans.set()
    if callback_query.data == 'problem11-solution':
        await callback_query.message.delete()
        task = Ege.ege_11_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem12':
        await callback_query.message.delete()
        task = get_task(12)
        Ege.ege_12_task = task
        task_condition_text = task.get('condition').get('text')  # .replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        Ege.ege_12_ans = task.get('answer')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_12_ans.set()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=back_kb, parse_mode='HTML')
            await message_url(task, callback_query)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Ваш ответ:", reply_markup=back_kb)
            await EgeState.ege_12_ans.set()
    if callback_query.data == 'problem12-solution':
        await callback_query.message.delete()
        task = Ege.ege_12_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'bot-advantages':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Наш бот имеет множество уникальных функций, кототрые позволяют пользователю с удобством решать различные математические задачи. Среди них можно выделить самые значительные:\n\n'
                                    '• Большой сборник заданий ЕГЭ с решениями и ответами \n\n'
                                    '• Множество геометрических формул \n\n'
                                    '• Тренировочные задания для оттачивания базовой геометрии \n\n'
                                    '• Калькулятор с функциями всех сложностей: от сложения до производной \n\n'
                                    '• Предоставление списка частых тригонометрических функций и вычисление для конкретных значений \n\n'
                                    '• Уникальная онлайн-игра "Кто быстрее решит задачу \n\n'
                                    '• Постоянное поддержание проекта, включая оказывание техподдержки \n\n')
    if callback_query.data == 'authors':
        await bot.send_message(chat_id=callback_query.from_user.id,
        text = 'Наши работники сделали: \n\n'
               'Валерий Аникин: руководитель проекта\n\n'
               'Михаил рубцов: сайт, задания ЕГЭ\n\n'
               'Александр Козленко: сайт\n\n'
               'Алексей Коновалов: сайт, перевод из радиан в градусы, этот список\n\n'
               'Ярамир Попель: сайт\n\n'
               'Вячеслав Смирнов: площади фигур, логарифмы, синусы, задания ЕГЭ, списоккоманд\n\n'
               'Артём Шабайков: площади фигур, извлечение корня, косинусы, задания ЕГЭ,\n\n'
               'Варвара Афонина: задания ЕГЭ, возведение в степень, тангенсы, задания ЕГЭ,\n\n'
               'Варвара Дорохина: задания ЕГЭ, нахождение НОК, формулы приведения, задания ЕГЭ,\n\n'
               'Дмитрий Москвичёв: нахождение НОД, задания ЕГЭ\n\n'
               'Дмитрий Филимонов: задачи, проценты, задания ЕГЭ, \n\n'
               'Егор Данович: формулы, факториалы, задания ЕГЭ,\n\n'
               'Илья Воронцов: тригонометрические функции\n\n'
               'Михаил Максимов: формулы, длина кривой, Задания ЕГЭ\n\n'
               'Михаил Помпушко: калькулятор, частная производная, дифференциальные уравнения, полный анализ, игра')
    if callback_query.data == 'square-square':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула площади:*\n _S = a^2, где a-сторона_\n'
                                    '_S = 1/2 * d^2, где d-диагональ_\n'
                                    'Выберите известную величину: ', reply_markup=square_area_kb)
    if callback_query.data == 'square-square-a':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте длину стороны квадрата.', reply_markup=back_kb)
        await CurrentState.square_a.set()
    if callback_query.data == 'square-square-d':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте длину диагонали квадрата.', reply_markup=back_kb)
        await CurrentState.square_d.set()
    if callback_query.data == 'rect-square':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула площади:*\n_S = a * b, где a,b - стороны_\n'
                                    'Отправьте длину первой стороны:', reply_markup=back_kb)
        await CurrentState.rect_a.set()
    if callback_query.data == 'triang-square':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула площади:*\nS = 1/2 * a * h,'
                                    ' где a - сторона, h - высота\n'
                                    'Отправьте длину стороны:', reply_markup=back_kb)
        await CurrentState.triang_a.set()
    if callback_query.data == 'pyra-square':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула площади:*\nS = S(бок) + S(осн),'
                                    ' где S(бок) - площадь боковой поверхности,'
                                    ' S(осн) - площадь основания\n'
                                    'S(бок) = 1/2 * P(осн) * SH, где '
                                    'P(осн) - периметр основания, '
                                    'SH - апофема', reply_markup=pyra_square_kb)
    if callback_query.data == 'pyra-square-a':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте длину апофемы пирамиды:', reply_markup=back_kb)
        await CurrentState.pyra_apof_a.set()
    if callback_query.data == 'trape-square-b':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте кол-во углов пирамиды:', reply_markup=back_kb)
        await CurrentState.pyra_n.set()
    if callback_query.data == 'trape-square':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула площади:*\nS = (a+b)/2*h\n'
                                    'Где a и b - основания трапеции\n'
                                    'S = mh\n'
                                    'm = (a+b)/2\n'
                                    'где m - полуоснование трапеции', reply_markup=trape_square_kb)
    if callback_query.data == 'trape-square-a':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте длину стороны большего основания трапеции:', reply_markup=back_kb)
        await CurrentState.trape_a.set()
    if callback_query.data == 'trape-square-b':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте длину полуоснования трапеции:', reply_markup=back_kb)
        await CurrentState.trape_f.set()
    if callback_query.data == 'rhomb-square':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула площади:*\nS = (a*b)/2\n'
                                    'Где a и b - диагонали ромба\n'
                                    'S = a^2sinα\n'
                                    'где a - сторона ромба\n'
                                    'α - угл между сторонами ромба\n'
                                    'S = ah\n'
                                    'где а - сторона ромба\n'
                                    'h - высота, опущенная к этой стороне', reply_markup=rhomb_square_kb)
    if callback_query.data == 'rhomb-square-a':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте длину диагонали ромба:', reply_markup=back_kb)
        await CurrentState.rhomb_q.set()
    if callback_query.data == 'rhomb-square-b':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте длину стороны ромба:', reply_markup=back_kb)
        await CurrentState.rhomb_a.set()
    if callback_query.data == 'rhomb-square-c':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте длину стороны ромба:', reply_markup=back_kb)
        await CurrentState.rhomb_z.set()
    if callback_query.data == 'trape-height':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула высоты:*\nh = 2S/(a+b)\n'
                                    'Где a и b - основания трапеции\n'
                                    'S - площадь трапеции\n'
                                    'Отправьте площадь трапеции:', reply_markup=back_kb)
        await CurrentState.right_triang_a.set()
    if callback_query.data == 'circle-square':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула высоты:*\nS = π*r^2\n'
                                    'Где r - радиус окружности\n'
                                    'Отправьте радиус окружности:', reply_markup=back_kb)
        await CurrentState.circle_square_a.set()
    if callback_query.data == 'right-triang-square':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='*Формула площади:*\nS = (a*b)/2\n'
                                    'Где a и b - катеты прямоугольного треугольника\n'
                                    'S = bc*sina/2\n'
                                    'где a - угл прямоугольного треугольника\n'
                                    'b - прилежащий к углу а катет\n'
                                    'с - гипотенуза прямоугольного треугольника\n'
                                    'S = ah/2\n'
                                    'где а - гипотенуза прямоугольного треугольника\n'
                                    'h - высота, опущенная из прямого угла', reply_markup=right_triang_square_kb)
    if callback_query.data == 'right-triang-square-a':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте катет прямоугольного треугольника:', reply_markup=back_kb)
        await CurrentState.right_triang_q.set()
    if callback_query.data == 'right-triang-square-b':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте гипотенузу прямоугольного треугольника:', reply_markup=back_kb)
        await CurrentState.right_triang_a.set()
    if callback_query.data == 'right-triang-square-c':
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Отправьте гипотенузу прямоугольного треугольника:', reply_markup=back_kb)
        await CurrentState.right_triang_z.set()
    if callback_query.data == 'problem13':
        await callback_query.message.delete()
        task = get_task(13)
        Ege.ege_13_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Это задание из второй части ЕГЭ с развёрнутым ответом.'
                                    ' Мы не можем автоматически проверить его, '
                                    'поэтому вы можете проверить сами себя')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
                else:
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Произошла ошибка при отправке фотографии.', reply_markup=back_kb)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_13_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_13_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
    if callback_query.data == 'problem13-solution':
        task = Ege.ege_13_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem14':
        await callback_query.message.delete()
        task = get_task(14)
        Ege.ege_14_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Это задание из второй части ЕГЭ с развёрнутым ответом.'
                                    ' Мы не можем автоматически проверить его, '
                                    'поэтому вы можете проверить сами себя')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
                else:
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Произошла ошибка при отправке фотографии.', reply_markup=back_kb)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_14_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_14_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
    if callback_query.data == 'problem14-solution':
        task = Ege.ege_14_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem15':
        await callback_query.message.delete()
        task = get_task(15)
        Ege.ege_15_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
                else:
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Произошла ошибка при отправке фотографии.', reply_markup=back_kb)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_15_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_15_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
    if callback_query.data == 'problem15-solution':
        task = Ege.ege_15_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem16':
        await callback_query.message.delete()
        task = get_task(16)
        Ege.ege_16_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Это задание из второй части ЕГЭ с развёрнутым ответом.'
                                    ' Мы не можем автоматически проверить его, '
                                    'поэтому вы можете проверить сами себя')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
                else:
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Произошла ошибка при отправке фотографии.', reply_markup=back_kb)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_16_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_16_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
    if callback_query.data == 'problem16-solution':
        task = Ege.ege_16_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem17':
        await callback_query.message.delete()
        task = get_task(17)
        Ege.ege_17_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Это задание из второй части ЕГЭ с развёрнутым ответом.'
                                    ' Мы не можем автоматически проверить его, '
                                    'поэтому вы можете проверить сами себя')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
                else:
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Произошла ошибка при отправке фотографии.', reply_markup=back_kb)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_17_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_17_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
    if callback_query.data == 'problem17-solution':
        task = Ege.ege_17_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem18':
        await callback_query.message.delete()
        task = get_task(18)
        Ege.ege_18_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Это задание из второй части ЕГЭ с развёрнутым ответом.'
                                    ' Мы не можем автоматически проверить его, '
                                    'поэтому вы можете проверить сами себя')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
                else:
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Произошла ошибка при отправке фотографии.', reply_markup=back_kb)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_18_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_18_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
    if callback_query.data == 'problem18-solution':
        task = Ege.ege_18_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'problem19':
        await callback_query.message.delete()
        task = get_task(19)
        Ege.ege_19_task = task
        task_condition_text = task.get('condition').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_condition_imgs = task.get('condition').get('images')
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text='Это задание из второй части ЕГЭ с развёрнутым ответом.'
                                    ' Мы не можем автоматически проверить его, '
                                    'поэтому вы можете проверить сами себя')
        try:
            if len(task_condition_imgs) != 0:
                response = requests.get(task_condition_imgs[0])
                if response.status_code == 200:
                    with open('condition.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='condition.svg', write_to='condition.png')
                    with open('condition.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id, photo=photo,
                                             reply_markup=back_kb)
                    os.remove('condition.svg')
                    os.remove('condition.png')
                else:
                    await bot.send_message(chat_id=callback_query.from_user.id,
                                           text='Произошла ошибка при отправке фотографии.', reply_markup=back_kb)
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_19_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_condition_text, reply_markup=ege_19_wrong_ans_kb, parse_mode='HTML')
            await message_url(task, callback_query)
    if callback_query.data == 'problem19-solution':
        task = Ege.ege_19_task
        task_solution_text = task.get('solution').get('text').replace('\u202f', ' ').replace('\xad', '')
        task_solution_imgs = task.get('solution').get('images')
        try:
            if len(task_solution_imgs) == 1:
                response = requests.get(task_solution_imgs)
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo='solution.png', reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            elif len(task_solution_imgs) != 0 and len(task_solution_imgs) != 1:
                response = requests.get(task_solution_imgs[0])
                if response.status_code == 200:
                    with open('solution.svg', 'wb') as f:
                        f.write(response.content)
                    cairosvg.svg2png(url='solution.svg', write_to='solution.png')
                    with open('solution.png', 'rb') as photo:
                        await bot.send_photo(chat_id=callback_query.from_user.id,
                                             photo=photo, reply_markup=back_kb)
                os.remove('solution.png')
                os.remove('solution.svg')
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
        except:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=task_solution_text, reply_markup=back_kb, parse_mode='HTML')
    if callback_query.data == 'f_Кв':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Квадрат</b>\n\nКвадрат - правильный четырёхугольник у которого все углы и всё стороны равны. Квадрат является частным случаем ромба и прямоугольника. \n\nS = a^2 \nР = 4а. \na - сторона квадрата\n\n<a href="https://ru.wikipedia.org/wiki/%D0%9A%D0%B2%D0%B0%D0%B4%D1%80%D0%B0%D1%82">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Куб':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Куб</b>\n\nКуб - правильный многогранник, каждая грань которого представляет собой квадрат. Частный случай параллелипипеда и призмы.\n\nS = 6а^2\nР = 12*а\nа - ребро.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%9A%D1%83%D0%B1">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Ромб':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Ромб</b>\n\nРомб - параллелограмм, у которого все стороны равны.\n\nS = 1/2*d1*d2\nS = ah\nP = 4a\nd1 и d2 - диагонали ромба\nh - высота ромба\na - сторона ромба.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%A0%D0%BE%D0%BC%D0%B1">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Пирам':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Пирамида</b>\n\nПирамида - многогранник у которого одна грань- произвольный многоугольник, называемое основанием, а остальные грани треугольники имеющие общую вершину..\n\nS = площади всех треугольников и основания\nS(треугольника) = (а*h)/2\nS основания вычисляется в зависимости от его формы, универсальной формулы нет.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%9F%D0%B8%D1%80%D0%B0%D0%BC%D0%B8%D0%B4%D0%B0">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Треугл':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Треугольник</b>\n\nТреугольник - геометрическая фигура, образованная тремя отрезками, которые соединяют три точки, не лежащие на одной прямой. Указанные три точки называются вершинами треугольника, а отрезки сторонами треугольника.\n\nS = 1/2a*h\nS = √(p*(p-a)*(p-b)*(p-c))\nS = 1/2a*b*sinc\nS = (a*b*c)/R\nS = p*r\na - сторона треугольника\nh - высота (в данном случае непосредственно падающая на сторону a)\np - полупериметр\nsinc - синус угла между сторонами a и b\nR - радиус описанной окружности\nr - радиус вписанной окружности\n\n<a href="https://ru.wikipedia.org/wiki/%D0%A2%D1%80%D0%B5%D1%83%D0%B3%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D0%BA">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Параллгр':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Параллелограмм</b>\n\nПараллелограмм - четырехугольник, у которого стороны попарно параллельны. Признаки параллелограмма: Если противоположные стороны четырехугольника попарно параллельны, то этот четырехугольник называется параллелограммом .\n\nS = a*h\nP = 2*(a+b)\nh - высота непосредственно падающая на сторону a.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%9F%D0%B0%D1%80%D0%B0%D0%BB%D0%BB%D0%B5%D0%BB%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Трапец':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Трапеция</b>\n\nТрапеция - выпуклый четырехугольник, у которого две стороны параллельны, а две другие нет. Две параллельные стороны трапеции называются её основаниями, а две другие- боковыми сторонами.\n\nS = (a+b)/2*h\nS = (a+b)/2*√(c^2-(((a-b)^2+c^2-d^2)/2*(a-b))^2)\nР = a+b+c+d\na - верхнее основание\nb - нижнее основание\nc и d - боковые стороны\nh - высота непосредственно подающая с верхнего основания на нижнее.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%A2%D1%80%D0%B0%D0%BF%D0%B5%D1%86%D0%B8%D1%8F">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Конус':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Конус</b>\n\nКонус - тело в евклидовом пространстве полученное объединением всех лучей исходящих, из одной точки и проходящих через плоскую поверхность.\n\nS = πr^2+πRl\nl- образующая конуса.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BD%D1%83%D1%81">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Окр':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Окружность</b>\n\nОкружность - множество точек плоскости, равноудаленных от заданной точки этой плоскости\n\nS = πr^2\nP = 2πr\nr - радиус круга\nπ - 3,1415926535897....\n\n<a href="https://ru.wikipedia.org/wiki/%D0%9A%D1%80%D1%83%D0%B3">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Сф':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Сфера</b>\n\nСфера - геометрическое место точек в пространстве, равно удаленные от некоторой заданной точки. Расстояние от центра сферы до её любой точки называется её радиусом. Сфера радиуса 1 называется единичной сферой.\n\nS = 4πR^2.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%A1%D1%84%D0%B5%D1%80%D0%B0">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Прям':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Прямоугольник</b>\n\nПрямоугольник - четырехугольник, у которого все углы прямые(90градусов).\n\nS= a*b\nP = 2(a+b)\na и b - стороны прямоугольника.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D1%8F%D0%BC%D0%BE%D1%83%D0%B3%D0%BE%D0%BB%D1%8C%D0%BD%D0%B8%D0%BA">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_Параллпд':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Параллелепипед</b>\n\nПараллелипипед - призма, основанием которой служит параллелограмм, или многогранник, у которого шесть граней и каждая является параллелограммом.\n\nS = 2(ab+bc+ac)\nР = 4(а+b+c)\na,b и с - рёбра параллелепипеда.\n\n<a href="https://ru.wikipedia.org/wiki/%D0%9F%D0%B0%D1%80%D0%B0%D0%BB%D0%BB%D0%B5%D0%BB%D0%B5%D0%BF%D0%B8%D0%BF%D0%B5%D0%B4">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_n-при':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>n-угольная призма</b>\n\nn-угольная призма – это геометрическое тело, составленный из двух равных многоугольников, лежащих в параллельных плоскостях и n параллелограммов, являющихся боковыми гранями призмы. Призма является многогранником – геометрическим телом, состоящим из граней. Боковые ребра призмы между собой равны и параллельны.\n\nS = p*h\nV = s*h\nS - площадь боковой поверхности призмы\np - периметр основания призмы\nh - высота призмы\nV - объем призмы\ns - площадь основания призмы\n\n<a href="https://ru.wikipedia.org/wiki/Призма_(геометрия)">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_n-угл':
        await callback_query.message.delete()
        await callback_query.message.answer(
            text='<b>Правильный n-угольник</b>\n\nПравильный n-угольник – это выпуклый многоугольник, в котором n сторон, n вершин и n углов (n≥3) и у которого равны все стороны и все углы между смежными сторонами.\n\nα = 180(n-2)\nP = na\nD = n(n-3)/2\nS = πa^2/4\na = 2r*tg(180°/n)\na = 2r*tg(π/n)\na = 2R*sin(180°/n)\na = 2R*sin(π/n)\nS = na^2*ctg(180°/n)/4\nS = nR^2*sin(360°/n)/2\nα1 = (n-2)*180°/n\nα - cумма углов n-угольника\nn - количество сторон n-угольника\nP - периметр n-угольника\na - длина стороны n-угольника\nD - количество диагоналей n-угольника\nS - площадь n-угольника\nr - радиус вписанного n-угольника\nR - радиус описанного n-угольника\nα1 - величина угла между сторонами правильного n-угольника\n\n<a href="https://ru.wikipedia.org/wiki/Правильный_многоугольник">Теоремы, свойства и формулы</a>',
            reply_markup=teorems_back_kb, parse_mode="HTML")
    if callback_query.data == 'f_back':
        await callback_query.message.delete()
        await callback_query.message.answer(text='Выберите фигуру:', reply_markup=teorems_kb)



# if __name__ != '__main__':
cursor.execute("""DROP TABLE IF EXISTS ActiveFinders""")
cursor.execute("""DROP TABLE IF EXISTS ActivePlayers""")
cursor.execute("""DROP TABLE IF EXISTS ActiveCalc""")
cursor.execute("""DROP TABLE IF EXISTS Players""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ActiveFinders (
    id INTEGER PRIMARY KEY
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ActivePlayers (
    id_player1 INTEGER,
    id_player2 INTEGER,
    start_time INTEGER,
    correct_ans TEXT,
    score INTEGER
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ActiveCalc (
    id INTEGER,
    chsarg BOOLEAN,
    args TEXT,
    requested TEXT
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Players (
    id INTEGER PRIMARY KEY,
    score INTEGER,
    sum_answer_time INTEGER,
    count_answers INTEGER,
    correct INTEGER,
    overtaked INTEGER,
    subscr INTEGER
    )
""")
executor.start_polling(dp, skip_updates=True)
