from datastore import customers, accounts
from models.customer import Customer
from models.account import Account

def seed_data():
    customers.clear()
    accounts.clear()

    customers.extend([
        Customer(id=1, name="Alice", email="alice@test.com", accounts=[accounts[0], accounts[1]]),
        Customer(id=2, name="David", email="david@test.com", accounts=[accounts[2]]),
        Customer(id=3, name="Zack", email="zack@test.com", accounts=[accounts[3]]),
        Customer(id=4, name="Erika", email="erika@test.com", accounts=[accounts[4]])
    ])

    accounts.extend([
        Account(id=1, account_number="1001", account_type="Checking", balance=5000, customer_id=1),
        Account(id=2, account_number="1002", account_type="Savings", balance=5000, customer_id=1),
        Account(id=3, account_number="1003", account_type="Checking", balance=10000, customer_id=2),
        Account(id=4, account_number="1004", account_type="Checking", balance=3000, customer_id=3),
        Account(id=5, account_number="1005", account_type="Savings", balance=4000, customer_id=4)
    ])