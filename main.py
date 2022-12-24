########################################################################################################################
"""                                                   Библиотеки                                                     """
########################################################################################################################

import telebot
# import requests as r
import time
import codecs
import random
import sqlite3 as sq

########################################################################################################################
"""                                              Настройка бота и файлов                                             """
########################################################################################################################

bot = telebot.TeleBot('5670044864:AAHC4Cj8DguEZ-2s0LXIbaNgiril_Gz6rvg')

black_list = codecs.open('black_list.txt', 'r', 'utf-8')
words = black_list.read().strip(' ,.').split()

stick_file = open('stickers.txt', 'r')
stick = stick_file.read().strip().split()

########################################################################################################################
"""                                                   База данных                                                    """
########################################################################################################################

with sq.connect('users.db') as con:
    con = sq.connect('users.db', check_same_thread=False)
    cur = con.cursor()

    data = cur.execute("SELECT telegram_user_id FROM user_inf;")
    user_id = []

    for i in data:
        user_id.append(i[0])

########################################################################################################################
"""                                                   Команды бота                                                   """


########################################################################################################################

@bot.message_handler(commands=['start'])  # если бот получает команду "/start"
def start(message):
    mess = f'''
Ну привіт, {message.from_user.first_name}!
Мене звати Алічка, я бот Арлеса, яку створили на зразок його дружини. Поки що я вмію не багато, але продовжую \
розвиватися.
Я самий перший бот мого Творця, тому сподіваюся на щасливе своє майбутнє!
Напиши "/help", щоб подивитися мої поточні команди!'''
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['help'])  # если бот получает команду "/help"
def help(message):
    commands = f'''
* Напиши мені "привіт" / "привет", щоб я з тобой привіталася!
 
* Хочеш дізнатися ID свого акаунта? Напиши "id"!

* Якщо тобі недостатньо мілоти у житті, тоді напиши меня "надішли кота" / "пришли кота" — і я це зроблю!

* Хтось невдало пожартував, скинув дурний мем, чи інша ситуація, де потрібно посміятися? Напиши "Аля, посмійся" / "Аля,\
 посмейся"!

* О ні! Тобі сумно? Напиши "Аля, підбадьор мене" — і я тобі допоможу!
'''
    bot.send_message(message.chat.id, commands)


