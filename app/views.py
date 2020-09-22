from flask import (
    redirect,
    url_for,
)

from wtforms.fields import TextField

from app import r
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db
from app.models import (
    # Contact,
    # ContactGroup,
    # RedisValue,
    Location,
    Product,
    ProductMovement,
)

from flask import request, session, flash, redirect, url_for
from app import app, celery, db
from flask_babel import gettext

import logging
from flask_appbuilder.models.sqla.filters import FilterStartsWith


db.create_all()


class LocationModelView(ModelView):
    datamodel = SQLAInterface(Location)


class ProductModelView(ModelView):
    datamodel = SQLAInterface(Product)


from flask_appbuilder.fieldwidgets import BS3TextFieldWidget


class BS3TextFieldROWidget(BS3TextFieldWidget):
    def __call__(self, field, **kwargs):
        kwargs["readonly"] = "true"
        return super(BS3TextFieldROWidget, self).__call__(field, **kwargs)


class ProductMovementModelView(ModelView):
    datamodel = SQLAInterface(ProductMovement)

    # list_columns = [
    # "from_location_id",
    # "to_location",
    # "product",
    # "current_location",
    # ]
    # add_columns = [
    #     "current_location",

    # ]
    # add_form_extra_fields = {
    #     'field2': TextField('field2', widget=BS3TextFieldROWidget())
    # }
    add_form_extra_fields = {
        "extra": TextField(
            gettext("Extra Field"),
            description=gettext("Extra Field description"),
            widget=BS3TextFieldWidget(),
        )
    }
    # add_columns = ['product', 'field2']
    # add_form_query_rel_fields = {
    #     'group': [['name', FilterStartsWith, 'W']],
    #     'gender': [['name', FilterStartsWith, 'M']]
    # }

    def pre_add(self, obj):
        obj.from_location = obj.product.current_location

    # edit_columns = add_columns


appbuilder.add_view(ProductModelView(), "Products")
appbuilder.add_view(ProductMovementModelView(), "Product Movements")
appbuilder.add_view(LocationModelView(), "Warehouses")
