from datastore import customers, accounts
from models.customer import Customer
from models.account import Account

def seed_data():
    customers.clear()
    accounts.clear()

    accounts.append(Account(id=1, account_number="1001", account_type="Checking", balance=5000, customer_id=1)),
    accounts.append(Account(id=2, account_number="1002", account_type="Savings", balance=5000, customer_id=1)),
    accounts.append(Account(id=3, account_number="1003", account_type="Checking", balance=10000, customer_id=2)),
    accounts.append(Account(id=4, account_number="1004", account_type="Checking", balance=3000, customer_id=3)),
    accounts.append(Account(id=5, account_number="1005", account_type="Savings", balance=4000, customer_id=4))

    customers.append(Customer(id=1, name="Alice", email="alice@test.com", accounts=[1001, 1002])),
    customers.append(Customer(id=2, name="David", email="david@test.com", accounts=[1003])),
    customers.append(Customer(id=3, name="Zack", email="zack@test.com", accounts=[1004])),
    customers.append(Customer(id=4, name="Erika", email="erika@test.com", accounts=[1005]))