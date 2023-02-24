import telebot
from config import token
import tarkov

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message) -> None:
    bot.send_message(message.chat.id, "Привет! Я сделан для парcинга данных о предметах Escape from Tarkov"
                                      "Для того, чтобы узнать список доступных команд напишите '/help'.")


@bot.message_handler(commands=["help"])
def help_cmd(message) -> None:
    bot.send_message(message.chat.id, "Список доступных команд: 1) /history - Выведет историю ваших запросов\n"
                                      "                         2) /search - команда для поиска полной "
                                      "информации о предмете\n"
                                      "                         3) /suminfo [name] - краткая информация о "
                                      "предмете(буфер)\n"
                                      "                         4) /clear_history - очистка истории\n")


@bot.message_handler(commands=["search"])
def search(message) -> None:
    item = str(message.text[8:])
    data = tarkov.request(item)
    for key, value in data.items():
        if key == "Цена у торговца":
            str1 = key + ": " + str(value) + " " + data["Валюта торговца"]
        elif key == "Валюта торговца":
            continue
        elif isinstance(value, bool):
            if value:
                str1 = key + ": да"
            elif not value:
                str1 = key + ": нет"
        else:
            str1 = key + ": " + str(value)
        bot.send_message(message.chat.id, str1)


@bot.message_handler(commands=["suminfo"])
def search(message) -> None:
    item = str(message.text[8:])
    data = tarkov.request(item)
    for key, value in data.items():
        if key == "Название":
            str2 = key + ": " + str(value)
            bot.send_message(message.chat.id, str2)
        elif key == "Валюта торговца":
            continue
        elif isinstance(value, bool):
            if value:
                str2 = key + ": да"
                bot.send_message(message.chat.id, str2)
            elif not value:
                str2 = key + ": нет"
                bot.send_message(message.chat.id, str2)
        elif key == "Цена":
            str2 = key + ": " + str(value)
            bot.send_message(message.chat.id, str2)
        elif key == "Торговец":
            str2 = key + ": " + str(value)
            bot.send_message(message.chat.id, str2)
        elif key == "Цена у торговца":
            str2 = key + ": " + str(value) + " " + data["Валюта торговца"]
            bot.send_message(message.chat.id, str2)


@bot.message_handler(content_types=["text"])
def hello(message) -> None:
    text = message.text.lower()
    if text == "привет":
        bot.send_message(message.chat.id, "Здравствуйте, я бот")
    else:
        bot.send_message(message.chat.id, "")


if __name__ == '__main__':
    bot.infinity_polling()
