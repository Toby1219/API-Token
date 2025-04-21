from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def write_jsons(v, path='./instance/tokens.json'):
    import json
    with open(f"{path}", "w") as f:
        json.dump(v, f, indent=2)

def reader(path):
    import json
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except:
        return None

def update_jsons(v):
    datas = reader()
    datas['data']['token'] = v
    write_jsons(datas)


def message_handler(*args:tuple[str, list[dict]], ok:bool=True, write=False)->dict:
    response = {
        "status":"sucess" if ok else "Error",
        "message":args[0],
        "data": args[1],
        "count": len(args[1]) if ok else 0
    }
    if write:
        write_jsons(response)
    return response


def token_times(payload):
    from datetime import datetime
    claims = payload()
    issued_at = datetime.fromtimestamp(claims["iat"]).strftime("%Y-%m-%d %H:%M:%S")
    exp_time = datetime.fromtimestamp(claims["exp"]).strftime("%Y-%m-%d %H:%M:%S")
    return issued_at, exp_time

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify(message_handler(f"Access denied: {claims.get("role")}", 
                                               '', ok=False)), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


