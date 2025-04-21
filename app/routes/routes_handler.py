from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session
from ..models.model import Product, db
from flask import jsonify
from ..extension.utils import message_handler, role_required
from functools import wraps


def session_handler() -> Session:
  with db.session() as session:
    return session

def pagnation_handler(_page=1, _per_page=5):
    pagination = Product.query.paginate(
      page=_page,
      per_page=_per_page
    )
    products = pagination.items
    result = {
          'products': [p.to_dict() for p in products],  # you must define `to_dict()` in your model
          'total': pagination.total,
          'page': pagination.page,
          'per_pages': pagination.per_page
      }
    return result

def search_handler(*args):
    prod = session_handler().query(Product).all()
    result = [d.to_dict() for d in prod if d.to_dict()[args[0]].lower() == args[1].lower()]
    return jsonify(message_handler(f'Details of product {dict({args[0].capitalize():args[1]})}', result))


def func_wraper_handler(bp, method="GET", route_="/"):
  def decorator(f):
    @wraps(f)
    @bp.route(route_, methods=[method])
    @role_required('user', 'admin')
    @jwt_required() 
    def wraped(*args, **kwargs):
      return f(*args, **kwargs)
    return wraped
    
  return decorator