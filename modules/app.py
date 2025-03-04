import customtkinter as ctk, os, json
from .add_users import add_users

questions = []

app = ctk.CTk()
width = 600
height = 440
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2) - 50
app.geometry(f'{width}x{height}+{x}+{y}')
app.title("Settings")
app.resizable(False, False)
frame_all_questions = ctk.CTkScrollableFrame(app, width=600, height=350, fg_color='transparent')
bot_working = ctk.CTkLabel(app, text="Бот працює", font=("Arial", 40))
add_users_button = ctk.CTkButton(app, text="Додати користувачів", font=("Arial", 20), width=230, height=40, command=lambda: add_users())
button_add_test = ctk.CTkButton(app, text="Додати тест", font=("Arial", 20), width=230, height=40, command=lambda: add_test())
input_test_name = ctk.CTkEntry(app, placeholder_text="Введіть назву тесту", width=300, height=40, font=("Arial", 18))
button_back = ctk.CTkButton(app, text="⬅", font=("Arial", 20), width=30, height=40, command=lambda: back())
frame_buttons = ctk.CTkFrame(frame_all_questions, width=500, height=80, fg_color='transparent')
frame_buttons.pack(pady=20)
button_create_question_variant = ctk.CTkButton(frame_buttons, text="Додати запитання з варіантами", font=("Arial", 16), width=170, height=30, command=lambda: create_question_variant())
button_create_question_variant.pack(side="left", padx=10)
button_create_question_input = ctk.CTkButton(frame_buttons, text="Додати запитання з введенням", font=("Arial", 16), width=170, height=30, command=lambda: create_question_input())
button_create_question_input.pack(side="right", padx=10)
button_save_test = ctk.CTkButton(frame_all_questions, text="Зберегти", font=("Arial", 20), width=200, height=40, command=lambda: save_test())
button_save_test.pack(pady=20)

def create_question_variant():
    pass

def save_test():
    file_name = input_test_name.get()
    path_to_file = os.path.abspath(__file__ + f"/../../static/{file_name}.json")
    data = {
        'questions': questions
    }
    with open(path_to_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    back()

def save_input_question(question, answer, modal_window):
    questions.append({
        'question': question,
        "variants": [],
        "type": "input",
        'correct_answer': [answer]
    })
    def delete_question(index):
        del questions[index]
        frame_questions.destroy()
    modal_window.destroy()
    frame_buttons.pack_forget()
    button_save_test.pack_forget()
    frame_questions = ctk.CTkFrame(frame_all_questions, width=500, height=60)
    frame_questions.pack(pady=20)
    label_question = ctk.CTkLabel(frame_questions, text=questions[-1]['question'], font=("Arial", 16))
    label_question.pack(pady=10, anchor='w', padx=15)
    button_trash = ctk.CTkButton(frame_questions, text="🗑️", font=("Arial", 10), width=30, height=30, command=lambda: delete_question(len(questions) - 1))
    button_trash.place(x=470, y=0)
    frame_buttons.pack(pady=30)
    button_save_test.pack(pady=20)
    frame_questions.pack_propagate(False)
    
def create_question_input():
    modal_window = ctk.CTkToplevel(app)
    modal_window.title("Додати запитання з введенням")
    modal_window.geometry("400x300")
    modal_window.resizable(False, False)
    question_input = ctk.CTkEntry(modal_window, placeholder_text="Введіть запитання", width=330, height=60, font=("Arial", 16))
    question_input.pack(pady=30)
    answer_input = ctk.CTkEntry(modal_window, placeholder_text="Введіть відповідь", width=280, height=40, font=("Arial", 16))
    answer_input.pack(pady=20)
    button_save = ctk.CTkButton(modal_window, text="Зберегти", font=("Arial", 20), width=200, height=40, command = lambda: save_input_question(question_input.get(), answer_input.get(), modal_window))
    button_save.pack(pady=20)

def back():
    input_test_name.pack_forget()
    button_back.place_forget()
    frame_all_questions.pack_forget()
    bot_working.pack(pady=60)
    add_users_button.pack(pady=15)
    button_add_test.pack(pady=15)

def add_test():
    bot_working.pack_forget()
    add_users_button.pack_forget()
    button_add_test.pack_forget()
    input_test_name.pack(pady=30)
    button_back.place(x=10, y=10)
    frame_buttons.pack(pady=30)
    frame_all_questions.pack()


def authorize(name, password):
    # if name == "admin" and password == "admin":
    auth_text.pack_forget()
    input_name.pack_forget()
    input_password.pack_forget()
    auth_button.pack_forget()
    bot_working.pack(pady=60)
    add_users_button.pack(pady=15)
    button_add_test.pack(pady=15)
    # else:
    #     auth_text.configure(text="Неправильне ім'я або пароль")

auth_text = ctk.CTkLabel(app, text="Authorization", font=("Arial", 40))
auth_text.pack(pady=40)
input_name = ctk.CTkEntry(app, placeholder_text="Введіть своє ім'я", width=300, height=40, font=("Arial", 18))
input_name.pack(pady=10)
input_password = ctk.CTkEntry(app, placeholder_text="Введіть свій пароль", width=300, height=40, font=("Arial", 18))
input_password.pack(pady=10)
auth_button = ctk.CTkButton(app, text="Авторизуватись", font=("Arial", 20), width=200, height=40, command=lambda: authorize(input_name.get(), input_password.get()))
auth_button.pack(pady=15)