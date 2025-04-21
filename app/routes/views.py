from flask import Blueprint, request, jsonify
from ..extension.utils import message_handler
from ..models.model import Product
from .routes_handler import *

w_bp = Blueprint('w_bp', __name__)
  
@w_bp.route('/guest/product', methods=['GET'])
def home_guest():
  prod = session_handler().query(Product).all()
  result = [d.to_dict() for d in prod]
  return jsonify([message_handler("Products API <Current user(guest)>", result[:10])]), 200
   
@func_wraper_handler(bp=w_bp, route_='/product/all')
def home_user():
  _page = request.args.get("page", default=1, type=int)
  _per_page = request.args.get("per_page", default=5, type=int)
  return pagnation_handler(_page, _per_page)

@func_wraper_handler(bp=w_bp, route_="/product/id")
def product_id():
  pram = request.args.get("", default="1", type=str)
  prod = session_handler().query(Product).all()
  if pram: 
    clean_ids = [x.strip() for x in pram.split(",")]
    valid_ids = []
    for _id in clean_ids:
        if not _id.isdigit():
            return jsonify([message_handler(f"Invalid ID: '{_id}'. IDs must be integers.", "", ok=False)]), 400
        valid_ids.append(int(_id))
    results = [d.to_dict() for d in prod if d.to_dict()["id"] in valid_ids]
    if not results:
        return jsonify([message_handler("No products found for the provided IDs.", "", ok=False)]), 404
    return jsonify([message_handler("products IDs", results)]), 200 
  
  return jsonify([message_handler("Missing 'id' parameter", "", ok=False)]), 400

@func_wraper_handler(bp=w_bp, route_="/product/price")
def product_price():
    # get and sort price and sort if as
    parm = request.args.get("sort", default='true', type=str)
    prod = session_handler().query(Product).all()
    if parm != None and parm in ["true", "asec"]:
        result = sorted([d.to_dict() for d in prod], key=lambda x: x["price"], reverse=False)
        return jsonify([message_handler("Price in asecending order", result)])
    elif parm !=  None and parm in ["false", "desec"]:
        result = sorted([d.to_dict() for d in prod], key=lambda x: x["price"], reverse=True)
        return jsonify([message_handler("Price in descending order", result)])
    else:
        return jsonify([message_handler("Error invald url", "", ok=False)])

@func_wraper_handler(bp=w_bp, route_="/product/search")
def search_():
  pram = request.args.get('', default='all')
  if pram == "all":
    return pagnation_handler()

@func_wraper_handler(bp=w_bp, route_="/product/search_<string:val>=<string:val2>")
def search_query(val, val2):
  if val in 'title':
    val = 'title'
    return search_handler(val, val2) 
  elif val in 'sku':
    val = 'sku'
    return search_handler(val, val2)
  elif val in 'category':
    val = 'category'
    return search_handler(val, val2)
  else:
    return jsonify(message_handler(f"Invalid URl {request.url}", "", ok=False)) 
 

  
  