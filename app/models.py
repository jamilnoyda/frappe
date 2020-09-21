from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


from app import r


class RedisValue(Model):

    """
    redis
    """

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    key = Column(String(256), nullable=False)
    value = Column(String(256), nullable=False)

    @property
    def get_value(self):
        return r.get(self.key)

    @property
    def get_key(self):
        return self.key

    def __repr__(self):
        return self.key


class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564), default="Street ")
    birthday = Column(Date)
    personal_phone = Column(String(20))
    personal_cellphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey("contact_group.id"))
    contact_group = relationship("ContactGroup")

    def __repr__(self):
        return self.name