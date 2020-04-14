import random
import hashlib
import logging
import json
import time
from enum import Enum

class Role(Enum):
    admin = 0
    cashier = 1

class Session:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def main_dialogue(self):
        pass

    def load_coffee_types(self):
        return load_db('coffee_types.txt')

    def load_records(self):
        return load_db('records.txt')

    def dump_records(self, db):
        return dump_db('records.txt', db)

class AdminSession(Session):
    def __init__(self, name):
        super(AdminSession, self).__init__(name, Role.admin)


    def main_dialogue(self):
        print("\n=====Welcome, admin=====")
        while True:
            print('\nChoose action')
            response = input("Register new user(1)\nShow records(2)\nShow coffee types and prices(3)\nExit(else)\n")
            if response == '1':
               self.register_prompt()
            elif response == '2':
                self.show_records()
            elif response == '3':
                self.show_coffee()
            else:
                break

    def register_prompt(self):
        name = input("Name: ").strip()
        passwd = input("Password: ").strip()
        role = input("Role: admin(1) or cashier(else) ").strip()
        if role == '1':
            role_enum = Role.admin
        else:
            role_enum = Role.cashier
        self.execute_register((name, passwd, role_enum.value))
        print("Done")

    def execute_register(self, credentials):
        db = load_logins()
        name, password, role = credentials
        salt = generate_salt()
        db.append((name, hashlib.md5((password + salt).encode()).hexdigest(), salt, role))
        dump_logins(db)

    def show_records(self):
        print('\nHere are all the records. Yup, no sorting or something, sorrie')
        print(self.load_records())

    def show_coffee(self):
        print('\nHere are all the coffees')
        print(self.load_coffee_types())

class CashierSession(Session):
    def __init__(self, name):
        super(CashierSession, self).__init__(name, Role.cashier)

    def main_dialogue(self):
        print("\n=====Welcome, cashier=====")
        while True:
            print('\nChoose action')
            response = input("New order(1)\nExit(else)\n").strip()
            if response == '1':
                self.new_order_dialogue()
            else:
                break
        return


    def new_order_dialogue(self):
        print("\nNEW ORDER!!!")
        order = list()
        cost = 0
        coffee_types = self.load_coffee_types()
        while True:
            print("\nChoose coffee type:")
            for i in range(len(coffee_types)):
                print(coffee_types[i][0], '({})'.format(i))
            if len(order) == 0:
                print('Cancel (else) ')
            else:
                print('That''s it (else) ')

            coffee_name = input()
            if coffee_name.isdigit() and int(coffee_name) < len(coffee_types):
                str_count = input('Amount? (else = 1)\n')
                if str_count.isdigit():
                    count = int(str_count)
                else:
                    count = 1
                order.append((count, coffee_types[int(coffee_name)][0], count))
                cost += coffee_types[int(coffee_name)][1]
            elif len(order) == 0:
                return
            else:
                break

        print("Final order:", order, 'Cost:', cost)
        print("Confirm?\nYes (nothing)\nNo (else)")
        answer = input()
        if answer == '':
            print('Confirmed')
            self.record_order(order)
        else:
            return

    def record_order(self, order):
        records = self.load_records()
        records.append([time.asctime(), self.name, order])
        self.dump_records(records)

def load_logins():
    return load_db('logins.txt')

def dump_logins(db):
    return dump_db('logins.txt', db)

def dump_db(name, db):
    f = open(name, 'wt')
    json.dump(db, f)
    f.close()

def load_db(name):
    f = open(name, 'rt')
    db = json.load(f)
    f.close()
    return db

def generate_salt():
    return format(random.getrandbits(128), 'x')

def execute_login(credentials):
    db = load_logins()
    name, password = credentials
    for record in db:
        if name == record[0]:
            if hashlib.md5((password + record[2]).encode()).hexdigest() == record[1]:
                print("Access granted")
                if record[3] == Role.admin.value:
                    return AdminSession(name)
                else:
                    return CashierSession(name)
            else:
                print("Access denied")
                return None
    print("No such user")
    return None

def login_prompt():
    name = input("Name: ")
    passwd = input("Password: ")
    session = execute_login((name, passwd))
    return session

if __name__ == '__main__':
    session = login_prompt()
    if session == None:
        exit()
    session.main_dialogue()


