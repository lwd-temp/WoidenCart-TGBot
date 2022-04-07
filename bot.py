# -*- coding: utf-8 -*-
import re
from random import choice
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater,CommandHandler

updater = Updater("<YOUR TOKEN>", workers=128)
dispatcher = updater.dispatcher

class Woiden:
    @staticmethod
    def get_ua(brower_name):
        useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.30 Safari/537.36"
        return useragent

    def check(self, url):
        headers = {
            "User-Agent": self.get_ua("Safari"),
            "Content-type": "application/json",
        }
        datas = requests.get(url, headers=headers).text
        return datas

    def get_data_center(self):
        html_text = self.check("https://woiden.id/create-vps/")
        soup = BeautifulSoup(html_text, "html.parser")
        center_list = [x.text for x in soup("option", value=re.compile(r"^[A-Z]{2,}-"))]
        center_str = "\n".join(center_list)
        return center_str

    def main(self):
        vps_str = self.get_data_center()
        data_center = (
            f"[🚩Currently available data centers / 当前可开通的数据中心]\n{vps_str}\n\n"
        )
        msg = data_center
        return msg

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="欢迎使用Woiden库存查询监控bot！\n我能够帮你拿到Woiden官网上的库存信息，并把他们发送到你的Telegram会话中\n输入 /help 获取帮助列表\nGithub: Misaka-blog    TG: @misakanetcn")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Woiden 库存查询监控BOT 帮助菜单\n/help 显示本菜单\n/get 获取当前库存情况\n/ping 检测bot存活状态")

def ping(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Pong~")

def get(update, context):
    res = Woiden().main()
    context.bot.send_message(chat_id=update.effective_chat.id, text=res)

Start = CommandHandler('start', start, run_async=True)
Ping = CommandHandler('ping', ping, run_async=True)
Get = CommandHandler('get', get, run_async=True)
Help = CommandHandler('help', help, run_async=True)
dispatcher.add_handler(Ping)
dispatcher.add_handler(Start)
dispatcher.add_handler(Get)
dispatcher.add_handler(Help)

updater.start_polling()
