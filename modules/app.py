import customtkinter as ctk
from .add_users import add_users


app = ctk.CTk()
width = 600
height = 440
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2) - 50
app.geometry(f'{width}x{height}+{x}+{y}')
app.title("Settings")
app.resizable(False, False)

def authorize(name, password):
    if name == "admin" and password == "admin":
        auth_text.destroy()
        input_name.destroy()
        input_password.destroy()
        auth_button.destroy()
        bot_working = ctk.CTkLabel(app, text="Бот працює", font=("Arial", 40))
        bot_working.pack(pady=60)
        add_users_button = ctk.CTkButton(app, text="Додати користувачів", font=("Arial", 20), width=230, height=40, command=lambda: add_users())
        add_users_button.pack(pady=15)
    else:
        auth_text.configure(text="Неправильне ім'я або пароль")

auth_text = ctk.CTkLabel(app, text="Authorization", font=("Arial", 40))
auth_text.pack(pady=40)
input_name = ctk.CTkEntry(app, placeholder_text="Введіть своє ім'я", width=300, height=40, font=("Arial", 18))
input_name.pack(pady=10)
input_password = ctk.CTkEntry(app, placeholder_text="Введіть свій пароль", width=300, height=40, font=("Arial", 18))
input_password.pack(pady=10)
auth_button = ctk.CTkButton(app, text="Авторизуватись", font=("Arial", 20), width=200, height=40, command=lambda: authorize(input_name.get(), input_password.get()))
auth_button.pack(pady=15)