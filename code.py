import requests
import pymorphy2

from tkinter import *
from googletrans import Translator

morph = pymorphy2.MorphAnalyzer()

root = Tk()


def kelvin_to_celsius(temp):
    return round(temp - 273.15, 2)


def eng_to_rus(city):
    translator = Translator(service_urls=['translate.googleapis.com'])
    result = translator.translate(city, src='en', dest='ru')
    p = morph.parse(result.text)[0]
    city = p.inflect({'loct'}).word
    if len(city) > 1:
        city = city.split()[-1]
    return city[0].upper() + city[1:]


def get_weather():
    city = cityField.get()
    api_key = '28eded49f31842a06cc280df5ab95800'  # нужно получить на OpenWeathepMap ссылка: https://openweathermap.org/
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    params = {'APPID': api_key, 'q': city}
    result = requests.get(url, params=params)
    weather = result.json()
    info['text'] = f'Информация о погоде в {eng_to_rus(str(weather["name"]))}:\n\n' \
                   f'Средняя температура: {kelvin_to_celsius(weather["main"]["temp"])}°C\n' \
                   f'Скорость ветера: {weather["wind"]["speed"]}м/с\n' \
                   f'Облачность: {weather["clouds"]["all"]}%\n' \
                   f'Видимость: {weather["visibility"]}м'


def clear():
    cityField.delete(0, 'end')


root['bg'] = '#fafafa'
root.title('Погодное приложение')
root.geometry('400x300')

root.resizable(width=False, height=False)
# Верхний прямоугольник
frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.15, rely=0.03, relwidth=0.7, relheight=0.20)
# Нижний прямоугольник
frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.15, rely=0.35, relwidth=0.7, relheight=0.55)
# Строка ввода
cityField = Entry(frame_top, bg='white', justify=CENTER, font=('Helvetica', 11))
cityField.pack()
# Кнопка
btn = Button(frame_top, text='Посмотреть погоду', command=get_weather, font=('Helvetica', 11))
btn.pack()
# Инфомарция о погоде
info = Label(frame_bottom, text='Информация о погоде', bg='#ffb700', font=('Helvetica', 11))
info.pack()

# Добавить кнопку clear
cls_btn = Button(frame_top, text='X', command=clear)
cls_btn.pack()
cls_btn.place(height=21, width=21, relx=0.82, rely=0)

root.mainloop()
