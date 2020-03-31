## This is the object model representation for the Application

class User:
    """
    This is the mina user onject representation
    """

    data = []

    def __init__(self, name, id):
        self.__name = name
        self.__id = int(id)
        self.__btc = 0
        self.__xrp = 0
        self.data.append(self)

    def __str__(self):
        return "{0}".format(self.__name)  

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

    @classmethod
    def get_user(cls, num):
        "Get user object from id"
        target = cls.data

        for i in range(len(target)):
            if num == target[i].__id:
                return target[i]
        return None







# person = User("codefred", 7877)
# import pdb; pdb.set_trace()
# print(person)

# person.add_btc(400)

# person.deduct_btc(20)
# print(person.get_btc_balance())


