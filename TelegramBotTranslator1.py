from googletrans import Translator
import telebot
from telebot import types

bot = telebot.TeleBot('5************************0')

translator = Translator()
@bot.message_handler(commands=['start'])
def start(message): #чтобы отслеживать команды /start
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Переведи текст")
    markup.add(btn1)
    mess = f'Hello, {message.from_user.first_name} ! Я переводчик с английского на русский и наоборот :)'
    bot.send_message(message.chat.id, mess, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):

    if (message.text == "Отмена"):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Переведи текст")
        markup.add(btn2)
        mess = f'Вы вернулись к главному меню'
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
    elif (message.text == "Переведи текст"):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='RU', callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='EN', callback_data=2))

        bot.send_message(message.chat.id, "Выбери язык, на который хочешь перевести текст.", parse_mode='html', reply_markup=markup)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Переведи текст")
        markup.add(btn2)
        mess = f'Не понял тебя(... Жми на кнопку или напиши: "Переведи текст".'
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

def next_trans2(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text = message.text
        lang = 'en'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)

def next_trans3(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text = message.text
        lang = 'ru'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)

@bot.callback_query_handler(func= lambda call:True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)
    answer = ''
    if call.data == '1':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="Выбрать другой язык.", callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text="Отмена", callback_data=4))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id,
                                    text = "Введите текст для перевода", reply_markup= markup)
        bot.register_next_step_handler(msg, next_trans3)
    elif call.data == '2':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="Выбрать другой язык.", callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text="Отмена", callback_data=4))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id,
                                    text = "Введите текст для перевода", reply_markup= markup)
        bot.register_next_step_handler(msg, next_trans2)
    elif call.data == '3':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text="RU", callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text="EN", callback_data=2))
        msg = bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id,
                                    text = "Выбери язык, на который хочешь перевести текст", reply_markup= markup)
    elif call.data == '4':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton("Переведи текст")
        markup.add(btn2)
        mess = f'Вы вернулись в главное меню!'
        bot.send_message(call.message.chat.id, mess, parse_mode='html', reply_markup=markup)

bot.polling()

