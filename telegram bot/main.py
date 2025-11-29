from aiogram import Bot, Dispatcher, types, executor  # pip install --force-reinstall -v "aiogram==2.25.2"
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from sympy import *
import math

# Документация по AIOGRAM
# https://docs.aiogram.dev/en/latest/contributing.html#guides

TOKEN_API = 'very-cool-token-should-be-here'  # !!! Необходимо сделать файл-конфиг и поместить туда эту переменную !!!
bot = Bot(TOKEN_API)
dp = Dispatcher(bot)
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton("/calculator"))

calculatorkb = ReplyKeyboardMarkup(resize_keyboard=True)
calculatorkb.add(KeyboardButton("/derivative"))
calculatorkb.add(KeyboardButton("/integral"))
calculatorkb.add(KeyboardButton("/partderivative"))
calculatorkb.add(KeyboardButton("/taylorseq"))
calculatorkb.add(KeyboardButton("/lim"))
calculatorkb.add(KeyboardButton("/diffequation"))
calculatorkb.add(KeyboardButton("/asymptotes"))
calculatorkb.add(KeyboardButton("/lengthcurve"))
calculatorkb.add(KeyboardButton("/fullanalysis"))
calculatorkb.add(KeyboardButton("/factorial"))
calculatorkb.add(KeyboardButton('/logarithm'))
calculatorkb.add(KeyboardButton('/lcm'))
calculatorkb.add(KeyboardButton('/elevation'))


class Requested:
    choosearg:bool = False
    listarg:list = list()
    def __init__(self, name:str):
        self.name = name
        self.active = False
    def calculate(self, func:str, args:list)->str:
        if(self.name == 'derivative'):
            x = symbols(args[1])
            funccpy:str = func
            try:
                for i in range(int(args[0])):
                    try:
                        derivative:str = simplify(diff(sympify(funccpy), x))
                    except:
                        return "Не удалось продифференцировать"
                    if(str(derivative)[0:10] == "Derivative"):
                        return "Не удалось продифференцировать"
                    funccpy = derivative
            except:
                return "Ошибка"
            answer:str = "Производная функции " + str(func) + f" по d{args[1]} равна " + str(derivative)
            return answer
        elif(self.name == 'integral'):
            x = symbols(args[0])
            try:
                integral:str = simplify(integrate(sympify(func), x))
            except:
                return "Не удалось проинтегрировать или не существует элементарной первообразной"
            if(str(integral)[0:8] == "Integral"):
                return "Не удалось проинтегрировать или не существует элементарной первообразной"
            answer:str = "Интеграл функции " + func + f" по d{args[0]} равен " + str(integral) + " + C"
            return answer
        elif(self.name == 'lim'):
            x = symbols(args[0])
            if(args[1] == "oo" or args[1] == "-oo"):
                limit_result = simplify(limit(sympify(func), x, args[1]))
            else:
                limit_result = simplify(limit(sympify(func), x, int(args[1])))
            return "Предел равен" + str(limit_result)
        elif(self.name == 'taylorseq'):

            x = symbols(args[0])
            try:
                initpt:int = int(args[2])
                count:int = int(args[1])
                exfunc = sympify(func)
                answ = exfunc.subs(x, initpt)

                for i in range(2, count+1):

                    answ += exfunc.diff(x, i - 1).subs(x, initpt) * ((x-initpt)**(i - 1)) / math.factorial(i - 1)
                #answ = simplify(answ)
                if(str(answ) == "nan"): return "Неопределено"
                return "Приближенная функция: " + str(answ)
            except:
                return "Ошибка"
        elif(self.name == "asymptotes"):
            x = symbols(args[0])
            asms:set = set()
            if(simplify(limit(sympify(func), x, +oo)) != +oo and simplify(limit(sympify(func), x, +oo) != -oo)):
                asms.add("y = " + str(simplify(limit(sympify(func), x, +oo))))
            if(simplify(limit(sympify(func), x, -oo)) != +oo and simplify(limit(sympify(func), x, -oo) != -oo)):
                asms.add("y = " + str(simplify(limit(sympify(func), x, -oo))))


            numerator, denominator = sympify(func).as_numer_denom()
            vertical_asymptotes = solve(denominator, x)
            for i in vertical_asymptotes:
                asms.add("x = " + str(i))
            if(degree(numerator) == degree(denominator) + 1):
                slope = limit(numerator / denominator, x, oo)
                asms.add(f"y = {slope}*x + b")
            ans:str = "Функция имеет асимптоты:"
            for i in asms:
                ans+=(" " + i + " ")
            return ans
        elif (self.name == "factorial"):
            x: int = int(func)
            ans: int = 1
            for i in range(1,x+1):
                ans *= i
            return f"Факториал {func} равен {ans}"
        elif self.name == 'logarithm':
            try:
                x: int = int(args[0])
                a: int = int(args[1])
                if a > 0 and a != 1 and x > 0:
                    ans = str(log(x, a))
                    return f"Логарифм числа {x} по основанию {a} это {ans}"
                return 'Ошибка'
            except:
                return 'Ошибка'
        elif (self.name == 'lcm'):
            x: int = int(args[0])
            y: int = int(args[1])
            greater = max(x, y)
            while True:
                if ((greater % x == 0) and (greater % y == 0)):
                    lcm = greater
                    break
                greater += 1
            return "НОК равно " + str(lcm)
        elif self.name == 'elevation':
            try:
                a: float = float(args[0])
                n: int = int(args[1])
                ans: float = float(pow(a, n))
                return f'Число {a} в степени {n} = {ans}'
            except:
                return 'Ошибка'




