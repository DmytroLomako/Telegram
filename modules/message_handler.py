from .settings import user_status, id_admins, dispatcher, bot, list_code, quiz_dict, result_dict
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@dispatcher.message()
# Оброблюємо усі повідомлення
async def handler_message(message:Message):
    id = message.from_user.id 
    # Перевіряє чи є статус
    if id in user_status:
        # Якщо користувач вводить код
        if user_status[id] == "enter-code":
            # Перевіряємо правильність
            if message.text in list_code:
                await message.answer("Enter name") 
                user_status[id] = f"enter-name-{message.text}"
            else:
                await message.answer("This code invalid, try again")
        # Якщо користувач вводить ім'я
        elif 'enter-name' in user_status[id]:
            # split - помогает разделить строку на список по символу
            code = user_status[id].split('-')[2]
            # Створили словник користувача і додали його в квіз
            dict = {
                "name": message.text, 
                "id": message.from_user.id,
                "answer": None
            }
            quiz_dict[code]["users"].append(dict)
            # Онулюємо статус користувача
            user_status[id] = ''
            await message.answer("Waiting...")
            # Текст списку користувачів
            text = "User list:\n"
            for user in quiz_dict[code]["users"]:
                name = user["name"]
                text += f" • {name}\n"

            button_start = InlineKeyboardButton(text='Start quiz', callback_data=f'start-{code}')
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_start]])
            await bot.edit_message_text(chat_id = quiz_dict[code]["chat_id_admin"], message_id = quiz_dict[code]["id_message_users"], text=text, reply_markup=keyboard)
            name_quiz = quiz_dict[code]["quiz_name"]
            result_dict[f"{name_quiz}_{code}"][str(id)] = {
                'name': message.text,
                'result': 0
            } 
    