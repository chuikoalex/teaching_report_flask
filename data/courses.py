import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Course(SqlAlchemyBase):
    __tablename__ = 'courses'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')

    def __repr__(self):
        return f"{self.id} '{self.title}', преподаватель - {self.user_id}."
