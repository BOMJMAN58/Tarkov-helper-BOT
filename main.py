from telebot import types
import telebot
import config
import tarkov
from db import SQLighter
import os
from dotenv import load_dotenv


load_dotenv()
bot = telebot.TeleBot(os.getenv("token"))


@bot.message_handler(commands=["start"])
def start(message) -> None:
    """
    Выводит вступление
    :param message:
    :return: None
    """
    db_worker = SQLighter(config.database_name)
    db_worker.add_log(message.chat.id, message.text)
    db_worker.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/help")
    btn2 = types.KeyboardButton("/history")
    btn3 = types.KeyboardButton("/clearHistory")
    btn4 = types.KeyboardButton("/giveMax")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я сделан для парcинга данных о предметах Escape from Tarkov"
                          "Для того, чтобы узнать список доступных команд напишите '/help'.".format(
                           message.from_user), reply_markup=markup)


@bot.message_handler(commands=["help"])
def help_cmd(message) -> None:
    """
    Выводит список доступных команд
    :param message:
    :return: None
    """
    db_worker = SQLighter(config.database_name)
    db_worker.add_log(message.chat.id, message.text)
    db_worker.close()
    bot.send_message(message.chat.id, "Список доступных команд:\n 1) /history - Выведет историю ваших запросов\n"
                                      "2) /search [name] - поиск полной информации о предмете\n"
                                      "3) /suminfo [name] - краткая информация о предмете(буфер)\n"
                                      "4) /clearHistory - очистка истории\n"
                                      "5) /start - Введение\n"
                                      "6) /giveMax - самый дорогой элемент на барахолке")


@bot.message_handler(commands=["history"])
def start(message) -> None:
    """
    Выводит пользователю историю его команд
    :param message:
    :return: None
    """
    db_worker = SQLighter(config.database_name)
    hist = db_worker.select_all(message.chat.id)
    db_worker.close()
    if not hist:
        bot.send_message(message.chat.id, "Нет записей")
    counter = 1
    hist.reverse()
    for event in hist:
        answer = f"{counter}. " + event[0]
        counter += 1
        if counter == 11:
            break
        bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=["clearHistory"])
def start(message) -> None:
    """
    Очищает историю команд пользователя
    :param message:
    :return: None
    """
    db_worker = SQLighter(config.database_name)
    db_worker.del_log(message.chat.id)
    db_worker.close()
    bot.send_message(message.chat.id, "История очищена")


@bot.message_handler(commands=["giveMax"])
def give_max(message) -> None:
    """
    Передаёт сообщение о самом дорогом элементе на барахолке
    :param message:
    :return:None
    """
    db_worker = SQLighter(config.database_name)
    db_worker.del_log(message.chat.id)
    db_worker.close()
    max_item = tarkov.request_2()
    bot.send_message(message.chat.id, str(max_item))


@bot.message_handler(commands=["search"])
def search(message) -> None:
    """
    Выводит полную информацию о предмете
    :param message:
    :return: None
    """
    db_worker = SQLighter(config.database_name)
    db_worker.add_log(message.chat.id, message.text)
    db_worker.close()
    item = str(message.text[8:])
    if not item:
        bot.send_message(message.chat.id, "Вы не ввели название предмета")
    else:
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
    """
    Выводит основную информацию о предмете
    :param message:
    :return: None
    """
    db_worker = SQLighter(config.database_name)
    db_worker.add_log(message.chat.id, message.text)
    db_worker.close()
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
    """
    Сообщение пользователю о том, что он ввёл неверную команду
    :param message:
    :return: None
    """
    bot.send_message(message.chat.id, "Я вас не понял.\n"
                                      "Список команд: '/help'")


if __name__ == '__main__':
    bot.infinity_polling()
