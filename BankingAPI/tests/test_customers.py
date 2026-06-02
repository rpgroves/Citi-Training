from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# get all customers
def test_get_all_customers():
    response = client.get("/api/customers")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

# get customers by name
def test_get_customer_by_name_not_found():
    response = client.get("/api/customers/search?name=NonExistent")

    assert response.status_code == 404

# get premium customers
def test_get_premium_customers():
    response = client.get("/api/customers/premium")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

# get customers by id
def test_get_customer_by_id_not_found():
    response = client.get("/api/customers/999")

    assert response.status_code == 404

# create customer
#def test_create_customer():
#def test_create_customer_invalid():

# update customer
#def test_update_customer():
#def test_update_customer_invalid():
#def test_update_customer_not_found():

# delete customer
#def test_delete_customer():
#def test_delete_customer_not_found():
#def test_update_customer_invalid():


