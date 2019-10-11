# coding: utf-8

import jwt
from flask import url_for, current_app
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from webapp.extensions import db


class PaginatedAPIMixin(object):
    @staticmethod
    def from_dict(cls, data, p_object=None, p_class=None, new_user=False):
        if data.json:
            data = data.json
        elif data.args:
            data = data.args
        else:
            return None

        if p_object is not None:
            my_object = p_object
        else:
            my_object = p_class()

        my_attr_dict = dict(p_class)
        my_attr_dict.remove('password_hash')

        for field in my_attr_dict:
            if field in data:
                setattr(my_object, field, data[field])

        if new_user and 'password_hash' in data:
            my_object.password_hash(data['password_hash'])

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        ressources = query.paginate(page, per_page, False)
        my_items = [item.to_dict(endpoint) for item in ressources.items]

        data = {
            'items': my_items,
            'meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': ressources.pages,
                'total_items': ressources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs)
                if ressources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs)
                if ressources.has_next else None
            }

        }
        return data

    @staticmethod
    def list_all():
        return __class__.query.all()


def commit_data():
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()


def store_data(*item):
    for i in item:
        if type(item) is not list:
            to_list = list(item)
        else:
            to_list = item
        db.session.add_all(to_list)
        commit_data()


def count(p_req):
    return db.session.query(func.count(p_req))


# Fonction same_as permet d'initialiser un default sur une colonne par rapport à une autre colonnes
def same_as(col):
    return lambda ctx: ctx.current_parameters.get(col)
