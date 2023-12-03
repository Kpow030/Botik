import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message):
    bot.send_message(message.chat.id, f'Здравствуйте, <b>{message.from_user.first_name}</b>, '
                                      f'здесь вы можете проконвертировать валюты!\n'
                     f'Инструкция по конвертированию: \n'
                     f'1 - <b>валюта, цену которой надо узнать</b>\n'
                     f'2 - <b>валюта, в которой надо узнать цену первой валюты</b>\n'
                     f'3 - <b>количество первой валюты</b>\n'
                     f'Параметры вводятся в строчку разделяя пробелом\n'
                     f'Например:\n'
                     f'<b> доллар рубль 1</b>\n'
                     f'Что-бы посмотреть весь список валют воспользуйтесь /values', parse_mode='html')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
