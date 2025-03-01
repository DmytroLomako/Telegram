from .settings import dispatcher, bot, id_admins, list_code, quiz_dict, result_dict, users_test_data, last_question
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from .models import *
from .read_json import read_json
import random, ast

@dispatcher.callback_query()
# оброблюємо натиск кнопки
async def handler_button(callback: CallbackQuery):
    press_user_id = callback.from_user.id
    # перевіряємо чи юзер адмін
    if press_user_id in id_admins:
        # перевіряємо що кнопка це вибір тесту
        if 'quiz-' in callback.data and 'end' not in callback.data:
            # створюємо назву квізу та код
            quiz_name = callback.data.split("quiz-")[-1]
            quiz_code = random.randint(1000, 9999)
            # перестворюємо код доки він не буде унікальним
            while quiz_code in list_code:
                quiz_code = random.randint(1000, 9999)
            # Start quiz
            list_code.append(str(quiz_code))
            await bot.edit_message_text(text = f"Quiz: {quiz_name}\nCode: {quiz_code}", message_id=callback.message.message_id, chat_id = press_user_id)
            # User list
            
            message = await bot.send_message(text = 'User list: \n', chat_id=press_user_id)
            # додаємо новий тест до словнику
            quiz_dict[str(quiz_code)] = {
                "users": [], 
                "id_message_users": message.message_id, 
                "chat_id_admin": press_user_id,
                "quiz_name":quiz_name, 
                "question_index": 0,
                "recruitment": True,
                "id_message_answer": None
            }
            result_dict[f"{quiz_name}_{quiz_code}"] = {}
        elif 'start-' in callback.data or "next_question" in callback.data:
            code = callback.data.split('-')[1]
            if code in quiz_dict:
                id_admin = quiz_dict[code]["chat_id_admin"]
                list_user = quiz_dict[code]['users']
                quiz_name = quiz_dict[code]["quiz_name"]
                quiz_dict[code]["recruitment"] = False
                list_question = read_json(quiz_name)["questions"]
                index = quiz_dict[code]['question_index']
                if "next_question" in callback.data:
                    index += 1
                list_question = read_json(quiz_name)["questions"]
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
                    await bot.delete_message(chat_id=id_admin, message_id=callback.message.message_id)
                    await bot.send_message(text = text_admin, chat_id = id_admin)
                    del quiz_dict[code]
                else:
                    question_text = list_question[index]["question"]
                    question_variants = list_question[index]["variants"]
                    correct_answer = list_question[index]["correct_answer"]
                    list_button = []
                    if len(correct_answer) == 1:
                        for variant in question_variants:
                            index_variant = question_variants.index(variant)
                            button = InlineKeyboardButton(text=variant, callback_data=f'variant|{code}|{index_variant}')
                            list_button.append([button])
                    else:
                        for variant in question_variants:
                            index_variant = question_variants.index(variant)
                            button = InlineKeyboardButton(text=variant, callback_data=f'multivariant|{index}|{quiz_name}|{code}|{index_variant}')
                            list_button.append([button])
                        button = InlineKeyboardButton(text='✅ Відповісти ✅', callback_data=f'variant|{code}|{index_variant}')
                        list_button.append([button])
                    keyboard = InlineKeyboardMarkup(inline_keyboard=list_button)  
                    list_user_name = ""
                    if len(list_question[index]["correct_answer"]) == 1:
                        if "next_question" in callback.data:
                            quiz_dict[code]['question_index'] += 1
                    for user in list_user:
                        name = user['name']
                        if user['answer'] != None or index == 0:
                            message = await bot.send_message(text=question_text,chat_id=user['id'], reply_markup=keyboard)
                            last_question[user["id"]] = message.message_id
                        else:
                            message_id = last_question[user["id"]]
                            prev_question = list_question[index - 1]["question"]
                            await bot.edit_message_text(text=f'{prev_question}\nВи не встигли відповісти', chat_id=user['id'], message_id=message_id)
                            message = await bot.send_message(text=question_text,chat_id=user['id'], reply_markup=keyboard)
                            last_question[user["id"]] = message.message_id
                        user['answer'] = None
                        list_user_name += f'\n • {name}'
                    button_next = InlineKeyboardButton(text='Next', callback_data=f'next_question-{code}')
                    button_end = InlineKeyboardButton(text='❌ End Quiz ❌', callback_data=f'end_quiz-{quiz_name}-{code}')
                    admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_next], [button_end]])
                    # \n - в строке помогает перенести содержимое на следующую строку
                    try:
                        message = await bot.edit_message_text(chat_id=id_admin, text=f"Users answered:\nDon't answered: {list_user_name}", message_id=callback.message.message_id, reply_markup=admin_keyboard)
                        quiz_dict[code]["id_message_answer"] = message.message_id
                    except Exception as error:
                        print(error)

    if 'end_quiz' in callback.data:
        quiz_name = callback.data.split('-')[-2]
        code = callback.data.split('-')[-1]
        text_admin = "The test is over.\n\nUser results:\n"
        count_answers = quiz_dict[code]["question_index"]
        sum_result = 0
        list_user = quiz_dict[code]['users']
        id_admin = quiz_dict[code]["chat_id_admin"]
        for user in list_user:
            user_id = user['id']
            await bot.delete_message(chat_id=user_id, message_id=last_question[user_id])
            if f"{quiz_name}_{code}" in result_dict and str(user_id) in result_dict[f"{quiz_name}_{code}"]:
                correct_count = result_dict[f"{quiz_name}_{code}"][str(user_id)]['result']
                user_name = result_dict[f"{quiz_name}_{code}"][str(user_id)]['name']
                text_admin += f' • {user_name} - {correct_count}/{count_answers}\n'
                sum_result += int(correct_count)
                text = f"The test is over, your results are {correct_count}/{count_answers} correct answers"
                await bot.send_message(text = text,chat_id= user_id)
        sum_result /= count_answers * len(list_user)
        sum_result *= 100
        text_admin += f'\n Global result - {int(sum_result)}%'
        await bot.delete_message(chat_id=id_admin, message_id=callback.message.message_id)
        await bot.send_message(text = text_admin, chat_id = id_admin)
        del quiz_dict[code]
        
    elif 'user-test-result' in callback.data:
        result_id = callback.data.split('-')[-1]
        session = Session()
        result = session.query(Result).filter_by(id=result_id).first()
        session.close()
        test = read_json(result.test_name)
        await bot.delete_message(chat_id=press_user_id, message_id=callback.message.message_id)
        if result:
            results = result.result
            results = '[' + results + ']'
            results = ast.literal_eval(results)
            results = [[int(x) if isinstance(x, str) else x for x in sublist] for sublist in results]
            print(results, 'vsufnhvhsufhfuihsiuhfiusfhiuhfiushiufh')
            user_result = f'Результат тесту {result.test_name}:\n'
            count_result = 0
            count = 0
            for question in test['questions']:
                index_question = test['questions'].index(question) + 1
                question_text = question["question"]
                all_variants = question['variants']
                user_result += f'\n{index_question}. {question_text}\n'
                user_answer_index = results[count]
                correct_answer = question['correct_answer']
                if len(user_answer_index) == 1:
                    answer = all_variants[int(user_answer_index[0])]
                else:
                    answer = ''
                    for index in user_answer_index:
                        answer += f'{all_variants[int(index)]} '
                if str(user_answer_index) == str(correct_answer):
                    count_result += 1
                list_buttons = [[]]
                for variant in all_variants:
                    if len(user_answer_index) == 1:
                        if variant == answer:
                            button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data='hello')
                        else:
                            button = InlineKeyboardButton(text=variant, callback_data='hello')
                    else:
                        if variant in answer:
                            button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data='hello')
                        else:
                            button = InlineKeyboardButton(text=variant, callback_data='hello')
                    list_buttons.append([button])
                keyboard = InlineKeyboardMarkup(inline_keyboard=list_buttons)
                await bot.send_message(text=question_text, reply_markup=keyboard, chat_id=press_user_id)
                count += 1
        else:
            await bot.edit_message_text(text='Результат не знайдено', chat_id=press_user_id, message_id=callback.message.message_id)
            
    elif 'user-multianswer' in callback.data:
        index = int(callback.data.split('-')[-2])
        question_index = int(callback.data.split('-')[-3])
        # test = read_json(callback.data.split('-')[-1])
        chosen = callback.data.split('-')[-4]
        name = callback.data.split('-')[-1]
        test = read_json(name)
        question = test['questions'][question_index]
        correct_answer = question
        answers = []
        if chosen == 'True':
            answers = users_test_data[press_user_id]["answers"][-1]
        list_buttons = [[]]
        for variant in question['variants']:
            index_variant = question['variants'].index(variant)
            if variant == question["variants"][index]:
                if question['variants'].index(variant) in answers:
                    button = InlineKeyboardButton(text=f'{variant}', callback_data=f'user-multianswer-{True}-{question_index}-{index_variant}-{name}')
                    users_test_data[press_user_id]["answers"][-1].remove(question['variants'].index(variant))
                else:
                    button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data=f'user-multianswer-{True}-{question_index}-{index_variant}-{name}')
                    if chosen == 'True':
                        users_test_data[press_user_id]["answers"][-1].append(index)
                    else:
                        users_test_data[press_user_id]["answers"].append([index])
            else:
                if question['variants'].index(variant) in answers:
                    button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data=f'user-multianswer-{True}-{question_index}-{index_variant}-{name}')
                else:
                    button = InlineKeyboardButton(text=variant, callback_data=f'user-multianswer-{True}-{question_index}-{index_variant}-{name}')
            list_buttons.append([button])
        button = InlineKeyboardButton(text='✅ Відповісти ✅', callback_data=f'user-answer-{chosen}--{index_variant}-{name}')
        list_buttons.append([button])
        button = InlineKeyboardButton(text='❌ Зупинити тест ❌', callback_data=f'user-end-test-{index}-{name}')
        list_buttons.append([button])
        keyboard = InlineKeyboardMarkup(inline_keyboard=list_buttons)
        await bot.edit_message_reply_markup(chat_id=press_user_id, message_id=callback.message.message_id, reply_markup=keyboard)
    
    elif 'user-test' in callback.data or 'user-answer' in callback.data:
        if 'user-test' in callback.data and callback.from_user.id in users_test_data:
            await bot.edit_message_text(text='Тест вже запущено', chat_id=press_user_id, message_id=callback.message.message_id)
        else:
            name = callback.data.split('-')[-1]
            test = read_json(name)
            try:
                multi = callback.data.split('-')[-4]
            except:
                multi = False
            if len(test['questions']) > 0:
                index_question = 0
                if press_user_id in users_test_data:
                    users_test_data[press_user_id]['question_index'] += 1
                    index_question = users_test_data[press_user_id]['question_index']
                    if multi != 'True':
                        users_test_data[press_user_id]['answers'].append([callback.data.split('-')[-2]])
                else:
                    users_test_data[press_user_id] = {
                        'test_name': name,
                        'question_index': 0,
                        'answers': []
                    }
                question_count = len(test['questions'])
                if index_question >= question_count:
                    user_result = 'Тест завершено\nВаші результати:\n'
                    await bot.edit_message_text(text=user_result, chat_id=press_user_id, message_id=callback.message.message_id)
                    user_result = ''
                    result = 0
                    list_answers = ''
                    for question in test['questions']:
                        index_question = test['questions'].index(question) + 1
                        question_text = question["question"]
                        user_result += f'\n{index_question}. {question_text}\n'
                        user_answer_index = users_test_data[press_user_id]['answers'][index_question - 1]
                        correct_answer = question['correct_answer']
                        if len(user_answer_index) == 1:
                            answer = question['variants'][int(user_answer_index[0])]
                            list_answers += f'{[user_answer_index[0]]},'
                            if str(user_answer_index[0]) == str(correct_answer[0]):
                                result += 1
                        else:
                            answer = []
                            list_answers += f'{user_answer_index},'
                            for index in user_answer_index:
                                answer.append(question['variants'][int(index)])
                            if correct_answer == user_answer_index:
                                result += 1
                        list_buttons = [[]]
                        for variant in question['variants']:
                            if type(answer) == int:
                                if variant == answer:
                                    button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data='hello')
                                else:
                                    button = InlineKeyboardButton(text=variant, callback_data='hello')
                            else:
                                if variant in answer:
                                    button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data='hello')
                                else:
                                    button = InlineKeyboardButton(text=variant, callback_data='hello')
                            list_buttons.append([button])
                        keyboard = InlineKeyboardMarkup(inline_keyboard=list_buttons)
                        await bot.send_message(text=question_text, reply_markup=keyboard, chat_id=press_user_id)
                    list_answers = list_answers[:-1]
                    result = round(result / question_count * 100, 1)
                    user_result = f'\nВаш результат: {result}%'
                    await bot.send_message(text=user_result, chat_id=press_user_id)
                    session = Session()
                    user = session.query(User).filter_by(telegram_id=press_user_id).first()
                    if user:
                        result = Result(
                            user_id = user.id,
                            test_name = name,
                            result = list_answers
                        )
                        session.add(result)
                        session.commit()
                        session.close()
                        await bot.send_message(text='Ваш результат успішно збережено\nВи можете подивидить за командою /results', chat_id=press_user_id)
                    del users_test_data[press_user_id]
                else:
                    question = test['questions'][index_question]
                    question_text = question["question"]
                    question_variants = question["variants"]
                    correct_answer = question['correct_answer']
                    if len(correct_answer) > 1:
                        question_text += '\nОберіть усі правильні відповіді'
                    list_button = []
                    chosen = False
                    for variant in question_variants:
                        index = question_variants.index(variant)
                        if len(correct_answer) > 1:
                            button = InlineKeyboardButton(text=variant, callback_data=f'user-multianswer-{chosen}-{index_question}-{index}-{name}')
                        else:
                            button = InlineKeyboardButton(text=variant, callback_data=f'user-answer-{index}-{name}')
                        list_button.append([button])
                    if len(correct_answer) > 1:
                        button = InlineKeyboardButton(text='✅ Відповісти ✅', callback_data=f'user-answer-{index}-{name}')
                        list_button.append([button])
                    button = InlineKeyboardButton(text='❌ Зупинити тест ❌', callback_data=f'user-end-test-{index}-{name}')
                    list_button.append([button])
                    keyboard = InlineKeyboardMarkup(inline_keyboard=list_button)  
                    try:
                        await bot.edit_message_text(text=question_text,chat_id=press_user_id, message_id=callback.message.message_id, reply_markup=keyboard)
                    except Exception as error:
                        print(error)
            
            
    elif 'user-end-test' in callback.data:
        name = callback.data.split('-')[-1]
        test = read_json(name)
        question_count = len(test['questions'])
        user_result = 'Тест завершено\nВаші результати:\n'
        await bot.edit_message_text(text=user_result, chat_id=press_user_id, message_id=callback.message.message_id)
        user_result = ''
        result = 0
        count_answers = len(users_test_data[press_user_id]['answers'])
        for question in test['questions']:
            index_question = test['questions'].index(question) + 1
            if index_question > count_answers:
                break
            question_text = question["question"]
            user_result += f'\n{index_question}. {question_text}\n'
            user_answer_index = users_test_data[press_user_id]['answers'][index_question - 1]
            correct_answer = question['correct_answer']
            if len(user_answer_index) == 1:
                answer = question['variants'][int(user_answer_index[0])]
                if str(user_answer_index[0]) == str(correct_answer[0]):
                    result += 1
            else:
                answer = []
                for index in user_answer_index:
                    answer.append(question['variants'][int(index)])
                if correct_answer == user_answer_index:
                    result += 1
            list_buttons = [[]]
            for variant in question['variants']:
                if type(answer) == int:
                    if variant == answer:
                        button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data='hello')
                    else:
                        button = InlineKeyboardButton(text=variant, callback_data='hello')
                else:
                    if variant in answer:
                        button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data='hello')
                    else:
                        button = InlineKeyboardButton(text=variant, callback_data='hello')
                list_buttons.append([button])
            keyboard = InlineKeyboardMarkup(inline_keyboard=list_buttons)
            await bot.send_message(text=question_text, reply_markup=keyboard, chat_id=press_user_id)
        result = round(result / count_answers * 100, 1)
        user_result = f'\nВаш результат: {result}%'
        await bot.send_message(text=user_result, chat_id=press_user_id)
        del users_test_data[press_user_id]
            
    elif 'multivariant' in callback.data:
        code = callback.data.split('|')[-2]
        name = callback.data.split('|')[-3]
        index = int(callback.data.split('|')[-4])
        if code in quiz_dict:
            list_question = read_json(name)['questions']
            index_v = int(callback.data.split('|')[-1])
            question_text = list_question[index]["question"]
            question_variants = list_question[index]["variants"]
            correct_answer = list_question[index]["correct_answer"]
            list_button = []
            for user in quiz_dict[code]["users"]:
                if user["id"] == press_user_id:
                    if user['answer'] == None:
                        user['answer'] = [index_v]
                    else:
                        if index_v not in user['answer']:
                            user['answer'].append(index_v)
                        else:
                            user['answer'].remove(index_v)
                    user_answer = user['answer']   
            for variant in question_variants:
                index_variant = question_variants.index(variant)
                if int(index_v) == question_variants.index(variant):
                    if question_variants.index(variant) in user_answer:
                        button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data=f'multivariant|{index}|{name}|{code}|{index_variant}')
                else:
                    if question_variants.index(variant) in user_answer:
                        button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data=f'multivariant|{index}|{name}|{code}|{index_variant}')
                    else:
                        button = InlineKeyboardButton(text=f'{variant}', callback_data=f'multivariant|{index}|{name}|{code}|{index_variant}')
                list_button.append([button])
            button = InlineKeyboardButton(text='✅ Відповісти ✅', callback_data=f'variant|{True}|{code}|{user_answer}')
            list_button.append([button])
            keyboard = InlineKeyboardMarkup(inline_keyboard=list_button)
            await bot.edit_message_reply_markup(chat_id=press_user_id, message_id=callback.message.message_id, reply_markup=keyboard)
    
    elif 'variant|' in callback.data:
        code = callback.data.split('|')[-2]
        multi = callback.data.split('|')[-3]
        if code in quiz_dict:
            # Index variant
            index = callback.data.split('|')[-1]
            question_index = quiz_dict[code]["question_index"]
            quiz_name = quiz_dict[code]["quiz_name"]
            question = read_json(quiz_name)['questions']
            que_text = question[question_index]['question']
            que_answer = ''
            if len(index) == 1:
                que_answer = question[question_index]['variants'][int(index[0])]
            else:
                que_answer = ''
                for i in ast.literal_eval(index):
                    que_answer += (question[question_index]['variants'][int(i)])
                    que_answer += ', '
                que_answer = que_answer[:-2]
            correct_answer = question[question_index]['correct_answer']
            
            await bot.edit_message_text(text=f"{que_text}\nYour answer: {que_answer}", message_id=callback.message.message_id, chat_id=press_user_id)

            list_user_answered = ""
            list_user_not_answered = ""
            for user in quiz_dict[code]["users"]:
                name = user['name']
                if user["id"] == press_user_id and user["answer"] != None:
                    if user["answer"] == correct_answer:
                        result_dict[f'{quiz_name}_{code}'][str(press_user_id)]['result'] += 1   
                if user["id"] == press_user_id and user["answer"] == None:
                    user["answer"] = index
                    if index == str(correct_answer[0]):
                        result_dict[f'{quiz_name}_{code}'][str(press_user_id)]['result'] += 1
                if user["answer"] != None:
                    list_user_answered += f'\n • {name}'
                else:
                    list_user_not_answered += f'\n • {name}'
                    
            button_next = InlineKeyboardButton(text='Next', callback_data=f'next_question-{code}')
            button_end = InlineKeyboardButton(text='❌ End Quiz ❌', callback_data=f'end_quiz-{quiz_name}-{code}')
            admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_next], [button_end]])
            text = f"Users answered: {list_user_answered}\nDon't answered: {list_user_not_answered}"
            await bot.edit_message_text(text= text, chat_id= quiz_dict[code]["chat_id_admin"], message_id= quiz_dict[code]["id_message_answer"], reply_markup=admin_keyboard)