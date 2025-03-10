from .settings_db import *
import sqlalchemy
from sqlalchemy.orm import relationship

user_teacher = sqlalchemy.Table(
    'user_teacher',
    Base.metadata,
    sqlalchemy.Column('users_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('teachers_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('teachers.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    results = relationship('Result', back_populates='user', cascade='all, delete')
    quiz_results = relationship('ResultQuiz', back_populates='user', cascade='all, delete') 
    username = sqlalchemy.Column(sqlalchemy.String)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True, default=None)
    password = sqlalchemy.Column(sqlalchemy.String(15))
    email = sqlalchemy.Column(sqlalchemy.String)
    teachers = relationship('Teacher', secondary=user_teacher, back_populates='users')
    def __repr__(self):
        return f'User: {self.username}, Id: {self.telegram_id}'

class Teacher(Base):
    __tablename__ = 'teachers'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String(15))
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True, default=None)
    users = relationship('User', secondary=user_teacher, back_populates='teachers')
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=None)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    def __repr__(self):
        return f'Teacher: {self.username}'
    
class Result(Base):
    __tablename__ = 'results'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user = relationship('User', back_populates='results')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='CASCADE'))
    test_name = sqlalchemy.Column(sqlalchemy.String)
    result = sqlalchemy.Column(sqlalchemy.String)
    right_answers = sqlalchemy.Column(sqlalchemy.Integer)
    wrong_answers = sqlalchemy.Column(sqlalchemy.Integer)
    def __repr__(self):
        return f'Result: {self.result}, User: {self.user_id}'
    
class ResultQuiz(Base):
    __tablename__ = 'results_quiz'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    test_id = sqlalchemy.Column(sqlalchemy.Integer)
    user = relationship('User', back_populates='quiz_results')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='CASCADE'))
    test_name = sqlalchemy.Column(sqlalchemy.String)
    right_answers = sqlalchemy.Column(sqlalchemy.Integer)
    wrong_answers = sqlalchemy.Column(sqlalchemy.Integer)
    def __repr__(self):
        return f'User: {self.user_id}'
    
Base.metadata.create_all(db)