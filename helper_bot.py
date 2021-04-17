import telebot
from keyboard import main_keyboard, back_keyboard_check, keyboard_qiwi, checks_and_balances_keyboard, back, tinkoff, screens, sber, admin, rassilka_keyboard, mail, deanon_keyboard
from telebot.types import InputMediaPhoto
import sqlite3
import PIL
from PIL import Image, ImageFont, ImageDraw
import json
import random
import os
import time
import datetime
import requests
import sys
import bs4

import urllib.request, phonenumbers, sqlite3, os

from datetime import datetime, date, timedelta

from phonenumbers import geocoder, carrier, timezone

from bs4 import BeautifulSoup as bs

import threading
from telebot import types
global ADMIN_ID
ADMIN_ID = 1413651617 #Сюда свой айди

token = '1789386623:AAENBTZ_4uXEjr_bw55F4sSjYmw7eeAFnwc' #Токен бота

bot = telebot.AsyncTeleBot(token)

@bot.message_handler(commands=['start']) #Авторизация пользователей, выдача кол-ва пользователей админу.
def start_message(message):
    con = sqlite3.connect('counter.db')
    cur = con.cursor()
    db = sqlite3.connect('users.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT
    )""")
    
    con.commit()
    db.commit()
    id = message.chat.id
    sql.execute(f"SELECT id FROM users WHERE id = '{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?)", (id,))
        cur.execute(f"SELECT count FROM counter")
        c = cur.fetchone()[0] + 1
        print(c)
        cur.execute(f"UPDATE counter SET count = {c}")
        bot.send_message(message.chat.id, '🧾Привет! У меня ты сможешь сделать фейк чеки популярных приложений. Надеюсь тебе понравится :)\n⚠️Воспользуйся кнопками для управления ботом\nПо всем вопросам: @scm_takashi', reply_markup=main_keyboard())
        db.commit()
        con.commit()
    else: 
        bot.send_message(message.chat.id, '🧾Привет, у меня ты сможешь сделать фейк чеки популярных приложений. Надеюсь тебе понравится :)\n⚠️Воспользуйся кнопками для управления ботом\nПо всем вопросам: @scm_takashi', reply_markup=main_keyboard())
   
@bot.message_handler(content_types="text") #Работа бота
def main(message):
    if message.text == '📝Отрисовка (Чеки, балансы)':
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=checks_and_balances_keyboard())
        bot.register_next_step_handler(message, checks_and_balances)
    elif message.text == "🖼Готовые скрины":
        bot.send_message(message.chat.id, 'Готовые чеки, выберите категорию:',reply_markup=screens())
        bot.register_next_step_handler(message, screen)
    elif message.text == "👁Информация":
        con = sqlite3.connect('counter.db')
        cur = con.cursor()
        cur.execute("SELECT count FROM counter")
        count = cur.fetchone()[0]        
        bot.send_message(message.chat.id, f"👁Информация\n\nВаш id: {message.chat.id}\nАдмин Бота: @scm_takashi\n\nПользователей в Боте: {count}", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "Админ" and message.chat.id == ADMIN_ID:        
        bot.send_message(message.chat.id, "Вы перешли в меню админа", reply_markup=admin())
        bot.register_next_step_handler(message, admin_panel)
    elif message.text == "🙋Здесь могла быть твоя реклама!":
        bot.send_message(message.chat.id, "Заказать рекламу: @scm_takashi", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "📩Отрисовка писем":
        bot.send_message(message.chat.id, "Выберите категорию: ", reply_markup=mail())
        bot.register_next_step_handler(message, mail_)
    elif message.text == "🚨Деанон":
        bot.send_message(message.chat.id, "Введите номер телефона (вместе с +):", reply_markup=deanon_keyboard())
        bot.register_next_step_handler(message, deanon)
    elif message.text == "Нaзад":
        bot.send_message(message.chat.id, "Выберите категорию: ")
        bot.register_next_step_handler(message, mail_)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def mail_(message):
    if message.text == "Письмо Avito":
        bot.send_message(message.chat.id, "Введите текст письма: ", reply_markup=back())
        bot.register_next_step_handler(message, mail_avito)
    elif message.text == "Письмо Юла":
        bot.send_message(message.chat.id, "Введите текст письма: ", reply_markup=back())
        bot.register_next_step_handler(message, mail_youla)
    elif message.text == "⬅️Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def mail_avito(message):
    if message.text == "⬅️Назад":       
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Введите текст письма: ")
                bot.register_next_step_handler(message, mail_avito)
            else:
                try:
                    text = message.text
                    tink = Image.open('Image source/mail_avito.png')
                    font = ImageFont.truetype('Fonts/arial.ttf', 22)
                    d = ImageDraw.Draw(tink)
                    d.text((26,486), text, font=font, fill=(0, 0, 0,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, mail_avito)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def mail_youla(message):
    if message.text == "⬅️Назад":       
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Введите текст письма: ")
                bot.register_next_step_handler(message, mail_youla)
            else:
                try:
                    text = message.text
                    tink = Image.open('Image source/mail_youla.png')
                    font = ImageFont.truetype('Fonts/arial.ttf', 22)
                    d = ImageDraw.Draw(tink)
                    d.text((26,486), text, font=font, fill=(0, 0, 0,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, mail_youla)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
        
def admin_panel(message):
    if message.text == "Сделать рассылку" and message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Введите текст рассылки: ", reply_markup=rassilka_keyboard())
        bot.register_next_step_handler(message, rassilka)
    elif message.text == "Выход" and message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Выход из панели админа", reply_message=main_keyboard())
        bot.register_next_step_handler(message, main)
def rassilka(message):
    if message.text == "Отменить" and message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Отменено", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text and message.chat.id == ADMIN_ID:
        text = message.text
        db = sqlite3.connect('users.db')
        sql = db.cursor()
        sql.execute("SELECT id FROM users")
        id = sql.fetchall()
        for id in id:
            for id in id:
               try:
                bot.send_message(id, f"{text}")
                time.sleep(1)
               except:
                   sql.execute(f"DELETE FROM users WHERE id = {id}")
        bot.send_message(ADMIN_ID, "Рассылка завершена", reply_markup=main_keyboard())
        db.commit()
        bot.register_next_step_handler(message, main)

def screen(message):
    if message.text == "🇷🇺Авито":
        av1 = open('Screens/av1.jpg', 'rb')
        av2 = open('Screens/av2.jpg', 'rb')
        av3 = open('Screens/av3.jpg', 'rb')
        av4 = open('Screens/av4.jpg', 'rb')
        av5 = open('Screens/av5.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(av1),InputMediaPhoto(av2), InputMediaPhoto(av3), InputMediaPhoto(av4),InputMediaPhoto(av5)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "🇷🇺СДЕК":
        cd = open('Screens/cd.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(cd)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "🇷🇺BlaBlaCar":
        bbk1 = open('Screens/bbk1.jpg', 'rb')
        bbk2 = open('Screens/bbk2.jpg', 'rb')
        bbk3 = open('Screens/bbk3.jpg', 'rb')
        bbk4 = open('Screens/bbk4.jpg', 'rb')
        bbk5 = open('Screens/bbk5.jpg', 'rb')
        bbk6 = open('Screens/bbk6.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(bbk1),InputMediaPhoto(bbk2), InputMediaPhoto(bbk3), InputMediaPhoto(bbk4),InputMediaPhoto(bbk5), InputMediaPhoto(bbk6)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "🇰🇿OLX.KZ":
        kz1 = open('Screens/kz1.jpg', 'rb')
        kz2 = open('Screens/kz2.jpg', 'rb')
        kz3 = open('Screens/kz3.jpg', 'rb')
        kz4 = open('Screens/kz4.jpg', 'rb')
        kz5 = open('Screens/kz5.jpg', 'rb')
        kz6 = open('Screens/kz6.jpg', 'rb')
        kz7 = open('Screens/kz7.jpg', 'rb')
        kz8 = open('Screens/kz8.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(kz1),InputMediaPhoto(kz2), InputMediaPhoto(kz3), InputMediaPhoto(kz4),InputMediaPhoto(kz5), InputMediaPhoto(kz6), InputMediaPhoto(kz7), InputMediaPhoto(kz8)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "🇺🇦OLX.UA":
        ua1 = open('Screens/ua1.jpg', 'rb')
        ua2 = open('Screens/ua2.jpg', 'rb')
        ua3 = open('Screens/ua3.jpg', 'rb')
        ua4 = open('Screens/ua4.jpg', 'rb')
        ua5 = open('Screens/ua5.jpg', 'rb')
        ua6 = open('Screens/ua6.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(ua1),InputMediaPhoto(ua2), InputMediaPhoto(ua3), InputMediaPhoto(ua4),InputMediaPhoto(ua5), InputMediaPhoto(ua6)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "🇵🇱OLX.PL":
        pl1 = open('Screens/pl1.jpg', 'rb')
        pl2 = open('Screens/pl2.jpg', 'rb')
        pl3 = open('Screens/pl3.jpg', 'rb')
        pl4 = open('Screens/pl4.jpg', 'rb')
        pl5 = open('Screens/pl5.jpg', 'rb')
        pl6 = open('Screens/pl6.jpg', 'rb')
        pl7 = open('Screens/pl7.jpg', 'rb')
        pl8 = open('Screens/pl8.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(pl1),InputMediaPhoto(pl2), InputMediaPhoto(pl3), InputMediaPhoto(pl4),InputMediaPhoto(pl5), InputMediaPhoto(pl6), InputMediaPhoto(pl7), InputMediaPhoto(pl8)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "🇧🇾KUFAR.BY":
        by1 = open('Screens/by1.jpg', 'rb')
        by2 = open('Screens/by2.jpg', 'rb')
        by3 = open('Screens/by3.jpg', 'rb')
        by4 = open('Screens/by4.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(by1),InputMediaPhoto(by2), InputMediaPhoto(by3), InputMediaPhoto(by4)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "📞WhatsApp":
        wh1 = open('Screens/wh1.jpg', 'rb')
        wh2 = open('Screens/wh2.jpg', 'rb')
        bot.send_media_group(message.chat.id, [InputMediaPhoto(wh1),InputMediaPhoto(wh2)])
        bot.register_next_step_handler(message, screen)
    elif message.text == "⬅️Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def checks_and_balances(message):
    if message.text == "Тинькофф💛":
        bot.send_message(message.chat.id, '💛Доступные чеки Тинькофф:', reply_markup=tinkoff())
        bot.register_next_step_handler(message, tinkov)
    elif message.text == 'Сбер♻️':
        bot.send_message(message.chat.id, "♻️Сбер, Доступные чеки:", reply_markup=sber())
        bot.register_next_step_handler(message, sber_menu)
    elif message.text == 'QIWI🐥':
        bot.send_message(message.chat.id, '🐥Вы выбрали QIWI. \n Выберите категорию:', reply_markup=keyboard_qiwi())
        bot.register_next_step_handler(message, qiwi)
    elif message.text == "⬅️Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == 'ПриватБанк🔵':
        bot.send_message(message.chat.id, "OLX Приватбанк, заполните форму: \n\nСистемное время\nДата и время\nСумма перевода\nОстаток \n\n❗️Разделяйте параметры переносом строки❗️", reply_markup=back())
        bot.register_next_step_handler(message, privat)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def privat(message):
    if message.text == "⬅️Назад":       
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "OLX Приватбанк, заполните форму: \n\nСистемное время\nДата и время\nСумма перевода\nОстаток \n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, privat)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    date_time = text[1]
                    money = "-"+text[2]+" ГРН"
                    balance = text[3] + " ГРН"
                    tink = Image.open('Image source/privatbank.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 37)
                    font_date_time = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 43)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 80)
                    font_balance = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 57)
                    w1, h1 = font_money.getsize(money)
                    w2, h2 = font_balance.getsize(balance)
                    W = 1080
                    d = ImageDraw.Draw(tink)
                    d.text((945,45), time, font=font_time, fill=(228, 255, 194, 255))
                    d.text((51, 420), date_time, font=font_date_time, fill=(102, 102, 102,255))
                    d.text(((W - w1)/2,540), money, font=font_money, fill=(0,0,0,255))
                    d.text(((W - w2)/2, 1060), balance, font=font_balance, fill=(0,0,0,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, sber_transfer)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def sber_menu(message):
    if message.text == "♻️Перевод Сбер♻️":
        photo = open('Image reference/sber_transfer.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример перевода")
        time.sleep(0.2)
        bot.send_message(message.chat.id, "♻️Выбран перевод сбер. Заполните форму:\n\nСистемное время\nИмя получателя\nСумма \n\n❗️Разделяйте параметры переносом строки❗️")
        bot.register_next_step_handler(message, sber_transfer)
    elif message.text == "⬅️Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def sber_transfer(message):
    if message.text == "⬅️Назад":       
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "♻️Выбран перевод сбер. Заполните форму:\n\nСистемное время\nИмя получателя\nСумма \n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, sber_transfer)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    name = text[1]
                    money = text[2]+" ₽"
                    tink = Image.open('Image source/sber_transfer.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 39)
                    font_name = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 43)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 80)
                    d = ImageDraw.Draw(tink)
                    d.text((70,25), time, font=font_time, fill=(225, 238, 229,255))
                    d.text((200,245), name, font=font_name, fill=(255,255,255,255))
                    d.text((200, 325), money, font=font_money, fill=(255,255,255,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, sber_transfer)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
        

def tinkov(message):
    if message.text == "Тинькофф Перевод":
        photo = open('Image reference/tinkoff_transfer.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример перевода")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "Тинькофф перевод, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nНа карту\n\n❗️Разделяйте параметры переносом строки❗️",reply_markup=back())
        bot.register_next_step_handler(message, tinkov_tranfer)
    elif message.text == "⬅️Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "💲Оплата Авито":
        photo = open('Image reference/tinkoff_avito.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример оплаты")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "Тинькофф оплата Авито, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nПоследние 4 цифры вашей карты\nКэшбэк\n\n❗️Разделяйте параметры переносом строки❗️",reply_markup=back())
        bot.register_next_step_handler(message, tinkov_avito)
    elif message.text == "🌀Оплата Юла":
        photo = open('Image reference/tinkoff_youla.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример оплаты")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "Тинькофф оплата Юла, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nПоследние 4 цифры вашей карты\nКэшбэк\n\n❗️Разделяйте параметры переносом строки❗️",reply_markup=back())
        bot.register_next_step_handler(message, tinkov_youla)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def tinkov_youla(message):
    if message.text == "⬅️Назад":     
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Тинькофф оплата Юла, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nПоследние 4 цифры вашей карты\nКэшбэк\n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, tinkov_youla)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    date_time = text[1]
                    money = "– "+text[2]+"₽"
                    rec = "Tinkoff Black *"+text[3]
                    cashback = "+"+text[4]+" ₽"
                    tink = Image.open('Image source/tinkoff_youla_pay.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 39)
                    font_date_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 53)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 90)
                    font_rec = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
                    W = 1080
                    w1, h1 = font_time.getsize(money)
                    w2, h2 = font_time.getsize(cashback)
                    d = ImageDraw.Draw(tink)
                    d.text((70,25), time, font=font_time, fill=(195,195,195,255))
                    d.text((193,125), date_time, font=font_date_time, fill=(255,255,255,255))
                    d.text(((W - w1-260)/2, 755), money, font=font_money, fill=(255,255,255,255))
                    d.text(((W-44-w2),1861), cashback, font=font_rec, fill=(255,255,255,255))
                    d.text((190,1525), rec, font=font_rec, fill=(255,255,255,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, tinkov_youla)
                except Exception as ex:
                    print(ex)
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def tinkov_avito(message):
    if message.text == "⬅️Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Тинькофф оплата Авито, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма(только Рубли и копейки, остальное поставится за вас. Например 1500,00)\nПоследние 4 цифры вашей карты\nКэшбэк\n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, tinkov_avito)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    date_time = text[1]
                    money = "– "+text[2]+"₽"
                    rec = "Tinkoff Black *"+text[3]
                    cashback = "+"+text[4]+" ₽"
                    tink = Image.open('Image source/tinkoff_avito_pay.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 39)
                    font_date_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 53)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 90)
                    font_rec = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
                    W = 1080
                    w1, h1 = font_time.getsize(money)
                    w2, h2 = font_time.getsize(cashback)
                    d = ImageDraw.Draw(tink)
                    d.text((70,25), time, font=font_time, fill=(195,195,195,255))
                    d.text((193,125), date_time, font=font_date_time, fill=(255,255,255,255))
                    d.text(((W - w1-260)/2, 755), money, font=font_money, fill=(255,255,255,255))
                    d.text(((W-44-w2),1861), cashback, font=font_rec, fill=(255,255,255,255))
                    d.text((190,1525), rec, font=font_rec, fill=(255,255,255,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, tinkov_avito)
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def tinkov_tranfer(message):
    if message.text == "⬅️Назад":
            bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
    else:
        if message.text:
            if message.text == "Вернуться в Меню🧭":
                bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
            elif message.text == "Ещё раз":
                bot.send_message(message.chat.id, "Тинькофф перевод, заполните форму:\n\nСистемное время\nДата и время платежа\nСумма\nНа карту\n\n❗️Разделяйте параметры переносом строки❗️")
                bot.register_next_step_handler(message, tinkov_tranfer)
            else:
                try:
                    text = message.text.split("\n")
                    time = text[0]
                    date_time = text[1]
                    money = "– "+text[2]+"₽"
                    rec = text[3]
                    tink = Image.open('Image source/tinkoff_transfer.png')
                    font_time = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 39)
                    font_date_time = ImageFont.truetype('Fonts/Roboto-Medium.ttf', 53)
                    font_money = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 90)
                    font_rec = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
                    W = 1080
                    w1, h1 = font_time.getsize(money)
                    d = ImageDraw.Draw(tink)
                    d.text((70,25), time, font=font_time, fill=(195,195,195,255))
                    d.text((193,125), date_time, font=font_date_time, fill=(255,255,255,255))
                    d.text(((W - w1-260)/2, 755), money, font=font_money, fill=(255,255,255,255))
                    d.text((45,1878), rec, font=font_rec, fill=(255,255,255,255))
                    tink.save("Image cache/file3.png", "PNG")
                    img = open('Image cache/file3.png', 'rb')
                    bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                    bot.register_next_step_handler(message, tinkov_tranfer)
                except:
                    bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                    bot.register_next_step_handler(message, main)
        else:
            bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
def qiwi(message):
    if message.text == 'Фейк баланс💰':
        photo = open('Image reference/qiwi_balance.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример оплаты")
        time.sleep(0.1)
        bot.send_message(message.chat.id, "Какой баланс вы хотите?(Например 151,02. Знак ₽ поставится за вас!", reply_markup=back())
        bot.register_next_step_handler(message, qiwi_balance2)
    elif message.text == 'Фейк чек🧾':
        photo = open('Image reference/qiwi_transfer.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption="Пример оплаты")
        time.sleep(0.1)
        bot.send_message(message.chat.id, 'Введите сумму, номер перевода, дату и время в таком формате:\n151,92\n+79XXXXXXXXX\n01.12.2020 в 19:01', reply_markup=back())
        bot.register_next_step_handler(message, qiwi_check)
    elif message.text == "⬅️Назад":
        bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    else:
        bot.send_message(message.chat.id, "Неизвестная команда, возврат в меню", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
def qiwi_check(message):
    
    if message.text:
        
        if message.text == "⬅️Назад":
            bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
        else:
            try:
                text = message.text.split("\n")
                money = text[0] + " ₽"
                money2 = "- " + text[0].strip() + " ₽"
                phone = text[1].strip()
                date_time = text[2].strip()
                qiwi = Image.open('Image source/qiwi_check.png')
                font1 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 53)
                font2 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 38)
                font3 = ImageFont.truetype('Fonts/Roboto-Regular.ttf', 45)
                font4 = ImageFont.truetype('Fonts/Roboto-Bold.ttf', 45)
                W = 1080
                w1, h1 = font1.getsize(money2)
                w2, h2 = font1.getsize(phone)
                d = ImageDraw.Draw(qiwi)
                d.text(((W-w1)/2,685), money2, font=font1, fill=(0,0,0,255))
                d.text(((W-w2)/2 + 60,614), phone, font=font2, fill=(153,153,153,255))
                d.text((56,1890), date_time, font=font3, fill=(0,0,0,255))
                d.text((56,2072), money, font=font4, fill=(0,0,0,255))
                qiwi.save("Image cache/file3.png", "PNG")
                img = open('Image cache/file3.png', 'rb')
                bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
                bot.register_next_step_handler(message, qiwi_check2)
            except:
                bot.send_message(message.chat.id, 'Что-то пошло не так. Возврат в меню..', reply_markup=main_keyboard())
                bot.register_next_step_handler(message, main)
def qiwi_check2(message):
    if message.text == "Вернуться в Меню🧭":
        bot.send_message(message.chat.id, "Выберите категорию из списка:", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "Ещё раз":
        bot.send_message(message.chat.id, "Введите сумму, номер перевода, дату и время в таком формате:\n151,92\n+79XXXXXXXXX\n01.12.2020 в 19:01")
        bot.register_next_step_handler(message, qiwi_check)
    else:
        bot.register_next_step_handler(message, qiwi_check)



def qiwi_balance2(message):
    if message.text:
        if message.text == "⬅️Назад":
            bot.send_message(message.chat.id, 'Выберите категорию: ', reply_markup=main_keyboard())
            bot.register_next_step_handler(message, main)
        else:
            text = message.text + ' ₽'
            qiwi = Image.open("Image source/qiwi_balance.png")
            fnt = ImageFont.truetype("Fonts/Roboto-Bold.ttf", 100)
            W = 1080
            w, h = fnt.getsize(text)
            d = ImageDraw.Draw(qiwi)
            d.text(((W-w)/2,296), text, font=fnt, fill=(255,255,255,255))
            del d
            qiwi.save("Image cache/file5.png", "PNG")
            img = open('Image cache/file5.png', 'rb')
            bot.send_photo(message.chat.id, img, reply_markup=back_keyboard_check())
            bot.register_next_step_handler(message, qiwi_balance3)
    else:
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBpp5fySJBsFYzrW_-3NIHuxhBXbKEZAACowoAAt-gOUkrfo6J91AWFx4E')
        bot.send_message(message.chat.id, "Ты еблан? Текст нужен")
        bot.register_next_step_handler(message, qiwi_balance2)

def qiwi_balance3(message):
    if message.text == "Вернуться в Меню🧭":
        bot.send_message(message.chat.id, "Возврат в меню...", reply_markup=main_keyboard())
        bot.register_next_step_handler(message, main)
    elif message.text == "Ещё раз":
        bot.send_message(message.chat.id, "Какой баланс вы хотите?(Например 151,02. Знак ₽ поставится за вас!")
        bot.register_next_step_handler(message, qiwi_balance2)
def deanon(message):
        if str(message.text) == 'Вернуться в Меню🧭':
            bot.send_message(message.chat.id, 'Возврат в меню...', parse_mode='HTML', reply_markup=main_keyboard)
        else:
                try:
                    if '+' in str(message.text):                    
                            z = phonenumbers.parse(str(message.text), None)
                            vall = phonenumbers.is_valid_number(z)
                            if vall == True:
                                vall = 'Существует'
                            else:
                                vall = 'Не существует'
                            coun = geocoder.description_for_number(z, 'ru')
                            timee = timezone.time_zones_for_geographical_number(z)
                            oper = carrier.name_for_number(z, "ru")
                    
                            uty = requests.get("https://api.whatsapp.com/send?phone="+str(message.text))
                            if uty.status_code==200:
                                utl2 = f'https://api.whatsapp.com/send?phone={message.text}'
                                what = types.InlineKeyboardMarkup(row_width=2)
                                what.add(
                                types.InlineKeyboardButton(text='✅ Whatsapp', url=utl2),
                                )
                            else:
                                utl2 = 'Не существует'
                                what = types.InlineKeyboardMarkup(row_width=2)
                                what.add(
                                types.InlineKeyboardButton(text='✅ Whatsapp', url=utl2)                            )
                            answer = ''
                            try:
                                resAV = requests.get('https://mirror.bullshit.agency/search_by_phone/'+str(message.text))
                                contentAV = bs(resAV.text, 'html.parser')
                                h1 = contentAV.find('h1')
                                if h1.text == '503 Service Temporarily Unavailable':
                                    answer += f'Процесс невозможен, попробуйте позже'
                                else:
                                    for url in contentAV.find_all(['a']):
                                        user_link = url['href']
                                        try:
                                            avito_url = requests.get('https://mirror.bullshit.agency'+user_link)#подпишись на канал по сливам схем/скриптов t.me/TRIGONPRO
                                            content = bs(avito_url.text, 'html.parser')
                                            url = content.find(['a'])
                                            
                                            linkAV = url['href']
                                            answer += f'{linkAV}\n'
                                        except:
                                            answer += f'{user_link}\n'
                                            continue
                            except:
                                answer += 'Не найдено'
                            if answer == '' or answer == ' ':
                                answer += 'Не найдено'
                            else:
                                pass
                            num = str(message.text)
                            rq = requests.post('https://www.instagram.com/accounts/account_recovery_send_ajax/',
                                        data={'email_or_username':num[1:]},
                                        headers={'accept-encoding':'gzip, deflate, br', 'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                                        'content-type':'application/x-www-form-urlencoded', 'cookie':'ig_did=06389D42-D5BA-42C2-BCA6-49C2913D682B; csrftoken=SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL; mid=XyIqeAALAAF1N7j0GbPCNuWhznuX; rur=FRC; urlgen="{\"109.252.48.249\": 25513\054 \"109.252.48.225\": 25513}:1k5JBz:E-7UgfDDLsdtlKvXiWBUphtFMdw"',
                                        'referer':'https://www.instagram.com/accounts/password/reset/', 'origin':'https://www.instagram.com',
                                        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.95 (Edition Yx)',
                                        'x-csrftoken':'SSEx9Bf0HmcQ8uCJVmh66Z4qBhu1F0iL', 'x-ig-app-id':'936619743392459',
                                        'x-instagram-ajax': 'a9aec8fa634f', 'x-requested-with': 'XMLHttpRequest'})
                            aq = rq.json()
                            if aq['status'] == 'ok':
                                insta = 'Существует'
                            else:
                                insta = 'Не существует'
                            user_all_info = f"""
