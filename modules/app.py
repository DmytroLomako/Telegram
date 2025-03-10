import PIL.Image, PIL.ImageTk, customtkinter as ctk, os, json, PIL, webbrowser, smtplib
from .add_users import add_users
from .models import Teacher, Session, Result, User, ResultQuiz
from .get_user_results import get_results
from .get_test_results import get_test_results
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

questions = []
list_links_names = []
list_links = []

app = ctk.CTk()
auth_teacher = False
list_images_path = []
width = 600
height = 440
x = (app.winfo_screenwidth() // 2) - (width // 2)
y = (app.winfo_screenheight() // 2) - (height // 2) - 50
app.geometry(f'{width}x{height}+{x}+{y}')
app.title("Settings")
app.resizable(False, False)

def open_link(link):
    webbrowser.open(link)

world_label = ctk.CTkLabel(app, text="WORLD", font=("Arial", 20), text_color='orange')
it_label = ctk.CTkLabel(app, text=".IT", font=("Arial", 20))
it_label.place(x=560, y=400)
world_label.place(x=486, y=400)
it_label.bind("<Button-1>", lambda e: open_link("https://www.instagram.com/world.it.academy/"))
world_label.bind("<Button-1>", lambda e: open_link("https://www.instagram.com/world.it.academy/"))
button_help = ctk.CTkButton(app, text="Підтримка", font=("Arial", 20), width=120, height=35, command=lambda: open_link("mailto:worldit_academy@worldit.academy"))
button_help.place(x=470, y=10)

dmytro_lomako = ctk.CTkLabel(app, text="DmytroLomako", font=("Arial", 20), text_color='white')
dmytro_lomako.place(x=330, y=400)
dmytro_lomako.bind("<Button-1>", lambda e: open_link("https://github.com/DmytroLomako/Telegram"))

frame_all_questions = ctk.CTkScrollableFrame(app, width=600, height=350, fg_color='transparent')
bot_frame = ctk.CTkFrame(app, width=width, height=0, fg_color='transparent')
bot_working = ctk.CTkLabel(bot_frame, text="Бот не працює", font=("Arial", 18))
bot_working.pack(side='left', padx=3)

path_cross_img = os.path.abspath(__file__ + '/../../static/app_images/cross.png')
image_cross = ctk.CTkImage(PIL.Image.open(path_cross_img), size=(20, 20))
cross = ctk.CTkLabel(bot_frame, text='', image=image_cross)

path_check_mark_img = os.path.abspath(__file__ + '/../../static/app_images/check-mark.png')
image_check_mark = ctk.CTkImage(PIL.Image.open(path_check_mark_img), size=(20, 20))

cross.pack(side='right')
bot_frame.place(x=10, y=403)

main_frame = ctk.CTkFrame(app, width=width, height=height, fg_color='transparent')
add_users_button = ctk.CTkButton(main_frame, text="Додати користувачів", font=("Arial", 20), width=260, height=40, command=lambda: add_users(auth_teacher))
button_add_test = ctk.CTkButton(main_frame, text="Додати тест", font=("Arial", 20), width=260, height=40, command=lambda: add_test())
button_get_results = ctk.CTkButton(main_frame, text="Отримати результати учнів", font=("Arial", 20), width=260, height=40, command=lambda: get_results_window())
button_get_test_results = ctk.CTkButton(main_frame, text="Отримати результати тесту", font=("Arial", 20), width=260, height=40, command=lambda: get_test_results_window())
button_add_teachers = ctk.CTkButton(main_frame, text="Додати вчителя", font=("Arial", 20), width=260, height=40, command=lambda: add_teacher())
add_users_button.pack(pady=15)
button_add_test.pack(pady=15)
button_get_results.pack(pady=15)
button_get_test_results.pack(pady=15)
input_test_name = ctk.CTkEntry(app, placeholder_text="Введіть назву тесту", width=300, height=40, font=("Arial", 18))
button_back = ctk.CTkButton(app, text="⬅", font=("Arial", 20), width=30, height=40, command=lambda: back())
frame_buttons = ctk.CTkFrame(frame_all_questions, width=500, height=50, fg_color='transparent')
frame_buttons.pack(pady=10)
button_create_question_variant = ctk.CTkButton(frame_buttons, text="Додати запитання з варіантами", font=("Arial", 16), width=170, height=30, command=lambda: create_question_variant())
button_create_question_variant.pack(side="left", padx=10)
button_create_question_input = ctk.CTkButton(frame_buttons, text="Додати запитання з введенням", font=("Arial", 16), width=170, height=30, command=lambda: create_question_input())
button_create_question_input.pack(side="right", padx=10)
button_create_link = ctk.CTkButton(frame_all_questions, text="Додати посилання для закріплення матеріалу", font=("Arial", 16), width=170, height=30, command=lambda: create_question_link())
button_create_link.pack()
button_save_test = ctk.CTkButton(frame_all_questions, text="Зберегти", font=("Arial", 20), width=200, height=40, command=lambda: save_test())
button_save_test.pack(pady=50)

def create_question_link():
    global count    
    list_names = []
    list_links = []
    modal_window = ctk.CTkToplevel(app)
    modal_window.title("Посилання")
    modal_window_width = 650
    count = 1
    modal_window_height = 400
    modal_window_y = (app.winfo_screenheight() // 2) - (modal_window_height // 2) - 50
    modal_window_x = (app.winfo_screenwidth() // 2) - (modal_window_width // 2)
    modal_window.geometry(f'{modal_window_width}x{modal_window_height}+{modal_window_x}+{modal_window_y}')
    
    def delete_link(frame, entry_name, entry_link):
        global count
        if count > 1:
            list_names.remove(entry_name)
            list_links.remove(entry_link)
            count -= 1
            frame.destroy()
            add_button.place(x=590, y=75*count)
        print(len(list_names))
        
    def add_link():
        global count
        count += 1
        button_save.pack_forget()
        frame = ctk.CTkFrame(modal_window, width=350, height=40, fg_color='transparent')
        frame.pack(pady=20)
        entry_name = ctk.CTkEntry(frame, placeholder_text="Введіть назву посилання", width=230, height=40, font=("Arial", 16))
        entry_name.pack(side="left", padx=10)
        entry_link = ctk.CTkEntry(frame, placeholder_text="Вставте посилання", width=330, height=40, font=("Arial", 16))
        entry_link.pack(side="left", padx=10)
        path_button_trash = os.path.abspath(__file__ + f"/../../static/app_images/trash.png")
        trash_img = PIL.ImageTk.PhotoImage(PIL.Image.open(path_button_trash).resize((35, 35)))
        trash_button = ctk.CTkLabel(frame, text="", image=trash_img)
        trash_button.pack(side='left')
        trash_button.bind("<Button-1>", lambda e: delete_link(frame, entry_name, entry_link))
        add_button.place(x=590, y=75*count)
        list_names.append(entry_name)
        list_links.append(entry_link)
        print(len(list_names))
        if count == 4:
            add_button.place_forget()
        button_save.pack(pady=20)
        
    path_button_add = os.path.abspath(__file__ + f"/../../static/app_images/add.png")
    add_img = PIL.ImageTk.PhotoImage(PIL.Image.open(path_button_add).resize((30, 30)))
    add_button = ctk.CTkLabel(modal_window, text="", image=add_img)
    add_button.bind("<Button-1>", lambda event: add_link())
    add_button.place(x=590, y=75)
        
    frame = ctk.CTkFrame(modal_window, width=350, height=40, fg_color='transparent')
    frame.pack(pady=20)
    entry_name = ctk.CTkEntry(frame, placeholder_text="Введіть назву посилання", width=230, height=40, font=("Arial", 16))
    entry_name.pack(side="left", padx=10)
    entry_link = ctk.CTkEntry(frame, placeholder_text="Вставте посилання", width=330, height=40, font=("Arial", 16))
    entry_link.pack(side="left", padx=10)
    list_names.append(entry_name)
    list_links.append(entry_link)
    path_button_trash = os.path.abspath(__file__ + f"/../../static/app_images/trash.png")
    trash_img = PIL.ImageTk.PhotoImage(PIL.Image.open(path_button_trash).resize((35, 35)))
    trash_button = ctk.CTkLabel(frame, text="", image=trash_img)
    trash_button.pack(side='left')
    trash_button.bind("<Button-1>", lambda e: delete_link(frame, entry_name, entry_link))
    button_save = ctk.CTkButton(modal_window, text="Зберегти", font=("Arial", 20), width=160, height=35, command=lambda: create_link(list_names, list_links, modal_window))
    button_save.pack(pady=20)

def create_link(names, links, modal_window):
    global list_links_names, list_links
    for link in links:
        if link.get() != "":
            list_links.append(link.get())
    for name in names:
        if name.get() != "":
            list_links_names.append(name.get())
    modal_window.destroy()

def get_test_results_window():
    modal_window = ctk.CTkToplevel(app)
    modal_window.title("Результати")
    modal_window_width = 400
    modal_window_height = 300
    modal_window_x = (app.winfo_screenwidth() // 2) - (modal_window_width // 2)
    modal_window_y = (app.winfo_screenheight() // 2) - (modal_window_height // 2) - 50
    modal_window.geometry(f'{modal_window_width}x{modal_window_height}+{modal_window_x}+{modal_window_y}')
    scrollable_frame = ctk.CTkScrollableFrame(modal_window, width=350, height=280, fg_color='transparent')
    scrollable_frame.pack(pady=10)
    session = Session()
    results = session.query(ResultQuiz).all()
    list_id = []
    for result in results:
        if result.test_id not in list_id:
            frame = ctk.CTkFrame(scrollable_frame, width=350, height=40)
            frame.pack(pady=10)
            user_number = ctk.CTkLabel(frame, text=f'{len(list_id) + 1}.', font=("Arial", 20), width=20, height=35)
            user_number.pack(side='left', padx=10)
            test_name = ctk.CTkLabel(frame, text=f'{result.test_name}', font=("Arial", 20))
            test_name.pack(side='left', padx=0)
            path_button_download = os.path.abspath(__file__ + '/../../static/app_images/download.png')
            image_download = ctk.CTkImage(PIL.Image.open(path_button_download), size=(20, 20))
            button_download = ctk.CTkButton(frame, text="", image=image_download, width=20, height=20, command=lambda: get_test_results(result.test_id))
            button_download.pack(side='right', padx=10)
            frame.pack_propagate(False)
            # ctk.CTkButton(frame, text=f'{user.username}', font=("Arial", 16), width=200, height=35, command=lambda user=user: get_results(result.user_id))
            list_id.append(result.test_id)

def add_teacher():
    modal_window = ctk.CTkToplevel(app)
    modal_window.title("Створення Вчителя")
    modal_window_width = 400
    modal_window_height = 330
    modal_window_x = (app.winfo_screenwidth() // 2) - (modal_window_width // 2)
    modal_window_y = (app.winfo_screenheight() // 2) - (modal_window_height // 2) - 50
    modal_window.geometry(f'{modal_window_width}x{modal_window_height}+{modal_window_x}+{modal_window_y}')
    modal_window.resizable(False, False)   
    frame = ctk.CTkFrame(modal_window, width=modal_window_width, height=modal_window_height, fg_color='transparent')
    frame.pack(pady=20)
    name = ctk.CTkEntry(frame, placeholder_text="Введіть ім'я", width=300, height=40, font=("Arial", 18))
    name.pack(pady=15)
    password = ctk.CTkEntry(frame, placeholder_text="Введіть пароль", width=300, height=40, font=("Arial", 18))
    password.pack(pady=15)
    email = ctk.CTkEntry(frame, placeholder_text="Введіть пошту", width=300, height=40, font=("Arial", 18))
    email.pack(pady=15)
    button_save = ctk.CTkButton(frame, text="Додати", font=("Arial", 20), width=200, height=40, command=lambda: save_teacher(name.get(), password.get(), email.get(), modal_window) if name.get() and password.get() and email.get() and '@gmail.com' in email.get() else None)
    button_save.pack(pady=20)

def save_teacher(name, password, email, modal_window):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
    server.login("", "")
    session = Session()
    teacher = Teacher(username=name, password=password, email=email)
    msg = MIMEMultipart()
    msg["Subject"] = "Ваш Quiz Teacher Account"
    body = f"Ваш логін: {name}\nВаш пароль: {password}\nУвійти в ваш обліковий запис ви можете, увійшовши в Telegram, вписавши у пошуку '@QuizTgDBot' і у боті написавши '/auth'."
    msg.attach(MIMEText(body, "plain"))
    server.sendmail("", f"{email}", msg.as_string())
    session.add(teacher)
    session.commit()
    session.close()
    server.quit()
    modal_window.destroy()

def get_results_window():
    modal_window = ctk.CTkToplevel(app)
    modal_window.title("Результати")
    modal_window_width = 400
    modal_window_height = 300
    modal_window_x = (app.winfo_screenwidth() // 2) - (modal_window_width // 2)
    modal_window_y = (app.winfo_screenheight() // 2) - (modal_window_height // 2) - 50
    modal_window.geometry(f'{modal_window_width}x{modal_window_height}+{modal_window_x}+{modal_window_y}')
    scrollable_frame = ctk.CTkScrollableFrame(modal_window, width=350, height=280, fg_color='transparent')
    scrollable_frame.pack(pady=10)
    session = Session()
    results = session.query(Result).all()
    list_users = []
    for result in results:
        if result.user_id not in list_users:
            user = session.query(User).filter_by(id=result.user_id).first()
            frame = ctk.CTkFrame(scrollable_frame, width=350, height=40)
            frame.pack(pady=10)
            user_number = ctk.CTkLabel(frame, text=f'{len(list_users) + 1}.', font=("Arial", 20), width=20, height=35)
            user_number.pack(side='left', padx=10)
            name = ctk.CTkLabel(frame, text=f'{user.username}', font=("Arial", 20))
            name.pack(side='left', padx=0)
            path_button_download = os.path.abspath(__file__ + '/../../static/app_images/download.png')
            image_download = ctk.CTkImage(PIL.Image.open(path_button_download), size=(20, 20))
            button_download = ctk.CTkButton(frame, text="", image=image_download, width=20, height=20, command=lambda user=user: get_results(result.user_id))
            button_download.pack(side='right', padx=10)
            frame.pack_propagate(False)
            # ctk.CTkButton(frame, text=f'{user.username}', font=("Arial", 16), width=200, height=35, command=lambda user=user: get_results(result.user_id))
            list_users.append(result.user_id)

def save_test():
    file_name = input_test_name.get()
    os.makedirs(os.path.abspath(__file__ + f"/../../static/tests/{auth_teacher.username}"), exist_ok=True)
    path_to_file = os.path.abspath(__file__ + f"/../../static/tests/{auth_teacher.username}/{file_name}.json")

    for image_path in list_images_path:
        image = PIL.Image.open(image_path)
        image_path = image_path.split('/')[-1]
        image_path = f'{file_name}/{image_path}'
        os.makedirs(os.path.abspath(__file__ + f"/../../static/images/{file_name}"), exist_ok=True)
        image.save(os.path.abspath(__file__ + f"/../../static/images/{image_path}"))
    for question in questions:
        if question['image']:
            question['image'] = f'{file_name}/{question["image"]}'
              
    if list_links_names and list_links:
        links = {}
        for i in range(len(list_links_names)):
            links[list_links_names[i]] = list_links[i]
    else:
        links = False
    
    data = {
        'questions': questions,
        'links': links
    }
    with open(path_to_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    back()

def save_input_question(question, answer, modal_window, image_path):

    if image_path:
        list_images_path.append(image_path)
        image_path = image_path.split('/')[-1]
    
    questions.append({
        'question': question,
        "image": image_path,
        "variants": [],
        "type": "input",
        'correct_answer': [answer]
    })
    def delete_question(index):
        if questions[index]['image']:
            for path in list_images_path:
                if questions[index]['image'] in path.split('/')[-1]:
                    list_images_path.remove(path)
                    break
        del questions[index]
        frame_questions.destroy()
    modal_window.destroy()
    frame_buttons.pack_forget()
    button_create_link.pack_forget()
    button_save_test.pack_forget()
    frame_questions = ctk.CTkFrame(frame_all_questions, width=500, height=60)
    frame_questions.pack(pady=20)
    label_question = ctk.CTkLabel(frame_questions, text=questions[-1]['question'], font=("Arial", 16))
    label_question.pack(pady=10, anchor='w', padx=15)
    path_button_trash = os.path.abspath(__file__ + f"/../../static/app_images/trash-can.png")
    trash_img = PIL.ImageTk.PhotoImage(PIL.Image.open(path_button_trash).resize((22, 22)))
    button_trash = ctk.CTkButton(frame_questions, text="", image=trash_img, width=23, height=26, fg_color='#504B4B', hover_color='#5C5858', command=lambda: delete_question(len(questions) - 1))
    button_trash.place(x=460, y=0)
    frame_buttons.pack(pady=30)
    button_create_link.pack(pady = 1)
    button_save_test.pack(pady=20)
    frame_questions.pack_propagate(False)
    
def create_question_input():
    global image
    image = False
    modal_window = ctk.CTkToplevel(app)
    modal_window.title("Додати запитання з введенням")
    modal_window_width = 400
    modal_window_height = 300
    modal_window_x = (app.winfo_screenwidth() // 2) - (modal_window_width // 2)
    modal_window_y = (app.winfo_screenheight() // 2) - (modal_window_height // 2) - 50
    modal_window.geometry(f'{modal_window_width}x{modal_window_height}+{modal_window_x}+{modal_window_y}')
    modal_window.resizable(False, False)
    
    def add_image():
        global image
        file_path = ctk.filedialog.askopenfilename(
            filetypes=[
                ('PNG', '*.png'),
                ('JPG', '*.jpg'),
                ('JPEG', '*.jpeg')
            ]
        )
        if file_path:
            image = file_path
            
    image_button_path = os.path.abspath(__file__ + f"/../../static/app_images/image.png")
    image_button_img = PIL.ImageTk.PhotoImage(PIL.Image.open(image_button_path).resize((30, 30)))
    image_button = ctk.CTkLabel(modal_window, text="", image=image_button_img)
    image_button.place(x=7, y=7)
    image_button.bind("<Button-1>", lambda event: add_image())
    question_input = ctk.CTkEntry(modal_window, placeholder_text="Введіть запитання", width=330, height=60, font=("Arial", 16))
    question_input.pack(pady=30)
    answer_input = ctk.CTkEntry(modal_window, placeholder_text="Введіть відповідь", width=280, height=40, font=("Arial", 16))
    answer_input.pack(pady=20)
    button_save = ctk.CTkButton(modal_window, text="Зберегти", font=("Arial", 20), width=200, height=40, command = lambda: save_input_question(question_input.get(), answer_input.get(), modal_window, image))
    button_save.pack(pady=20)
    
def save_variant_question(question, variant_inputs, checkboxes, modal_window, image_path):
    correct_answer = []
    variants = []
    test_name = input_test_name.get()
    for variant_input in variant_inputs:
        variants.append(variant_input.get())
    for i in range(len(checkboxes)):
        if checkboxes[i].get() == 1:
            correct_answer.append(variants[i])
    if image_path:
        list_images_path.append(image_path)
        image_path = image_path.split('/')[-1]
    questions.append({
        'question': question,
        "image": image_path,
        "variants": variants,
        'correct_answer': correct_answer
    })
    if len(correct_answer) > 1:
        questions[-1]['type'] = 'multi'
    else:
        questions[-1]['type'] = 'single'
        
    def delete_question(index):
        if questions[index]['image']:
            for path in list_images_path:
                if questions[index]['image'] in path.split('/')[-1]:
                    list_images_path.remove(path)
                    break
        del questions[index]
        frame_questions.destroy()
        
    modal_window.destroy()
    frame_buttons.pack_forget()
    button_create_link.pack_forget()
    button_save_test.pack_forget()
    frame_questions = ctk.CTkFrame(frame_all_questions, width=500, height=60)
    frame_questions.pack(pady=20)
    label_question = ctk.CTkLabel(frame_questions, text=questions[-1]['question'], font=("Arial", 16))
    label_question.pack(pady=10, anchor='w', padx=15)
    path_button_trash = os.path.abspath(__file__ + f"/../../static/app_images/trash-can.png")
    trash_img = PIL.ImageTk.PhotoImage(PIL.Image.open(path_button_trash).resize((22, 22)))
    button_trash = ctk.CTkButton(frame_questions, text="", image=trash_img, width=23, height=26, fg_color='#504B4B', hover_color='#5C5858', command=lambda: delete_question(len(questions) - 1))
    button_trash.place(x=460, y=0)
    frame_buttons.pack(pady=30)
    button_create_link.pack(pady=1)
    button_save_test.pack(pady=20)
    frame_questions.pack_propagate(False)
      
def create_question_variant():
    global modal_window_height, modal_window_y, image
    answer_frames = []
    answer_inputs = []
    answer_checkboxs = []
    image = False
    modal_window = ctk.CTkToplevel(app)
    modal_window.title("Додати запитання з варіантами")
    modal_window_width = 400
    modal_window_height = 205
    modal_window_x = (app.winfo_screenwidth() // 2) - (modal_window_width // 2)
    modal_window_y = (app.winfo_screenheight() // 2) - (modal_window_height // 2) - 50
    modal_window.geometry(f'{modal_window_width}x{modal_window_height}+{modal_window_x}+{modal_window_y}')
    modal_window.resizable(False, True)
    path_button_trash = os.path.abspath(__file__ + f"/../../static/app_images/trash.png")
    trash_img = PIL.ImageTk.PhotoImage(PIL.Image.open(path_button_trash).resize((30, 30)))
    
    def delete_answer():
        global modal_window_height, modal_window_y
        modal_window_height -= 60
        modal_window_y = (app.winfo_screenheight() // 2) - (modal_window_height // 2) - 50
        modal_window.geometry(f'{modal_window_width}x{modal_window_height}+{modal_window_x}+{modal_window_y}')
        add_button.place(x=360, y=105)
        for i in range(len(answer_inputs)):
            answer_inputs[i].configure(placeholder_text=f"Варіант {i+1}")
    
    def add_answer():
        global modal_window_height, modal_window_y
        if len(answer_frames) < 5:
            if len(answer_frames) == 4:
                add_button.place_forget()
            button_save.pack_forget()
            modal_window_height += 60
            modal_window_y = (app.winfo_screenheight() // 2) - (modal_window_height // 2) - 50
            modal_window.geometry(f'{modal_window_width}x{modal_window_height}+{modal_window_x}+{modal_window_y}')
            answer_frame = ctk.CTkFrame(modal_window, width=330, height=40, fg_color='transparent')
            answer_frame.pack(pady=10)
            trash_button = ctk.CTkLabel(answer_frame, text="", image=trash_img)
            trash_button.pack(side='left')
            variant_number = len(answer_frames) + 1
            answer_input = ctk.CTkEntry(answer_frame, placeholder_text=f"Варіант {variant_number}", width=280, height=40, font=("Arial", 16))
            answer_input.pack(side='left', padx=10)
            answer_checkbox = ctk.CTkCheckBox(answer_frame, text="", width=12, height=12)
            answer_checkbox.pack(side='right')
            answer_frames.append(answer_frame)
            answer_inputs.append(answer_input)
            answer_checkboxs.append(answer_checkbox)
            trash_button.bind("<Button-1>", lambda event: (answer_frame.destroy(), answer_frames.remove(answer_frame), answer_inputs.remove(answer_input), answer_checkboxs.remove(answer_checkbox), delete_answer()) if len(answer_frames) > 2 else None)
            button_save.pack(pady=20)
        
    def add_image():
        global image
        file_path = ctk.filedialog.askopenfilename(
            filetypes=[
                ('PNG', '*.png'),
                ('JPG', '*.jpg'),
                ('JPEG', '*.jpeg')
            ]
        )
        if file_path:
            image = file_path
    
    image_button_path = os.path.abspath(__file__ + f"/../../static/app_images/image.png")
    image_button_img = PIL.ImageTk.PhotoImage(PIL.Image.open(image_button_path).resize((30, 30)))
    image_button = ctk.CTkLabel(modal_window, text="", image=image_button_img)
    image_button.place(x=7, y=7)
    image_button.bind("<Button-1>", lambda event: add_image())
    
    question_input = ctk.CTkEntry(modal_window, placeholder_text="Введіть запитання", width=330, height=60, font=("Arial", 16))
    question_input.pack(pady=35)
    path_button_add = os.path.abspath(__file__ + f"/../../static/app_images/add.png")
    add_img = PIL.ImageTk.PhotoImage(PIL.Image.open(path_button_add).resize((30, 30)))
    add_button = ctk.CTkLabel(modal_window, text="", image=add_img)
    add_button.bind("<Button-1>", lambda event: add_answer())
    add_button.place(x=360, y=105)
    button_save = ctk.CTkButton(modal_window, text="Зберегти", font=("Arial", 20), width=200, height=40, command = lambda: save_variant_question(question_input.get(), answer_inputs, answer_checkboxs, modal_window, image))
    button_save.pack(pady=20)
    add_answer()
    add_answer()

def back():
    input_test_name.pack_forget()
    button_back.place_forget()
    frame_all_questions.pack_forget()
    # bot_working.place(x=10, y=10)
    if auth_teacher and auth_teacher.is_admin:
        print(10)
        button_add_teachers.pack(pady=15)
        main_frame.pack(padx=40, pady=40)
    else:
        main_frame.pack(pady=80, padx=80)
    print(auth_teacher)

def add_test():
    # bot_working.place_forget()
    if auth_teacher and auth_teacher.is_admin:
        button_add_teachers.pack_forget()
    main_frame.pack_forget()
    input_test_name.pack(pady=30)
    button_back.place(x=10, y=10)
    frame_buttons.pack(pady=30)
    button_create_link.pack()
    frame_all_questions.pack()
    
def logout():
    pass

def authorize(name, password):
    global auth_teacher
    session = Session()
    teacher = session.query(Teacher).filter_by(username=name, password=password).first()
    if teacher:
        auth_teacher = teacher
        auth_frame.pack_forget()
        # bot_working.place(x=10, y=10)
        bot_working.configure(text=f"Бот працює")
        cross.configure(image=image_check_mark)
        
        # path_logout = os.path.abspath(__file__ + f"/../../static/app_images/logout.png")
        # logout_img = PIL.ImageTk.PhotoImage(PIL.Image.open(path_logout).resize((20, 20)))
        # button_logout = ctk.CTkButton(app, text="Вийти", image=logout_img, width=35, height=10, compound='right', font=("Arial", 18), command=lambda: logout())    
        # button_logout.place(x=10, y=50)
    
        if auth_teacher.is_admin:
            button_add_teachers.pack(pady=15)
            main_frame.pack(padx=40, pady=40)
        else:
            main_frame.pack(padx=80, pady=80)
        # main_frame.pack_propagate(False)
    else:
        auth_text.configure(text="Неправильне ім'я або пароль")
    session.close()

auth_frame = ctk.CTkFrame(app, width=300, height=300, fg_color='transparent')
auth_text = ctk.CTkLabel(auth_frame, text="Авторизація", font=("Arial", 40))
auth_text.pack(pady=30)
input_name = ctk.CTkEntry(auth_frame, placeholder_text="Введіть своє ім'я", width=300, height=40, font=("Arial", 18))
input_name.pack(pady=10)
input_password = ctk.CTkEntry(auth_frame, placeholder_text="Введіть свій пароль", width=300, height=40, font=("Arial", 18))
input_password.pack(pady=10)
auth_button = ctk.CTkButton(auth_frame, text="Авторизуватись", font=("Arial", 20), width=200, height=40, command=lambda: authorize(input_name.get(), input_password.get()))
auth_button.pack(pady=20)
auth_frame.pack(pady=50)