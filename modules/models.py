from .settings_db import *
import sqlalchemy
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    results = relationship('Result', back_populates='user', cascade='all, delete')
    username = sqlalchemy.Column(sqlalchemy.String)
    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True, default=None)
    password = sqlalchemy.Column(sqlalchemy.String(15))
    def __repr__(self):
        return f'User: {self.username}, Id: {self.telegram_id}'
    
class Result(Base):
    __tablename__ = 'results'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user = relationship('User', back_populates='results')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id', ondelete='CASCADE'))
    test_name = sqlalchemy.Column(sqlalchemy.String)
    result = sqlalchemy.Column(sqlalchemy.String)
    def __repr__(self):
        return f'Result: {self.result}, User: {self.user_id}'
    
Base.metadata.create_all(db)