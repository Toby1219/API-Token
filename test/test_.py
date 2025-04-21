from app import create_app, db
from app.extension.to_sql import json_to_sql

app = create_app()
with app.app_context():
    db.create_all()
    json_to_sql()
header ={}

def test_reg():
    with app.test_client() as client:
        response = client.post("/auth/register", json={"username":"test1", "password":"122345"})
        assert response.status_code == 201 or response.status_code == 409
        
def test_login():
    with app.test_client() as client:
        response = client.post("/auth/login", json={"username":"test1", "password":"122345"})
        token = response.get_json()['data']['token']
        header["Authorization"] = f'Bearer {token}'
        assert response.status_code == 200
        
def test_whoami():
    with app.test_client() as client:
        response = client.get("/auth/whoami", headers=header)
        assert response.status_code == 200

def test_route_home_guest():
    with app.test_client() as client:
        response = client.get("/api/guest/product", headers=header)
        assert response.status_code == 200
        
def test_route_home_user():
    with app.test_client() as client:
        response = client.get("/api/product/all", headers=header)
        assert response.status_code == 200
        
def test_route_id():
    with app.test_client() as client:
        response = client.get("/api/product/id", headers=header)
        assert response.status_code == 200
        
def test_route_price():
    with app.test_client() as client:
        response = client.get("/api/product/price", headers=header)
        assert response.status_code == 200
        
def test_route_search():
    with app.test_client() as client:
        response = client.get("/api/product/search", headers=header)
        assert response.status_code == 200
        
def test_route_searchQ():
    with app.test_client() as client:
        response = client.get("/api/product/search_t=Wooden%20Bathroom%20Sink%20With Mirror", headers=header)
        assert response.status_code == 200
    
def test_log():
    with app.test_client() as client:
        response = client.post("/auth/login", json={"username":"test1", "password":"122345"})
        assert response.status_code == 200 or response.status_code == 409

    