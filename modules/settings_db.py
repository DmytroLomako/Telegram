import sqlalchemy, os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

path_to_db = os.path.abspath(os.path.join(__file__, '..', '..', 'instance'))
os.makedirs(path_to_db, exist_ok=True)
print(path_to_db)
db = sqlalchemy.create_engine(f'sqlite:///{path_to_db}/data.db', max_overflow=-1)
Base = declarative_base()
Session = sessionmaker(bind=db)