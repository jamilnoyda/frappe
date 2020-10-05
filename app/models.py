from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship

from slugify import slugify  # among other things
from sqlalchemy import CheckConstraint
from flask_appbuilder.models.decorators import renders

# from app import r
from flask import Markup


class Product(Model):
    __tablename__ = "product"

    stock = Column(Integer)

    __table_args__ = (CheckConstraint(stock >= 0, name="check_stock_positive"), {})

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    # slug = Column(String(255))

    # description = Column(String(255))
    price = Column(Float)
    current_location_id = Column(Integer, ForeignKey("location.id"), nullable=False)

    current_location = relationship("Location", foreign_keys=[current_location_id])

    # def __init__(self, *args, **kwargs):
    #     if not 'id' in kwargs:
    #         kwargs['id'] = slugify(kwargs.get('name', ''))
    #     super().__init__(*args, **kwargs)

    def __repr__(self):

        '''
        name, location and available stock
        '''
        return self.name+'-'+self.current_location.name+', stock: '+ str(self.stock)

    def total_price(self):
        return self.price * self.stock


class Location(Model):
    __tablename__ = "location"

    # def __init__(self, *args, **kwargs):
    #     if not 'id' in kwargs:
    #         kwargs['id'] = slugify(kwargs.get('name', ''))
    #     super().__init__(*args, **kwargs)

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class ProductMovement(Model):

    """

    ProductMovement table fields
    movement_id, timestamp, from_location, to_location, product_id, qty

    Primary key can be text / varchar that's why id is varchar field.

    """

    __tablename__ = "product_movement"

    qty = Column(Integer)

    __table_args__ = (CheckConstraint(qty >= 0, name="check_qty_positive"), {})

    # def __init__(self, *args, **kwargs):
    #     if not 'id' in kwargs:
    #         kwargs['id'] = slugify(kwargs.get('name', ''))
    #     super().__init__(*args, **kwargs)

    id = Column(Integer, primary_key=True)

    from_location_id = Column(Integer, ForeignKey("from_location.id"))
    from_location = relationship("Location")

    to_location_id = Column(Integer, ForeignKey("to_location.id"))
    to_location = relationship("Location")

    product_id = Column(Integer, ForeignKey("product.id"))
    product = relationship("Product")

    from_location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location_id = Column(Integer, ForeignKey("location.id"), nullable=False)
    to_location = relationship("Location", foreign_keys=[to_location_id])

    def __repr__(self):
        return self.product.name

    def current_location(self):
        if self.product:

            return self.product.current_location.name
        else:
            return "None"

    # def get_or_create(session, model, defaults=None, **kwargs):
