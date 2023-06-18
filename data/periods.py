import sqlalchemy

from .db_session import SqlAlchemyBase


class Period(SqlAlchemyBase):
    __tablename__ = 'periods'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