@bot.message_handler(content_types=['text'])  # если бот получает текст (в личных сообщениях или в группе)
def get_user_text(message):
    for i in words:
        if i in message.text.lower():
            bot.reply_to(message, 'Якщо ти не припиниш, то тебе забанять :)')
            bot.send_message(954233253,
                             f'В чате "{message.chat.title}" (@{message.chat.username}) {message.from_user.first_name} '
                             f'(@{message.from_user.username}) отправил запрещенное слово — "{message.text}".')
            time.sleep(1.3)
            bot.delete_message(message.chat.id, message.id)

        # with sqlite3.connect('users.db') as con:
        #     cur = con.cursor()
        #     cur.execute("UPDATE chat_user_info SET ")

    if message.from_user.id not in user_id:
        with sq.connect('users.db') as con:
            cur = con.cursor()
            user_id.append(message.from_user.id)
            cur.execute(f"INSERT INTO user_inf VALUES(?, ?, ?, ?);", (message.from_user.id, message.from_user.first_name, message.from_user.username, 0))
            bot.reply_to(message, 'Додала тебе у базу.')
            con.commit()

    if ('спасибо тебе' in message.text.lower().strip(' .,') and message.reply_to_message != 'None') \
            or ('спасибо' == message.text.lower().strip(' .,') and message.reply_to_message != 'None') \
            or ('+' == message.text.lower().strip(' .,') and message.reply_to_message != 'None')\
            or ('дякую' == message.text.lower().strip(' .,') and message.reply_to_message != 'None')\
            or ('подяка' == message.text.lower().strip(' .,') and message.reply_to_message != 'None'):
        if (message.reply_to_message.from_user.is_bot is True):
            bot.reply_to(message, 'Це бот, бовдур')
        else:
            with sq.connect('users.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE user_inf SET rating = rating + 1 WHERE telegram_user_id == :id",
                        {"id": message.reply_to_message.from_user.id})
                bot.send_message(message.chat.id, 'Вау, пушка, ти став краще! В-)', reply_to_message_id=message.reply_to_message.id)
                con.commit()

    if ('ганьба' in message.text.lower().strip(' .,') and message.reply_to_message != 'None') \
            or ('-' == message.text.lower().strip(' .,') and message.reply_to_message != 'None'):
        if (message.reply_to_message.from_user.is_bot is True):
            bot.reply_to(message, 'Це бот, бовдур')
        else:
            with sq.connect('users.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE user_inf SET rating = rating - 1 WHERE telegram_user_id == :id",
                        {"id": message.reply_to_message.from_user.id})
                bot.send_message(message.chat.id, 'Ну... Вітаю, ти став гірше!', reply_to_message_id=message.reply_to_message.id)
                con.commit()

    if message.text.lower().strip(' .,') == 'привет' or message.text.lower().strip(' .,') == 'привіт':
        mess = f'І тобі привітання, {message.from_user.first_name}!'
        bot.reply_to(message, mess)
    elif message.text.lower().strip(' ,.') == 'мой рейтинг' or message.text.lower().strip(' ,.') == 'мій рейтинг':
        with sq.connect('users.db') as con:
            cur = con.cursor()
            cur.execute(f"SELECT rating FROM user_inf WHERE telegram_user_id = {message.from_user.id};")
            current_rating = cur.fetchone()
            bot.reply_to(message, f'Прошу — {current_rating[0]}')

    elif message.text.lower().strip(' ,.') == 'топ рейтинг':
        with sq.connect('users.db') as con:
            cur = con.cursor()
            cur.execute(f'SELECT rating,first_name FROM user_inf ORDER BY rating DESC LIMIT 5;')
            top5 = cur.fetchall()
            msg = f"""
1. {top5[0][1]} — {top5[0][0]};
2. {top5[1][1]} — {top5[1][0]};
3. {top5[2][1]} — {top5[2][0]};
4.  {top5[3][1]} — {top5[3][0]};
5. {top5[4][1]} — {top5[4][0]}."""
            bot.send_message(message.chat.id, msg)


    elif message.text.lower().strip(' .,?') == 'аля':
        bot.reply_to(message, 'Це я')
    elif message.text.lower().strip(' .,') == 'id':
        bot.reply_to(message, f'Твій id — {message.from_user.id}')
    elif 'пришли кота' in message.text.lower().strip(' .,') or 'надішли кота' in message.text.lower().strip(' .,'):
        photo = open('D:/Bots/Alya/Cats/kitten.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, 'Це я!', reply_to_message_id=message.id)
    elif message.text.lower().replace(',', '') == 'аля посмейся' or message.text.lower().replace(',',
                                                                                                 '') == 'аля посмійся':
        bot.reply_to(message, 'АХАХАХАХАХАХ')
    elif message.text.lower().strip(' .,').replace(',', '') == 'аля подбодри меня' \
            or message.text.lower().strip(' .,').replace(',', '') == 'аля поддержи меня' \
            or message.text.lower().strip(' .,').replace(',', '') == 'мне нужна поддержка' \
            or message.text.lower().strip(' .,').replace(',', '') == 'поддержи меня' \
            or message.text.lower().strip(' .,').replace(',', '') == 'подбодри меня' \
            or message.text.lower().strip(' .,').replace(',', '') == 'аля підбадьор мене' \
            or message.text.lower().strip(' .,').replace(',', '') == 'аля підтримай мене' \
            or message.text.lower().strip(' .,').replace(',', '') == 'мені потрібна підтримка' \
            or message.text.lower().strip(' .,').replace(',', '') == 'підтримай мене' \
            or message.text.lower().strip(' .,').replace(',', '') == 'підбадьор мене':
        photo = open('D:/Bots/Alya/news.png', 'rb')
        bot.send_photo(message.chat.id, photo, reply_to_message_id=message.id, caption='Завжди рада допомогти!')
    elif 'кек' in message.text.lower().strip(' ,.').replace(',', ''):
        video = open('D:/Bots/Alya/omare.mp4', 'rb')
        bot.send_video(message.chat.id, video, reply_to_message_id=message.id)
    elif 'мотивация' in message.text.lower().strip(' ,.').replace(',', '') or \
            'мотивація' in message.text.lower().strip(' ,.').replace(',', ''):
        video = open('D:/Bots/Alya/motivation.mp4', 'rb')
        bot.send_video(message.chat.id, video, reply_to_message_id=message.id, caption='Мотиватор Всесвіту на місці')
    elif message.text.lower().strip(' ,.') == 'инфа' and message.from_user.id == 954233253:
        bot.send_message(954233253, message.reply_to_message)
        bot.delete_message(message.chat.id, message.id)

    x = random.randint(0, 50)  # роляем рандомно одно число, если в результате 3, то бот отправляет стикер
    if x == 3:
        bot.send_sticker(message.chat.id, random.choice(stick), reply_to_message_id=message.id)


########################################################################################################################
"""                                                   Работа бота                                                    """
########################################################################################################################


bot.polling(none_stop=True)
