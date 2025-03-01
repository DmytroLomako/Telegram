from .settings import dispatcher,id_admins,bot, user_status, users_test_data
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import os
# оброблюємо команду старт
@dispatcher.message(CommandStart())
async def start(message: Message):
    # перевіряємо чи адмін користувач
    if message.from_user.id in id_admins:
        await message.answer('Hello admin👋, you can execute this commands:\n\n/start - Greetings, starting the bot\n/create - Creating a quiz \n/delete - Delete quiz\n/start_quiz - Start public quiz\n/quiz - Start private quiz\n/result - Shows all results')
    else:
        await message.answer('Hello user👋, to join to test enter /join')
        
def read_all_tests(test_type: str) -> InlineKeyboardMarkup:
    static_path = os.path.abspath(__file__ + '/../../static')
    list_names = []
    # Убираем из именни файла .json
    # os.listdir(path) - Получает список всех файлов\папок по указаному пути
    for name in os.listdir(static_path):
        new_name = name.split('.json')[0]
        list_names.append(new_name)
    # Создаём кнопки и делим их на ряды
    list_buttons = [[]]
    for name in list_names:
        button = InlineKeyboardButton(text=name, callback_data=f'{test_type}-{name}')
        if len(list_buttons[-1]) < 2:
            list_buttons[-1].append(button)
        else:
            list_buttons.append([button])
    return InlineKeyboardMarkup(inline_keyboard=list_buttons)

# /start_quiz
@dispatcher.message(Command(commands = ['start_quiz']))
async def start_quiz(message: Message):
    if message.from_user.id in id_admins:
        keyboard = read_all_tests('quiz')
        await message.answer('Select quiz:', reply_markup=keyboard)

# оброблюємо команду join
@dispatcher.message(Command(commands=['join']))
async def join(message: Message):
    await message.answer('Please, enter the code.')
    # очікуємо введеня коду від користувача
    user_status[message.from_user.id] = 'enter-code'
    
@dispatcher.message(Command(commands=['quiz']))
async def user_quiz(message: Message):
    keyboard = read_all_tests('user-test')
    if message.from_user.id in users_test_data:
        await message.answer('Завершіть будь ласка тест, перед тим як починати новий')
    else:
        await message.answer('Оберіть тест для проходження:', reply_markup=keyboard)