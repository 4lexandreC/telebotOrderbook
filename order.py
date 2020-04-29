
class order(object):
    cant=0  #class var
    def __init__(self, name, amount, price, mode):
        order.cant+=1       #class var increment
        self._id = order.cant       #attribute with _ because its a @property
        self._name = name
        self._amount = amount
        self._price = price
        self._total = price*amount
        self._mode = mode            #bid or ask mode

    ##getters and setters
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self,amount):
        self._amount = amount
    
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self,price):
        self._price = price 

    @property
    def total(self):
        return self._total

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self,mode):
        self._mode = mode 

    @property
    def id(self):
        return self._id
