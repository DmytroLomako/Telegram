import os.path, customtkinter as ctk, pandas as pd, smtplib 
from .models import User, Session, Teacher
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def add_users(teacher = False):
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
            
        if teacher:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
            server.login("", "")
            for index, row in data.iterrows():
                try:
                    print(row['Username'], row['Password'], row['Email'])   
                    session = Session()
                    get_user = session.query(User).filter_by(username=row['Username'], password=row['Password'], email=row['Email']).first()
                    if get_user:
                        if teacher not in get_user.teachers:
                            get_user.teachers.append(teacher)
                    else:
                        user = User(username=row['Username'], password=row['Password'], email=row['Email'])
                        user.teachers.append(teacher)
                        session.add(user)
                        msg = MIMEMultipart()
                        msg["Subject"] = "Ваш Quiz Student Account"
                        body = f"Ваш логін: {row['Username']}\nВаш пароль: {row['Password']}\nУвійти в ваш обліковий запис ви можете, увійшовши в Telegram, вписавши у пошуку '@QuizTgDBot' і у боті написавши '/auth'."
                        msg.attach(MIMEText(body, "plain"))
                        server.sendmail("", f"{row['Email']}", msg.as_string())
                        
                        
                    session.commit()
                    session.close()
                    
                except Exception as error:
                    print(f'Помилка при створенні користувача {index}: {error}')
                    
            server.quit()
        else:
            session = Session()
            for index, row in data.iterrows():
                try:
                    teacher = Teacher(username=row['Username'], password=row['Password'])
                    session.add(teacher)
                    session.commit()
                except Exception as error:
                    print(f'Помилка при створенні вчителя {index}: {error}')

            session.close()
                
    except FileNotFoundError:
        print('Файл не знайдено')