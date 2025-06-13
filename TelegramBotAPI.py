import telebot
from telebot import types

from Sqlite import Database

# Токен для бота от BotFather
TOKEN = '7706937394:AAEO4HWY8RubKHlnQbJRL51zVhThg89Du0o'

# Инициализация бота
bot = telebot.TeleBot('7706937394:AAEO4HWY8RubKHlnQbJRL51zVhThg89Du0o')

db = Database() # Создали экземпляр базы данных

# # Хранение пользовательских данных
# user_data = {}  # {chat_id: {'state': '...', 'login': '...', 'password': '...'}}

# --- Функции создания клавиатур ---

def get_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_login = types.KeyboardButton("🔐 Войти в ЛМС")
    btn_faq = types.KeyboardButton("❓ FAQ")
    btn_commands = types.KeyboardButton("📋 Список команд")
    markup.add(btn_login, btn_faq, btn_commands)
    return markup

def get_logged_in_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_logout = types.KeyboardButton("🚪 Выйти из аккаунта")
    btn_deadlines = types.KeyboardButton("📅 Посмотреть дедлайны")
    btn_faq = types.KeyboardButton("❓ FAQ")
    btn_commands = types.KeyboardButton("📋 Список команд")
    markup.add(btn_logout, btn_deadlines, btn_faq, btn_commands)
    return markup

# переделать под вывод заданий по неделям
# def get_reminder_menu():
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     btn_3_days = types.KeyboardButton("📅 За 3 дня")
#     btn_1_day = types.KeyboardButton("📅 За 1 день")
#     btn_1_hour = types.KeyboardButton("⏰ За 1 час")
#     btn_back = types.KeyboardButton("↩️ Назад")
#     markup.add(btn_3_days, btn_1_day, btn_1_hour, btn_back)
#     return markup

# --- Команды и обработка нажатий ---

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    db.AddUserData(chat_id,status='logged_out') # Добавили пользователя в БД
    #user_data[chat_id] = {'state': 'logged_out'}
    bot.send_message(chat_id, "Привет! 👋\n\nЭтот бот поможет тебе следить за дедлайнами и управлять учётной записью ЛМС.\nНажмите на нужную кнопку ниже.", reply_markup=get_main_menu())

# --- Обработка всех сообщений ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()

    user_data = db.GetUserStatus(chat_id) # Пытаемся получить статус пользователя
    if user_data == None: # Если пользователь не был создан метод возвращает None
        db.AddUserData(chat_id,status='logged_out') # Добавляем пользователя
        current_state = db.GetUserStatus(chat_id) # Получаем его статус
    else:
        current_state = db.GetUserStatus(chat_id) # Если же пользовател был, то сразу же получаем статус

    # --- Главное меню обработка состояний (пользователь не вошёл) ---
    if current_state == 'logged_out':
        if text == "🔐 Войти в ЛМС":
            db.AddUserData(chat_id,status = 'awaiting_login')
            bot.send_message(chat_id, "Введите ваш логин:")

        elif text == "❓ FAQ":
            bot.send_message(chat_id, "Здесь будет текст с часто задаваевыми вопросами и ответами.")

        elif text == "📋 Список команд":
            show_commands(chat_id)

        else:
            bot.send_message(chat_id, "Не понял вас. Вот доступные команды:", reply_markup=get_main_menu())

    # --- Авторизация: ввод логина ---
    elif db.GetUserStatus(chat_id) == 'awaiting_login':
        db.add_user(chat_id, status='awaiting_password', login=text)
        bot.send_message(chat_id, "Введите ваш пароль:")

    # --- Авторизация: ввод пароля ---
    elif db.GetUserStatus(chat_id) == 'awaiting_password':
        db.add_user(chat_id, status='awaiting_password', password = text) # Записываем полученный пароль в БД
        
        try:
            x = ParserLMS(session,chat_id); 
            arr = x.Parsing(); # Первая стадия парсинга - получения массива html кодов за каждый день 
            task_days = x.IsExistTask(arr) # Вторая часть парсинга - Определение типа дня

            dayWithFullTask = x.ParseDateAboutAllDay(task_days) # Третья часть парсинга - парсинг и на выходе получение массива объектов Day
            
            # Только в случае успеха, т.е. если нет ошибки в парсинге
            bot.send_message(chat_id, f"✅ Вы успешно вошли в аккаунт *{login}*", parse_mode='Markdown')

            db.add_user(chat_id, status='logged_in')
            bot.send_message(chat_id, "Выберите действие:", reply_markup=get_logged_in_menu())


        except:
            bot.send_message(chat_id, "Введены недействительные данные логина и пароля. Пожалуйста повторно введите данные, используя соответсвующую функцию")
            db.add_user(chat_id, status='logged_out', login = None,password = None)



        
        

    # --- Меню после авторизации ---
    elif db.GetUserStatus(chat_id) == 'logged_in':
        if text == "📅 Посмотреть дедлайны":
            #Заменить на реальную реализацию
            bot.send_message(chat_id, "📌 Ближайшие дедлайны:\n1. Домашнее задание по математике — 05.04.2025\n2. Эссе по литературе — 08.04.2025")


        elif text == "🚪 Выйти из аккаунта":
            db.add_user(chat_id, status='logged_out', login=None, password=None) # Затираем данные логина и пароля (при этом не удаляем самого пользователя из бд)
            bot.send_message(chat_id, "🚪 Вы вышли из аккаунта.", reply_markup=get_main_menu())

        elif text == "❓ FAQ":
            bot.send_message(chat_id, "Здесь будет текст с частыми вопросами и ответами.")

        elif text == "📋 Список команд":
            show_commands(chat_id)

        else:
            bot.send_message(chat_id, "Неизвестная команда. Показываю список доступных команд:", reply_markup=get_logged_in_menu())


    # --- Резервный случай ---
    else:
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте начать заново с /start")


# --- Функция показа списка команд ---
def show_commands(chat_id):
    bot.send_message(chat_id, """
📄 Список доступных команд:
- 🔐 Войти в ЛМС — войти в систему обучения
- 📅 Посмотреть дедлайны — получить информацию о ближайших задачах
- 🚪 Выйти из аккаунта — завершить сессию
- ❓ FAQ — получить полезную информацию
- 📋 Список команд — вызвать это меню
    """)

# --- Запуск бота ---
print("Бот запущен..")
bot.polling(none_stop=True)