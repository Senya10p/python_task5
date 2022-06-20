import telebot
import random

token = ''

bot = telebot.TeleBot(token)

HELP = """
Список доступных команд:
/help - напечатать справку по программе.
/add - добавить задачу в список (название задачи запрашиваем у пользователя).
/show - напечатать все добавленные задачи.
/random - добавить рандомную задачу в список на сегодня.
"""

RANDOM_TASKS = ['Написать Гвидо письмо', 'Выучить Python', 'Записаться на курс в Нетологию', 'Посмотреть 4 сезон Рик и Морти']

tasks = {}
category = {}

# команда help - отобразит все команды
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

# добавляем задачу на дату
def add_todo(date, task):
    if False == (date in tasks):
        tasks[date] = []
    tasks[date].append(task)

# команда добавления задачи на дату
@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit = 2)
    if (len(command) < 3):
        bot.send_message(message.chat.id, "При добавлении нужно указать дату и задачу.")
        return
    date = command[1].lower()
    task = command[2]
    task_text = task.split('@', 1)[0]
    if (False == check_task(task_text)):
        bot.send_message(message.chat.id, "Название задачи должно быть не менее 3х символов.")
        return
    add_todo(date, task)
    bot.send_message(message.chat.id, "Задача " + task_text + " добавлена на дату " + date)

@bot.message_handler(commands=["random"])
def random_add(message):
    date = 'сегодня'
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    bot.send_message(message.chat.id, "Задача " + task + " добавлена на дату " + date)

@bot.message_handler(commands=["show", "print"])
def show(message):
    # command = message.text.split(maxsplit = 1)
    dates = message.text.split()
    text = ''
    for date in dates:
        if date in ['\show', '\print']:
           continue
        date = date.lower()
    # date = command[1].lower()
        if date  in tasks:
            text += date.upper() + '\n'
            for task in tasks[date]:
                text += '[] ' + task + '\n'
    if len(text) < 1:
        text = 'Задач на дату нет!'

    bot.send_message(message.chat.id, text)

def check_task(task):
    if len(task) < 3:
        return False
    return True

bot.polling(none_stop=True)
