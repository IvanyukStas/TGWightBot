from sqlalchemy import sql, Sequence, Column, DateTime
from datetime import datetime

from utils.db_api.database import db


class User(db.Model):
    __tablename__ = 'users'
    query: sql.Select

    id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    user_name = db.Column(db.String(50))
    user_tg_id = db.Column(db.Integer)
    date_of_create = db.Column(DateTime, default=datetime.utcnow)



    def __repr__(self):
        return f'''
        id: {self.id}
        User: {self.user_name}
        Вес: {self.user_weight}
        '''


class Weight(db.Model):
    __tablename__ = 'weight'
    query: sql.Select


    id = db.Column(db.Integer, primary_key=True)
    user_weight = db.Column(db.String(10))
    date_of_update = db.Column(DateTime, default=datetime.utcnow)
    users_id = db.Column(db.Integer, db.ForeignKey('users.user_tg_id'))


    def __repr__(self):
        return f'''
        Ваш вес - {self.user_weight}
        '''