from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship

from slugify import slugify  # among other things
from sqlalchemy import CheckConstraint

from app import r


# class RedisValue(Model):

#     """
#     redis
#     """

#     id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
#     key = Column(String(256), nullable=False)
#     value = Column(String(256), nullable=False)

#     @property
#     def get_value(self):
#         return r.get(self.key)

#     @property
#     def get_key(self):
#         return self.key

#     def __repr__(self):
#         return self.key


# class ContactGroup(Model):
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), unique=True, nullable=False)

#     def __repr__(self):
#         return self.name


# class Contact(Model):
#     id = Column(Integer, primary_key=True)
#     name = Column(String(150), unique=True, nullable=False)
#     address = Column(String(564), default="Street ")
#     birthday = Column(Date)
#     personal_phone = Column(String(20))
#     personal_cellphone = Column(String(20))
#     contact_group_id = Column(Integer, ForeignKey("contact_group.id"))
#     contact_group = relationship("ContactGroup")

#     def __repr__(self):
#         return self.name

class Product(Model):

    stock = Column(Integer)

    __table_args__ = (
        CheckConstraint(stock >= 0, name='check_stock_positive'),
        {})

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)

    slug = Column(String(255))

    description = Column(String(255))
    price = Column(Float)
    
    def __init__(self, *args, **kwargs):
        if not 'id' in kwargs:
            kwargs['id'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)
    
    def __repr__(self):
        return self.id


class Location(Model):

    def __init__(self, *args, **kwargs):
        if not 'id' in kwargs:
            kwargs['id'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)

    def __repr__(self):
        return self.id




class ProductMovement(Model):
    """

    ProductMovement table fields 
    movement_id, timestamp, from_location, to_location, product_id, qty

    Primary key can be text / varchar that's why id is varchar field.
     
    """

    __table_args__ = (
        CheckConstraint(qty >= 0, name='check_qty_positive'),
        {})


    def __init__(self, *args, **kwargs):
        if not 'id' in kwargs:
            kwargs['id'] = slugify(kwargs.get('name', ''))
        super().__init__(*args, **kwargs)

    id = Column(Integer, primary_key=True)
    

    from_location_id = Column(Integer, ForeignKey("from_location.id"))
    from_location = relationship("Location")

    to_location_id = Column(Integer, ForeignKey("to_location.id"))
    to_location = relationship("Location")

    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product")

    qty = Column(Integer)

    def __repr__(self):
        return self.id