requested:list = list()


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


@dp.message_handler(commands=['start'])
async def start_func(message: types.Message):
    await message.answer(text='Команда старт!', reply_markup = kb)

@dp.message_handler(commands=['calculator'])
async def calc_func(message: types.Message):

    await message.answer(text='Калькулятор. Выберите опцию:', reply_markup = calculatorkb)


@dp.message_handler(commands=['derivative'])
async def derivative_func(message: types.Message):
    await message.answer(text='Напишите порядок и зависимую переменную.', reply_markup = types.ReplyKeyboardRemove())
    for i in requested:
        if(i.name == 'derivative'):
            Requested.choosearg = True
            i.active = True

@dp.message_handler(commands=['integral'])
async def integral_func(message: types.Message):
    await message.answer(text='Напишите зависимую переменную.', reply_markup = types.ReplyKeyboardRemove())
    for i in requested:
        if(i.name == 'integral'):
            Requested.choosearg = True
            i.active = True

@dp.message_handler(commands=['lim'])
async def integral_func(message: types.Message):
    await message.answer(text='Напишите зависимую переменную предельного перехода и ее предел.', reply_markup = types.ReplyKeyboardRemove())
    for i in requested:
        if(i.name == 'lim'):
            Requested.choosearg = True
            i.active = True

@dp.message_handler(commands=['taylorseq'])
async def integral_func(message: types.Message):
    await message.answer(text='Напишите зависимую перменную, число слагаемых и начальную точку.', reply_markup = types.ReplyKeyboardRemove())
    for i in requested:
        if(i.name == 'taylorseq'):
            Requested.choosearg = True
            i.active = True

@dp.message_handler(commands=['asymptotes'])
async def integral_func(message: types.Message):
    await message.answer(text='Напишите зависимую переменную.', reply_markup = types.ReplyKeyboardRemove())
    for i in requested:
        if(i.name == 'asymptotes'):
            Requested.choosearg = True
            i.active = True

@dp.message_handler(commands=['factorial'])
async def integral_func(message: types.Message):
    await message.answer(text='Напишите подфакториальное число', reply_markup = types.ReplyKeyboardRemove())
    for i in requested:
        if(i.name == 'factorial'):
            Requested.choosearg = True
            i.active = True

@dp.message_handler(commands=['logarithm'])
async def log_func(message: types.Message):
    await message.answer(text='Напишите аргумент (число, которое нужно получить при возведении в логарифм) и '
                              'основания логарифма через запятую.',
                         reply_markup=types.ReplyKeyboardRemove())
    for i in requested:
        if i.name == 'logarithm':
            Requested.choosearg = True
            i.active = True

@dp.message_handler(commands=['lcm'])
async def lcm_func(message: types.Message):
    await message.answer(text='Напишите две зависимые переменные через запятую.', reply_markup = types.ReplyKeyboardRemove())
    for i in requested:
        if(i.name == 'lcm'):
            Requested.choosearg = True
            i.active = True

@dp.message_handler(commands=['elevation'])
async def elev_func(message: types.Message):
    await message.answer(text='Отправьте число и степень, в которую необходимо возвести'
                              ' число через запятую')
    for i in requested:
        if i.name == 'elevation':
            Requested.choosearg = True
            i.active = True


@dp.message_handler()
async def recieved_message(message: types.Message):
    if(Requested.choosearg):
        Requested.choosearg = False
        Requested.listarg = list(message.text.split(','))
        for i in requested:
            if(i.active):
                if(i.name == 'derivative'):
                    await message.answer(text='Напишите функцию')
                elif(i.name == 'integral'):
                    await message.answer(text='Напишите подынтегральную функцию.')
                elif(i.name == 'lim'):
                    await message.answer(text='Напишите функцию.')
                elif(i.name == 'taylorseq'):
                    await message.answer(text='Напишите функцию.')
                elif(i.name == 'asymptotes'):
                    await message.answer(text='Напишите функцию.')
                break
    temp:bool = False
    for i in requested:
        if(i.active):
            temp = True
            await message.answer(text=i.calculate(message.text, Requested.listarg), reply_markup = calculatorkb)
            i.active = False
            Requested.listarg = list()
            break
    if(not(temp)):
        await message.answer(text="Простите, я вас не понимаю")



#if __name__ != '__main__':
executor.start_polling(dp, skip_updates=True)
