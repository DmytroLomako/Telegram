from aiogram import Bot, Dispatcher


bot = Bot('') # Your Telegram Bot Api Token
dispatcher = Dispatcher()

id_admins = [] # Your Telegram Id

list_code = []

user_status = {}

quiz_dict = {}

result_dict = {}

last_question = {}

users_test_data = {}

# {
#     'telegram_id': {
#         'test_name': 'name',
#         'question_index': 'index',
#         'answers': ['answer1', 'answer2']
#     }
# }

# Создание:
# WINDOWS: python -m venv venv
# MAC OS: python3 -m venv venv
# Активация 
# WINDOWS: venv/scripts/activate
# MAC OS: source venv/bin/activate
# Установка из файла
# WINDOWS & MAC OS: pip install -r file_name

# {
#     '4104': {
#         "users":[{
#             "name":'Roman',
#             "answers": None,
#             "id": 
#         }],
#         "chat_id_admin": 0,
#         "id_message_users": 0,
#         "quiz_name": quiz1,
#         "question_index": 0,
#         "id_message_answer": 0000000000
#     }, 
#     '7428': {
#         "users":[{
#             "name":'Roman',
#             "id": 
#         }]
#         "chat_id_admin" 
#         "id_message_users"
#         "quiz_name": quiz2
#     }, 
# }