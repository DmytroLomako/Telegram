import customtkinter as ctk


app = ctk.CTk()
width = 600
height = 440
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2) - 50
app.geometry(f'{width}x{height}+{x}+{y}')
app.title("Settings")
app.resizable(False, False)

bot_working = ctk.CTkLabel(app, text="Bot is working", font=("Arial", 40))
bot_working.pack(pady=190)