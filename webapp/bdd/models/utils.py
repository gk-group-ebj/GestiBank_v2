from flask import url_for
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from webapp.extensions import db


class PaginatedAPIMixin(object):
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
                'next': url_for(endpoint, page=page+1, per_page=per_page, **kwargs)
                    if ressources.has_next else None,
                'prev': url_for(endpoint, page=page-1, per_page=per_page, **kwargs)
                    if ressources.has_next else None
            }

        }
        return data

    @staticmethod
    def populate(* args):
        db.session.add_all()

        try:
            db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()

    @staticmethod
    def list_all():
        return __class__.query.all()

    @staticmethod
    def count(p_req):
        return db.session.query(func.count(p_req))

# Fonction same_as permet d'initialiser un default sur une colonne par rapport à une autre colonnes
same_as = lambda col: lambda ctx: ctx.current_parameters.get(col)
