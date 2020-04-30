from order import order
import pickle   ##write and read python objects with dat files 

class orderbook():
    def __init__(self):
        self.title = ""
        self.headers = ""
        self.asks = []
        self.seperator = ""
        self.bids = []
        self.endline = ""
        self.visualtable = ""
        self._spread = 0.0
        self._last = 0.0

    @property
    def spread(self):
        return self._spread

    @property
    def last(self):
        return self._last

    def add_order(self, order):
        if(order.mode == 'a'):
            self.asks.append(order)
        elif(order.mode == 'b'):
            self.bids.append(order)

    def add_ask(self, order):
        self.asks.append(order)     #add object end of list

    def add_bid(self, order):
        self.bids.append(order)

    def close_order(self, orderid):
        success=False
        closedorder = next((x for x in self.asks if x.id == orderid), None)     #find obj in list must check in bids and asks
        if(closedorder is not None):    ##if found
            self._last = closedorder.price
            success=True

        if(closedorder is None):    ##if order is not in asks, check in asks
            closedorder = next((x for x in self.bids if x.id == orderid), None) 
            if(closedorder is not None):
                self._last = closedorder.price
                success=True

        if(success):
            self.asks = [x for x in self.asks if x.id != orderid]       ##remove the order from asks
            self.bids = [x for x in self.bids if x.id != orderid]
        return success

    def remove_order(self, orderid, user):
        success=False
        removedorder = next((x for x in self.asks if x.id == orderid and x.name == user), None)     ##check order id and user s order
        if(removedorder is not None):
            success=True

        if(removedorder is None):
            removedorder = next((x for x in self.bids if x.id == orderid and x.name == user), None) 
            if(removedorder is not None):
                success=True

        if(success):
            self.asks = [x for x in self.asks if x.id != orderid]
            self.bids = [x for x in self.bids if x.id != orderid]
        return success

    def remove_order_admin(self, orderid):
        success=False
        removedorder = next((x for x in self.asks if x.id == orderid), None)     ##check order id and user s order
        if(removedorder is not None):
            success=True

        if(removedorder is None):
            removedorder = next((x for x in self.bids if x.id == orderid), None) 
            if(removedorder is not None):
                success=True

        if(success):
            self.asks = [x for x in self.asks if x.id != orderid]
            self.bids = [x for x in self.bids if x.id != orderid]
        return success
    
    ##make an order line in html
    def make_order_linehtml(self, order):
        line = "\t<tr>\n\t\t<th>{}</th>\n\t\t<th>{}</th>\n\t\t<th>{}</th>\n\t\t<th>{}</th>\n\t\t<th>{}</th>\n\t</tr>\n".format(order.id, order.name, order.amount, order.total, order.price)
        return line
 
    ##make order line in ascii for printing
    def make_order_line(self, order):
        orderstr = format(order.amount, ',').replace(',', ' ').replace('.', ',')
        line = "{}, {}, {}TAU, ({}$tot),   {}$".format(order.id, order.name, orderstr, order.total, order.price)
        return line

    #refresh the orderbook, last, spread, makes the orderbook visuals with ask and bid list
    def refresh(self):
        if( (len(self.asks) != 0) and (len(self.bids) != 0) ):
           self.asks.sort(key=lambda x: x.price, reverse=True)
           self.bids.sort(key=lambda x: x.price, reverse=True)
           self._spread= self.asks[-1].price - self.bids[-1].price
        else:
            self._spread = 0.0
        self.visualtable = self.title + '\n' + self.headers
        if(len(self.asks) != 0):
            for a in self.asks:
                self.visualtable+= '\n'
                self.visualtable+= self.make_order_line(a)
        self.visualtable+= '\n' + self.seperator.format(self.last, self.spread)
        if(len(self.bids) != 0):
            for b in self.bids:
                self.visualtable+= '\n'
                self.visualtable+= self.make_order_line(b)
        self.visualtable+= '\n' + self.endline

    #show the orderbook in html and saves it in html file, aslo saves orderbook data in dat
    def show(self):
        self.title =        "<table border=1>\n\t<tr>Tau Orderbook</tr>\n"
        self.headers =      "\t<tr>\n\t\t<th>ID</th>\n\t\t<th>USER@</th>\n\t\t<th>AMOUNT(TAU)</th>\n\t\t<th>TOTAL$</th>\n\t\t<th>PRICE$</th>\n\t</tr>\n"
        self.seperator =    "\t<tr>\n\t\t<th> </th>\n\t\t<th> </th>\n\t\t<th>{0}</th>\n\t\t<th> </th>\n\t\t<th>{1}</th>\n\t</tr>\n"
        self.endline =      "\t<tr> </tr>\n </table>"
        self.refresh()
        self.save_html()
        self.save_data()
        return self.visualtable

    #show orderbook in ascii and saves it in txt file, also saves orderbook data in dat
    def showascii(self):
        self.title =        "____________Tau Orderbook_____________"
        self.headers =      "ID,USER@,AMOUNT(TAU),  TOTAL$,PRICE$"
        self.seperator =    "================{}$==========={}==".format(self._last,self._spread)
        self.endline =      "______________________________________"
        self.visualtable = ""
        self.refresh()
        self.save_txt()
        self.save_data()
        return self.visualtable

    #save the orderbook data in file with pickle
    def save_data(self):
        dat = open("orderbook.dat", "w")
        pickle.dump(order.cant,dat)
        pickle.dump(self._last,dat)
        pickle.dump(self._spread,dat)
        pickle.dump(self.asks,dat)
        pickle.dump(self.bids,dat)
        dat.close()

    #load the orderbook data with pickle
    def load_data(self):
        firstorderid=0
        try:
            dat = open("orderbook.dat", "r")
            firstorderid= pickle.load(dat)
            self._last= pickle.load(dat)
            self._spread= pickle.load(dat)
            self.asks= pickle.load(dat)
            self.bids= pickle.load(dat)
            dat.close()
        except:
            pass
        return firstorderid

    #save the orderbook in txt
    def save_txt(self):
        txt = open("orderbook.txt", "w")
        txt.write(self.visualtable)
        txt.close()

    #save the orderbook in html
    def save_html(self): 
        Html_file= open("orderbook.html","w")
        Html_file.write(self.visualtable)
        Html_file.close()


            
