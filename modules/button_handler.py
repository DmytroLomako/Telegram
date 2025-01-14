from .settings import dispatcher, bot, id_admins, list_code, quiz_dict, result_dict
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from .read_json import read_json
import random

@dispatcher.callback_query()
# оброблюємо натиск кнопки
async def handler_button(callback: CallbackQuery):
    # перевіряємо чи юзер адмін
    if callback.from_user.id in id_admins:
        # перевіряємо що кнопка це вибір тесту
        if 'quiz-' in callback.data:
            # створюємо назву квізу та код
            quiz_name = callback.data.split("quiz-")[-1]
            quiz_code = random.randint(1000, 9999)
            # перестворюємо код доки він не буде унікальним
            while quiz_code in list_code:
                quiz_code = random.randint(1000, 9999)
            # Start quiz
            list_code.append(str(quiz_code))
            await bot.send_message(text = f"Quiz: {quiz_name}\nCode: {quiz_code}", chat_id = callback.from_user.id)
            # User list
            
            message = await bot.send_message(text = 'User list: \n', chat_id=callback.from_user.id)
            # додаємо новий тест до словнику
            quiz_dict[str(quiz_code)] = {
                "users": [], 
                "id_message_users": message.message_id, 
                "chat_id_admin": callback.from_user.id,
                "quiz_name":quiz_name, 
                "question_index": 0,
                "id_message_answer": None
            }
            result_dict[f"{quiz_name}_{quiz_code}"] = {}
        elif 'start-' in callback.data or "next_question" in callback.data:
            code = callback.data.split('-')[1]
            if code in quiz_dict:
                id_admin = quiz_dict[code]["chat_id_admin"]
                list_user = quiz_dict[code]['users']
                quiz_name = quiz_dict[code]["quiz_name"]
                list_question = read_json(quiz_name)["questions"]
                # 
                if "next_question" in callback.data:
                    quiz_dict[code]['question_index'] += 1
                index = quiz_dict[code]['question_index']
                if index >= len(list_question):
                    text_admin = "The test is over.\n\nUser results:\n"
                    sum_result = 0
                    question_count = len(list_question)
                    for user in list_user:
                        user_id = user['id']
                        if f"{quiz_name}_{code}" in result_dict and str(user_id) in result_dict[f"{quiz_name}_{code}"]:
                            correct_count = result_dict[f"{quiz_name}_{code}"][str(user_id)]['result']
                            user_name = result_dict[f"{quiz_name}_{code}"][str(user_id)]['name']
                            text_admin += f' • {user_name} - {correct_count}/{question_count}\n'
                            sum_result += int(correct_count)
                            text = f"The test is over, your results are {correct_count}/{question_count} correct answers"
                            await bot.send_message(text = text,chat_id= user_id)
                    sum_result /= question_count * len(list_user)
                    sum_result *= 100
                    text_admin += f'\n Global result - {int(sum_result)}%'
                    await bot.send_message(text = text_admin, chat_id = id_admin)
                else:
                    question_text = list_question[index]["question"]
                    question_variants = list_question[index]["variants"]
                    # 
                    list_button = []
                    for variant in question_variants:
                        index = question_variants.index(variant)
                        button = InlineKeyboardButton(text=variant, callback_data=f'variant|{code}|{index}')
                        list_button.append([button])
                    keyboard = InlineKeyboardMarkup(inline_keyboard=list_button)  
                    list_user_name = ""
                    for user in list_user:
                        name = user['name']
                        user['answer'] = None
                        list_user_name += f'\n • {name}'
                        await bot.send_message(text=question_text,chat_id=user['id'], reply_markup=keyboard)
                    button_next = InlineKeyboardButton(text='Next', callback_data=f'next_question-{code}')
                    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_next]])
                    # \n - в строке помогает перенести содержимое на следующую строку
                    message = await bot.send_message(chat_id=id_admin, text=f"Users answered:\nDon't answered: {list_user_name}", reply_markup=admin_keyboard)
                    quiz_dict[code]["id_message_answer"] = message.message_id
    
    if 'variant|' in callback.data:
        code = callback.data.split('|')[1]
        if code in quiz_dict:
            # Index variant
            index = callback.data.split('|')[2]

            question_index = quiz_dict[code]["question_index"]
            quiz_name = quiz_dict[code]["quiz_name"]
            question = read_json(quiz_name)['questions']
            que_text = question[question_index]['question']
            que_answer = question[question_index]['variants'][int(index)]
            correct_answer = question[question_index]['correct_answer']
            
            await bot.edit_message_text(text=f"{que_text}\nYour answer: {que_answer}", message_id=callback.message.message_id, chat_id=callback.from_user.id)

            list_user_answered = ""
            list_user_not_answered = ""
            for user in quiz_dict[code]["users"]:
                name = user['name']
                if user["id"] == callback.from_user.id and user["answer"] == None:
                    user["answer"] = index
                    if index == str(correct_answer):
                        result_dict[f'{quiz_name}_{code}'][str(callback.from_user.id)]['result'] += 1
                if user["answer"] != None:
                    list_user_answered += f'\n • {name}'
                else:
                    list_user_not_answered += f'\n • {name}'
                    
            button_next = InlineKeyboardButton(text='Next', callback_data=f'next_question-{code}')
            admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_next]])
            text = f"Users answered: {list_user_answered}\nDon't answered: {list_user_not_answered}"
            await bot.edit_message_text(text= text, chat_id= quiz_dict[code]["chat_id_admin"], message_id= quiz_dict[code]["id_message_answer"], reply_markup=admin_keyboard)