import telebot, base as db, button as bt
from geopy import Nominatim


bot = telebot.TeleBot('6352907821:AAFKG1xCUGmVZqGJwxvO0nnv9cBmR8NoKwE')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36')

@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id

    user_id = message.from_user.id
    check_user = db.checker(user_id)

    if check_user:
        products = db.get_pr_name_id()
        bot.send_message(user_id, 'Добро пожаловать!', reply_markup=bt.remove())
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=bt.main_menu_buttons(products))
    else:
        bot.send_message(user_id, 'Приветствую вас! Начнем регистрацию, напишите свое имя', reply_markup=bt.remove())
        bot.register_next_step_handler(message, get_name)


def get_name(message):

    user_name = message.text
    bot.send_message(user_id, 'Отлично! А теперь отправьте номер!', reply_markup=bt.num_button())
    bot.register_next_step_handler(message, get_num, user_name)

def get_num(message, user_name):

    if message.contact:
        user_num = message.contact.phone_number
        bot.send_message(user_id, 'А теперь отправьте локацию!', reply_markup=bt.loc_button())

        bot.register_next_step_handler(message, get_loc, user_name, user_num)

    else:
        bot.send_message(user_id, 'Отправьте свой контакт через кнопку!')
        bot.register_next_step_handler(message, get_num, user_name)

def get_loc(message, user_name, user_num):

    if message.location:

        user_loc = geolocator.reverse(f'{message.location.longitude},' f'{message.location.latitude}')
        db.register(user_id, user_name, user_num, user_loc)

        bot.send_message(user_id, 'Вы успешно зарегистрировались!')
        products = db.get_pr_name_id()
        bot.send_message(user_id, 'Выберите пункт меню', reply_markup=bt.main_menu_buttons(products))

    else:

        bot.send_message(user_id, 'Отправьте локацию через кнопку!')
        bot.register_next_step_handler(message, get_loc, user_name, user_num)


bot.polling(non_stop=True)






























