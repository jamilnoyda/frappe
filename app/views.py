from flask import (
    redirect,
    url_for,
)

from wtforms.fields import TextField

from app import r
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView

from . import appbuilder, db
from app.models import (
    Location,
    Product,
    ProductMovement,
)

from flask import request, session, flash, redirect, url_for
from app import app, celery, db
from flask_babel import gettext

import logging
from flask_appbuilder.models.sqla.filters import FilterStartsWith
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget


db.create_all()


class LocationModelView(ModelView):
    datamodel = SQLAInterface(Location)


class ProductModelView(ModelView):
    datamodel = SQLAInterface(Product)

    list_columns = [
        # "from_location_id",
        "name",
        "stock",
        "current_location",
        "price",
        "total_price",
    ]


class BS3TextFieldROWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs["readonly"] = "true"
        return super(BS3TextFieldROWidget, self).__call__(field, **kwargs)


class ProductMovementModelView(ModelView):
    datamodel = SQLAInterface(ProductMovement)

    list_columns = [
        # "from_location_id",
        "to_location",
        "product",
        "current_location",
    ]
    # add_columns = [
    #     "current_location",

    # ]

    add_form_extra_fields = {
        "from_location": TextField(
            "from_location will be added from current product location",
            widget=BS3TextFieldROWidget(),
        )
    }
    add_columns = ["product", "to_location", "from_location", "qty"]

    edit_columns = add_columns

    def pre_add(self, obj):
        obj.from_location = obj.product.current_location
        if obj.from_location == obj.to_location:
            raise Exception("can't be same to and from location")

        if obj.qty > obj.product.stock:
            raise Exception("qty(stock) is not available ")
        obj.product.stock = obj.product.stock - obj.qty
        # import pdb; pdb.set_trace()
        instance = (
            db.session.query(Product)
            .filter_by(id=obj.product.id, current_location_id=obj.to_location.id)
            .first()
        )
        if instance:
            instance.stock = instance.stock + obj.qty
            db.session.add(instance)

        else:
            # print('eyese')
            instance = Product(
                **{
                    "name": obj.product.name,
                    "current_location_id": obj.to_location.id,
                    "stock": obj.qty,
                    "price": obj.product.price,
                }
            )
            db.session.add(instance)

    def pre_edit(self, obj):
        return self.pre_add(obj)

    edit_columns = add_columns


appbuilder.add_view(ProductModelView(), "Products")
appbuilder.add_view(ProductMovementModelView(), "Product Movements")
appbuilder.add_view(LocationModelView(), "Warehouses")
