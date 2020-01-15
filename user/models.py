import datetime
from sqlalchemy import Column, Integer, String, DateTime
from core.database import Base
from core.models import ModelMixin


class User(ModelMixin, Base):
    __tablename__ = 'user_users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
