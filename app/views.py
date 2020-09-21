from flask import (
    redirect,
    url_for,
)


from app import r
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView, ModelRestApi

from . import appbuilder, db
from app.models import Contact, ContactGroup, RedisValue

from flask import request, session, flash, redirect, url_for
from app import app, celery, db

import logging


db.create_all()


class RedisView(ModelView):

    route_base = "/redis-values"
    datamodel = SQLAInterface(RedisValue)
    list_columns = [
        "get_value",
        "get_key",
    ]

    add_columns = [
        "key",
        "value",
    ]

    edit_columns = add_columns

    def pre_add(self, obj):
        r.set(obj.key, obj.value)

    def pre_update(self, obj):
        self.pre_add(obj)

    # def post_edit_redirect(self):
    #     return redirect(url_for("RedisView.list"))

    # def post_delete_redirect(self):
    #     return redirect(url_for("RedisView.list"))

    # def post_add_redirect(self):
    #     return redirect(url_for("RedisView.list"))


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)


class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    label_columns = {"contact_group": "Contacts Group"}
    list_columns = ["name", "personal_cellphone", "birthday", "contact_group"]

    show_fieldsets = [
        ("Summary", {"fields": ["name", "address", "contact_group"]}),
        (
            "Personal Info",
            {
                "fields": ["birthday", "personal_phone", "personal_cellphone"],
                "expanded": False,
            },
        ),
    ]


appbuilder.add_view(ContactModelView(), "Contact")
appbuilder.add_view(GroupModelView(), "Group")
appbuilder.add_view(RedisView(), "kd")
