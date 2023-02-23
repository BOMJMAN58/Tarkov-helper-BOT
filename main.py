import telebot
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["hello-world"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, "Вы поздоровались с миром, а мир поздоровался с вами!")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    text = message.text.lower()
    if text == "привет":
        bot.send_message(message.chat.id, "Здравствуйте, Я бот Александра, пока нахожусь на стадии разработки...")
    else:
        bot.send_message(message.chat.id, "Пока я умею только здороваться и знаю команду - '/hello-world' :)")


if __name__ == '__main__':
    bot.infinity_polling()
