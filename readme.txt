Skillbox_Bunin_AV_bot - бот, для поиска информации о предметах игры escape from tarkov.

Используемые библиотеки: telebot(pip install pytelegtambotAPI)
                         sqlite3
                         requests
                         json
                         os
                         getenv


Команды:
    /history - Выведет историю ваших запросов
    /search [name] - команда для поиска полной информации о предмете
    /suminfo [name] - краткая информация о предмете(буфер)
    /clearHistory - очистка истории
    /start - Введение
    /help
    /giveMax - самый дорогой предмет

Запуск бота производится запуском main.py, база данных создаётся в репозитории и имеет одну таблицу для истории запросов
пользователей