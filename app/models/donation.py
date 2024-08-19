from sqlalchemy import Column, Integer, ForeignKey, Text
from app.models.base import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
