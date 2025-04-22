from flask_jwt_extended import jwt_required
from sqlalchemy.orm import Session
from ..models.model import Product, db
from flask import jsonify
from .utils import message_handler, role_required
from functools import wraps
from .. import limiter

# Function to obtain a database session.
# This function uses the SQLAlchemy session context manager to ensure proper session handling.
def session_handler() -> Session:
    with db.session() as session:
        return session

# Function to handle pagination for Product queries.
# It paginates the results based on the page number and items per page,
# and returns a dictionary containing product details, pagination details, and metadata.
def pagnation_handler(_page=1, _per_page=5):
    pagination = Product.query.paginate(
        page=_page,
        per_page=_per_page
    )
    products = pagination.items
    result = {
        'products': [p.to_dict() for p in products],  # `to_dict()` must be defined in the Product model to serialize objects.
        'total': pagination.total,
        'page': pagination.page,
        'per_pages': pagination.per_page
    }
    return result

# Function to handle product searches.
# It queries the database for all products and filters the results based on the provided arguments.
# The function returns a JSON response containing the filtered product details.
def search_handler(*args):
    prod = session_handler().query(Product).all()
    result = [d.to_dict() for d in prod if d.to_dict()[args[0]].lower() == args[1].lower()]
    return jsonify(message_handler(f'Details of product {dict({args[0].capitalize():args[1]})}', result))

# Function to create a route with custom behavior.
# This is a decorator function that wraps a given view function `f`.
# It applies additional decorators for route handling, role-based access control, and JWT authentication.
# Parameters:
# - `bp`: The Flask Blueprint to register the route.
# - `method`: The HTTP method for the route (default is "GET").
# - `route_`: The route path (default is "/").
def func_wraper_handler(bp, method="GET", route_="/", sec="2"):
    def decorator(f):
        @wraps(f)
        @bp.route(route_, methods=[method])
        @limiter.limit(f"{sec} per seconds")
        @role_required('user', 'admin')  # Restrict access to users with 'user' or 'admin' roles.
        @jwt_required()  # Require JWT authentication for the route.
        def wraped(*args, **kwargs):
            return f(*args, **kwargs)
        return wraped

    return decorator