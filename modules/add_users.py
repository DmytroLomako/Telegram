import os.path, customtkinter as ctk, pandas as pd, smtplib, random
from .models import User, Session, Teacher
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .settings import SYMBOLS, NUMBERS, LETTERS


def add_users(teacher):
    try:
        file_path = ctk.filedialog.askopenfilename(
            filetypes=[
                ('XLS', '*.xlsx'),
                ('ODS', '*.ods'),
                ('CSV', '*.csv'),
                ('TSV', '*.tsv')
            ]
        )
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension in '.xlsx':
            data = pd.read_excel(file_path)
        
        elif file_extension == '.ods':
            data = pd.read_excel(file_path, engine='odf')
            
        elif file_extension == '.csv':
            data = pd.read_csv(file_path)
            
        elif file_extension == '.tsv':
            data = pd.read_csv(file_path, sep='\t')

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
        server.login("", "")
        for index, row in data.iterrows():
            try:
                username = row['Username'].rstrip()
                email = row['Email'].rstrip()
                print(row['Username'], email)   
                session = Session()
                get_user = session.query(User).filter_by(username=username, email=email).first()
                if get_user:
                    if teacher not in get_user.teachers:
                        get_user.teachers.append(teacher)
                else:
                    chosen_symbol = random.choice(SYMBOLS)
                    chosen_number = random.choice(NUMBERS)
                    chosen_letters = [random.choice(LETTERS) for i in range(6)]
                    password_elements_list = [chosen_symbol] + [chosen_number] + chosen_letters
                    random.shuffle(password_elements_list)
                    password = ''.join(password_elements_list)
                    user = User(username=username, password=password, email=email)
                    user.teachers.append(teacher)
                    session.add(user)
                    msg = MIMEMultipart()
                    msg["Subject"] = "Ваш Quiz Student Account"
                    body = f"Ваш логін: {username}\nВаш пароль: {password}\nУвійти в ваш обліковий запис ви можете, увійшовши в Telegram, вписавши у пошуку '@QuizTgDBot' і у боті написавши '/auth'."
                    msg.attach(MIMEText(body, "plain"))
                    server.sendmail("", f"{email}", msg.as_string())
                    
                    
                session.commit()
                session.close()
                
            except Exception as error:
                print(f'Помилка при створенні користувача {index}: {error}')
                
        server.quit()
                
    except FileNotFoundError:
        print('Файл не знайдено')