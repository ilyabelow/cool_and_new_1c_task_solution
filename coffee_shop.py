import random
import hashlib
import logging
import json
from enum import Enum

class Role(Enum):
    admin = 0
    cashier = 1

class Session:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def dialogue(self):
        pass

class AdminSession(Session):
    def __init__(self, name):
        super(AdminSession, self).__init__(name, Role.admin)


    def dialogue(self):
        print("Welcome, admin")
        while True:
            response = input("Register new user(1) \nExit(else) ")
            if response == '1':
               self.register_prompt()
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
        with open('logins.txt', 'w') as logins_file:
            json.dump(db, logins_file)

class CashierSession(Session):
    def __init__(self, name):
        super(CashierSession, self).__init__(name, Role.cashier)

    def dialogue(self):
        print("Sorry, ya can do notin' yet")
        response = input("Exit(else)")
        return



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

def load_logins():
    logins_file = open('logins.txt')
    logins_db = json.load(logins_file)
    logins_file.close()
    return logins_db

def login_prompt():
    name = input("Name: ").strip()
    passwd = input("Password: ").strip()
    session = execute_login((name, passwd))
    return session

if __name__ == '__main__':
    session = login_prompt()
    if session == None:
        exit()
    session.dialogue()


