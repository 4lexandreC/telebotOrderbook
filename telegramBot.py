import requests
import json
import configparser as cfg
import telebot

##telegram bot class, without telebot you have to make the methods, 
##init tele makes this class a bit useless
class telegramBot():

        def __init__(self, config):
                self.token = self.read_token(config)
                self.base = "https://api.telegram.org/bot{}/".format(self.token)

        def init_tele(self):
                self.tbot = telebot.TeleBot(token=self.token)
        
        def tele(self):
                return self.tbot

        ## execute https://api.telegram.org/bot{token here}/getUpdates?timeout=100
        def get_updates(self, offset=None):
                url = self.base + "getUpdates?timeout=100"
                if offset:
                        url = url + "&offset={}".format(offset + 1)
                r = requests.get(url)
                return json.loads(r.content)

        def send_message(self, msg, chat_id):
                url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
                if msg is not None:
                        requests.get(url)

        def read_token(self, config):
                parser = cfg.ConfigParser()
                parser.read(config)
                return parser.get('creds', 'token')
