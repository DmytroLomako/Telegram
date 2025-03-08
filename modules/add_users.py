import os.path, customtkinter as ctk, pandas as pd
from .models import User, Session


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
                session.commit()
                session.close()
                
            except Exception as error:
                print(f'Помилка при створенні користувача {index}: {error}')
                
    except FileNotFoundError:
        print('Файл не знайдено')