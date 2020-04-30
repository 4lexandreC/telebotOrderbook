from telegramBot import telegramBot
from order import order
from orderbook import orderbook    ##import classes
import telebot                     ##telebot api
import time                        ##for sleep in superloop
import subprocess                  ##supposed to call a subprocess to conver orderbook html to a jpg image 
                                   ##but didnt work with pythonanywhere web app host
                                   ##need to install wkhtmltoimage to do that

bot = telegramBot('config.cfg')     ##load token from config to my bot
bot.init_tele()                     ##use telebot with my bot class
tbot = bot.tele()
update_id = None                    ##update id if you dont use telebot api

## WITHOUT TELEBOT
#def make_reply(msg):
#    if msg is not None:
#        reply = "Okay"
#    return reply

#while True:
#    print("...")
#    updates = bot.get_updates(offset=update_id)
#    updates = updates['result']
#    if updates:
#        for item in updates:
#            update_id = item["update_id"]
#            try:
#                message = item["message"]["text"]
#            except:
#                message = None
#            from_ = item["message"]["from"]["id"]
#            reply = make_reply(message)
#            bot.send_message(reply, from_)
#    pass


timeserver = 0                  #check if server is running for superloop
ini=0                           #for superloop to initialize orderbook once
tauorderbook = orderbook()      #the orderbook

##check if string is number
def is_number(s):
    valid=False
    try: 
        float(s)
        valid=True
    except ValueError:
        valid=False
    if( (float(s) > 0) and (float(s) < 9999999) and valid ):
        valid=True
    else:
        valid=False
    return valid

##check parameters of taubot commands add
def valid_add(words):
    valid=0
    if(len(words) == 5):
        if( is_number(words[1]) and is_number(words[2]) and (words[3] == 'a' or 'b' )):
            valid=1
    else:
        valid=0
    return valid

##check parameters of taubot commands buy sell
def valid_order(words):
    valid=0
    if(len(words) == 3):
        if( is_number(words[1]) and is_number(words[2]) ):
            valid=1
    else:
        valid=0
    return valid

##check parameters of taubot commands close and del
def valid_id(words):
    valid=0
    if(len(words) == 2):
        if(is_number(words[1])):
            valid=1
    else:
        valid=0
    return valid

###check parameters of taubot for orderbook and price commands
def valid_cmd(words):
    valid=0
    if(len(words) == 1):
        valid=1
    else:
        valid=0
    return valid

##check if admin
def is_sender_admin(message):
    user = message.from_user
    chatmember = tbot.get_chat_member(message.chat.id, user.id)                      #get chat member and user group info
    if(chatmember.status == 'administrator' or chatmember.status == 'creator'):
        return True
    else:
        return False

##print orderbook in telegram chat
@tbot.message_handler(commands=['orderbook'])
def send_orderbook(message):
    words = message.text.split()        ##split the message of user example: /buy 10 1 is words[0] words[1] words[2]
    if(valid_cmd(words)):
        visualtable = tauorderbook.showascii()
        ##html to jpg orderbook
        ##subprocess.call(["xvfb-run","wkhtmltoimage", "/home/AlexandreC/tausuperbot/orderbook.html", "/home/AlexandreC/tausuperbot/orderbook.jpg"])
        ##tbot.send_photo(message.chat.id, "orderbook.jpg")
        tbot.reply_to(message, visualtable)

##buy order
@tbot.message_handler(commands=['buy'])
def send_buy(message):
    words = message.text.split()
    if(valid_order(words)):
        user = message.from_user.username    ##get @username of the sender
        amount = float(words[1])            ##string to float
        price = float(words[2])
        myorder = order(user, amount, price,'b')    ## b is buy order category
        tauorderbook.add_bid(myorder)
        tbot.reply_to(message, "user {} added order n~{} for {}TAU with price {}$ total {}$".format(user,myorder.id,amount,price,myorder.total))

##sell order
@tbot.message_handler(commands=['sell'])
def send_sell(message):
    words = message.text.split()
    if(valid_order(words)):
        user = message.from_user.username  
        amount = float(words[1])
        price = float(words[2])
        myorder = order(user, amount, price,'a')
        tauorderbook.add_ask(myorder)
        tbot.reply_to(message, "user {} added sell order n~{} for {}TAU with price {}$ total {}$".format(user,myorder.id,amount,price,myorder.total))

##admin add order
@tbot.message_handler(commands=['add'])
def send_add(message):
    words = message.text.split()
    if(valid_add(words) and is_sender_admin(message)):
        user = message.from_user.username  
        amount = float(words[1])
        price = float(words[2])
        name = str(words[3])
        mode = str(words[4])
        myorder = order(name, amount, price, mode, name)
        tauorderbook.add_ask(myorder)
        tbot.reply_to(message, "admin added order for {} with n~{} for {}TAU with price {}$ total {}$".format(user,myorder.id,amount,price,myorder.total))

#delete order by id USER S ORDER ONLY
@tbot.message_handler(commands=['del'])
def send_delete(message):
    words = message.text.split()
    user = message.from_user
    if(valid_id(words)):
        username = user.username
        orderid = int(words[1])
        if(is_sender_admin(message)):
            tauorderbook.remove_order_admin(orderid)
            tbot.reply_to(message, "admin deleted order n~{}".format(orderid))
        elif(tauorderbook.remove_order(orderid,user)):
            tbot.reply_to(message, "user {} deleted order n~{}".format(username,orderid))

#close order by id ADMIN ONLY
@tbot.message_handler(commands=['close'])
def send_close(message):
    words = message.text.split()
    user = message.from_user        #get the user 
    chatmember = tbot.get_chat_member(message.chat.id, user.id)                      #get chat member and user group info
    if(chatmember.status == 'administrator' or chatmember.status == 'creator'):     #admin or creator
        if(valid_id(words)):
            username = user.username
            orderid = int(words[1])
            if(tauorderbook.close_order(orderid)):
                tbot.reply_to(message, "user {} closed his order n~{} TAU LAST PRICE {}$".format(username,orderid,tauorderbook._last))

##check orderbook last price
@tbot.message_handler(commands=['price'])
def send_price(message):
    words = message.text.split()
    if(valid_cmd(words)):
        last = tauorderbook.last
        tbot.reply_to(message, 'Tau Last Price: {}$'.format(last))

##load orderbook dat files, get ask and bid list, spread, last price and id so order id doesnt have duplicated when restarting the bot
def initorders():
    order.cant = tauorderbook.load_data()

##superloop
while True:
    if (ini==0):
        initorders()
        ini=1
    timeserver+=1
    print("server running ", timeserver)
    try:
        tbot.polling()
    except Exception:
        time.sleep(15)