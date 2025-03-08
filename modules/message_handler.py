from .settings import *
from .settings_db import *
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from .models import User, Teacher
from .read_static import read_json, get_image
from .user_result import save_result
import aiogram.types

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
                if quiz_dict[message.text]["recruitment"]:
                    if quiz_dict[message.text]["users"] and str(id) in str(quiz_dict[message.text]["users"][0]["id"]):
                        await message.answer("Ви вже в тесті")
                    else:
                        await message.answer("Enter name") 
                        user_status[id] = f"enter-name-{message.text}"
                else:
                    await message.answer("Цей тест вже запущений")
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
            del user_status[id]
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
        
        elif 'enter-auth-name' in user_status[id]:
            await message.answer("Введіть ваш пароль")
            name = message.text
            user_status[id] = f"enter-auth-password-{name}"
        
        elif 'enter-auth-password' in user_status[id]:
            name = user_status[id].split('-')[-1]
            password = message.text
            session = Session()
            del user_status[id]
            for user_type in [User, Teacher]:
                user = session.query(user_type).filter_by(username=name, password=password).first()
                if user:
                    user.telegram_id = id
                    session.commit()
                    session.close()
                    await message.answer("Ви успішно авторизовані")
                    if user_type == Teacher:
                        id_admins.append(id)
                    return user
            session.close()
            await message.answer("Невірний логін або пароль")
                
        elif 'quiz-input' in user_status[id]:
            test_name = user_status[id].split('-')[-1]
            question_index = int(user_status[id].split('-')[-2])
            code = user_status[id].split('-')[-3]
            list_users = quiz_dict[code]['users']
            test = read_json(test_name)
            question = test['questions'][question_index]
            correct_answer = question['correct_answer'][0]
            user_answer = message.text
            list_user_answered = ""
            list_user_not_answered = ""
            await message.answer("Вашу відповідь зараховано")
            if user_answer == correct_answer:
                result_dict[f"{test_name}_{code}"][str(id)]['result'] += 1
            for user in list_users:
                name = user['name']
                if user['id'] == id:
                    user['answer'] = message.text
                    del user_status[id]
                if user["answer"] != None:
                    list_user_answered += f'\n • {name}'
                else:
                    list_user_not_answered += f'\n • {name}'
            id_admin = quiz_dict[code]["chat_id_admin"]
            button_next = InlineKeyboardButton(text='Next', callback_data=f'next_question-{code}')
            button_end = InlineKeyboardButton(text='❌ End Quiz ❌', callback_data=f'end_quiz-{test_name}-{code}')
            admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_next], [button_end]])
            try:
                message_answer = quiz_dict[code]['id_message_answer']
                message = await bot.edit_message_text(chat_id=id_admin, text=f"Users answered: {list_user_answered}\nDon't answered: {list_user_not_answered}", message_id=message_answer, reply_markup=admin_keyboard)
                quiz_dict[code]["id_message_answer"] = message.message_id
            except Exception as error:
                print(error)
                
        elif 'user-input' in user_status[id]:
            test_name = user_status[id].split('-')[-1]
            question_index = int(user_status[id].split('-')[-2])
            user_answer = message.text
            test = read_json(test_name)
            question_count = len(test['questions'])
            users_test_data[id]['question_index'] += 1
            users_test_data[id]['answers'].append(user_answer)
            if question_index + 1 >= question_count:
                await save_result(id, test_name)
            else:
                
                question_index = users_test_data[id]['question_index']
                question = test['questions'][question_index]
                
                
                question_text = question["question"]
                question_image = question["image"]
                prev_question_image = test['questions'][question_index - 1]["image"]
                question_type = question["type"]
                question_variants = question["variants"]
                correct_answer = question['correct_answer']
                
                if len(correct_answer) > 1:
                    question_text += '\nОберіть усі правильні відповіді'
                if question_type == 'input':
                    user_status[id] = f'user-input-{question_index}-{test_name}'
                    text = f'{question_text}\nВведіть відповідь'
                    if question_image:
                        await bot.send_photo(photo=get_image(question_image), caption=question_text, chat_id=id)
                    else:
                        await message.answer(text=text)
                else:
                    list_button = [[]]
                    chosen = False
                    for variant in question_variants:
                        index = question_variants.index(variant)
                        if len(correct_answer) > 1:
                            button = InlineKeyboardButton(text=f'{index + 1}. {variant}', callback_data=f'user-multianswer-{chosen}-{question_index}-{index}-{test_name}')
                        else:
                            button = InlineKeyboardButton(text=f'{index+ 1}. {variant}', callback_data=f'user-answer-{index}-{test_name}')
                        # if len(list_button[-1]) < 2:
                        #     list_button[-1].append(button)
                        # else:
                        list_button.append([button])
                    if len(correct_answer) > 1:
                        button = InlineKeyboardButton(text='✅ Відповісти ✅', callback_data=f'user-answer-{index}-{test_name}')
                        list_button.append([button])
                    button = InlineKeyboardButton(text='❌ Зупинити тест ❌', callback_data=f'user-end-test-{index}-{test_name}')
                    list_button.append([button])
                    keyboard = InlineKeyboardMarkup(inline_keyboard=list_button)  
                    try:
                        if question_image:
                            await bot.send_photo(photo=get_image(question_image), caption=question_text, chat_id=id, reply_markup=keyboard) 
                        else:
                            await message.answer(text=question_text, reply_markup=keyboard)
                    except Exception as error:
                        print(error)