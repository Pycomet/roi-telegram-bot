## This is the object model representation for the Application

class Account:
    """
    This is the mina user onject representation
    """

    def __init__(self, name):
        self.__name = name
        self.__btc = 0
        self.__xrp = 0

    def __str__(self):
        return f"{self.__name}"

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
    def get_btc_balance(self):
        "Receive balance"
        return f"{self.__btc}"

    def get_xrp_balance(self):
        return f"{self.__xrp}"




person = Account(name="codefred")

print(person)

person.add_btc(400)

person.deduct_btc(20)
print(person.get_btc_balance())