<b>ℹ️ Информация по номеру {message.text}</b>:

├{z}
├<b>Страна</b>: <code>{coun}</code>
├<b>Оператор</b>: <code>{oper}</code>
├<b>Существование</b>: <code>{vall}</code>
├<b>Часовой пояс</b>: <code>{timee}</code>
├<b>Avito</b>: <code>{answer}</code>
├<b>Instagram</b>: <code>{insta}</code>
└<b>WhatsApp</b>: {utl2}"""
                            bot.send_message(message.chat.id, user_all_info, parse_mode='HTML', reply_markup=what, disable_web_page_preview = True)
                            bot.send_message(message.chat.id, 'Возврат в меню...', parse_mode='HTML', reply_markup=main_keyboard)
                            func.act_count_deanon("add", message.chat.id,)
                    else:
                        bot.send_message(message.chat.id, f'Введите пожалуйста номер телефона заново.', parse_mode='HTML', reply_markup=main_keyboard)
                except Exception as e:
                    bot.send_message(message.chat.id, 'Произошла ошибка, попробуй еще раз', reply_markup=main_keyboard)#подпишись на канал по сливам схем/скриптов t.me/TRIGONPRO
                    print(e)
                
                
                

if __name__ == '__main__':
    bot.polling(none_stop=True)