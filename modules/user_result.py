from .models import *
from .settings import *
from .read_json import read_json


async def save_result(press_user_id, name, message_id = None):
    test = read_json(name)
    question_count = len(test['questions'])
    user_result = 'Тест завершено\n'
    if message_id == None:
        await bot.send_message(text=user_result, chat_id=press_user_id)
    else:
        await bot.edit_message_text(text=user_result, chat_id=press_user_id, message_id=message_id)
    user_result = ''
    result = 0
    right = 0
    wrong = 0
    list_answers = ''
    for question in test['questions']:
        index_question = test['questions'].index(question) + 1
        question_text = question["question"]
        question_type = question["type"]
        user_result += f'\n{index_question}. {question_text}\n'
        correct_answer = question['correct_answer']
        if question_type == 'input':
            user_answer_index = users_test_data[press_user_id]['answers'][index_question - 1]
            answer = user_answer_index
            list_answers += f'{[answer]},'
            if answer == str(correct_answer[0]):
                result += 1
                right += 1
            else:
                wrong += 1
        else:
            user_answer_index = users_test_data[press_user_id]['answers'][index_question - 1]
            if len(user_answer_index) == 1:
                answer = question['variants'][int(user_answer_index[0])]
                # list_answers += f'{[user_answer_index[0]]},'
                list_answers += f'{[answer]},'
                if answer == str(correct_answer[0]):
                    result += 1
                    right += 1
                else:
                    wrong += 1
            else:
                answer = []
                # list_answers += f'{user_answer_index},'
                for index in user_answer_index:
                    answer.append(question['variants'][int(index)])
                list_answers += f'{answer},'
                if set(correct_answer) == set(answer):
                    result += 1
                    right += 1
                else:
                    wrong += 1
            # list_buttons = [[]]
            # for variant in question['variants']:
            #     if type(answer) == int:
            #         if variant == answer:
            #             button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data='hello')
            #         else:
            #             button = InlineKeyboardButton(text=variant, callback_data='hello')
            #     else:
            #         if variant in answer:
            #             button = InlineKeyboardButton(text=f'🔘{variant}🔘', callback_data='hello')
            #         else:
            #             button = InlineKeyboardButton(text=variant, callback_data='hello')
            #     list_buttons.append([button])
            # keyboard = InlineKeyboardMarkup(inline_keyboard=list_buttons)
            # await bot.send_message(text=question_text, reply_markup=keyboard, chat_id=press_user_id)
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
            result = list_answers,
            right_answers = right,
            wrong_answers = wrong
        )
        session.add(result)
        session.commit()
        session.close()
        await bot.send_message(text='Ваш результат успішно збережено\nВи можете подивидить за командою /results', chat_id=press_user_id)
    del users_test_data[press_user_id]