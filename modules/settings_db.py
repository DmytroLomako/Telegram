import sqlalchemy, os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

path_to_db = os.path.abspath(os.path.join(__file__, '..', '..', 'instance', 'data.db'))
print(path_to_db)
db = sqlalchemy.create_engine(f'sqlite:///{path_to_db}')
Base = declarative_base()
Session = sessionmaker(bind=db)