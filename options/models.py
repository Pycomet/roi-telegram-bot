## This is the object model representation for the Application
import json
from datetime import datetime as dt

class User:
    """
    This Is The Instance User Object Representation
    """

    # db_file = 'database.json'
    users = []

    def __init__(self, name, id):
        self.__name = name
        self.__id = int(id)
        self.__btc = 0
        self.__xrp = 0
        self.__is_new = True
        self.__investments = []
        self.__data_joined = str(dt.now())
        self.users.append(self)

    def __str__(self):
        val = self.__name
        return f"{val}" 

    ## Setters
    def add_btc(self, btc):
        "Add Btc"
        self.__btc += int(btc)

    def add_xrp(self, xrp):
        "Add Xrp"
        self.__xrp += int(xrp)

    def deduct_btc(self, btc):
        "Withdraw Btc"
        self.__btc -= int(btc)

    def deduct_xrp(self, xrp):
        "Withdraw Xrp"
        self.__xrp -= int(xrp)

    ## Getters
    def get_id(self):
        return "{0}".format(self.__id)

    def get_btc_balance(self):
        return "{0}".format(self.__btc)

    def get_xrp_balance(self):
        return "{0}".format(self.__xrp)

    def get_json(self):
        data = {
            "name": self.__name,
            "id": self.__id,
            "balance": {
                "btc": self.__btc,
                "xrp": self.__xrp,
            },
            "is_new": self.__is_new,
            "investments": self.__investments,
            "date_joined": self.__data_joined,
        }

        return data





    @classmethod
    def update_db(cls):
        """
        Update user informations into database
        """
        users = cls.users
        with open('database.json', 'r') as f:
            data = json.load(f)

        with open('database.json', 'w') as f:
            for user, obj in zip(users, data['users']):
                print(user, obj)

                if int(user.get_id()) == obj['id']:
                    obj.update(user.get_json())
                else:
                    data['users'].append(user.get_json())



            json.dump(data, f, indent=2)

        return "Done"
    
            


        







person = User("codeghfcgfred", 7877)
person2 = User("Coronsdsdhjh a", 55454343434)
# # print(person)

# # person.add_btc(400)

# # person.deduct_btc(2770)
# # print(person.get_btc_balance())

User.update_db()
