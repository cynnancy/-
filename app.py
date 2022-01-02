from typing import Text
from bs4.element import TemplateString
from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
from other_function import top_pawn, get_juridical_person, stock_dic, next_day_over_buy, next_day_over_sell
from news import news_carousel


#======這裡是呼叫的檔案內容=====
#from message import *
#from new import *
#from Function import *
from news import *
#======這裡是呼叫的檔案內容=====

#======python的函數庫==========
import tempfile, os
import datetime
import time
import pandas as pd
import time as t
import requests
import time as t
from urllib.parse import urljoin
#======python的函數庫==========
import re
from bs4 import BeautifulSoup

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# Channel Access Token 
#這行初始化了一個 LineBotApi的物件，該物件有一個方法reply_message
line_bot_api = LineBotApi('Acess Token')

# Channel Secret
handler = WebhookHandler('Channel Secret')

#佈署好自動推播訊息
#user_id
line_bot_api.push_message('User ID', TextSendMessage(text ='哈囉歡迎加入，輸入「幫助」獲取更多指令訊息'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


#line_bot_api.reply_message(*參數一,*參數二) 接收到其他 LINE 使用者的時候回覆信息
#參數一: reply_token 其他使用者傳送信息給機器人，產生一個reply_token
#參數二: TextSendMessage(text=event.message.text)
#line_bot_api.reply_message(欲回傳者的 token, 回傳的訊息)

#處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text #使用者傳入訊息
    emoji = [
        {
            "index": 10,
            "productId": "5ac1bfd5040ab15980c9b435",
            "emojiId": "038" #>_<_rabbit
        },
        {
            "index": 29,
            "productId": "5ac1bfd5040ab15980c9b435",
            "emojiId": "079" #nervous_chicken
        },
        {
            "index": 44,
            "productId": "5ac22775040ab15980c9b44c",
            "emojiId": "054" #money_cat
        },
    ]         
    
    if re.match("幫助", msg):
        message = "輸入「前五大」獲取前一交易日當沖交易量前五名之股票資訊\n\n輸入「新聞 股票名稱」獲取該個股相關新聞\n\n輸入「賣超 股票名稱」獲取前一交易日隔日沖券商賣超資訊\n\n輸入「買超 股票名稱」獲取前一交易日隔日沖券商買超資訊\n\n輸入「三大法人 個股名稱」獲取該股前一交易日三大法人資訊"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = message))

    elif re.match("前五大", msg):
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="前五大", contents = top_pawn(event)))

    elif re.match("新聞", msg[:2]):
        stock = msg[3:]
        message = TemplateSendMessage(alt_text="新聞", template=CarouselTemplate(columns = news_carousel(stock), image_aspect_ratio=None, image_size=None))
        line_bot_api.reply_message(event.reply_token, message)

    elif re.match("賣超", msg[:2]):
        if msg[3:] in stock_dic:
            stock = msg[3:]
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="隔日沖券商賣超", contents= next_day_over_sell(stock)))

        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="股票名稱輸入錯誤，請重新輸入"))

    elif re.match("買超", msg[:2]):
        if msg[3:] in stock_dic:
            stock = msg[3:]
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="隔日沖券商買超", contents= next_day_over_buy(stock)))

        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="股票名稱輸入錯誤，請重新輸入"))

    elif re.match("三大法人", msg[:4]):
        if msg[5:] in stock_dic:
            stock = msg[5:]
            line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text = "三大法人", contents = get_juridical_person(stock)))
            
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="股票名稱輸入錯誤，請重新輸入"))

    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "感謝您傳送訊息給我!$\n很抱歉，我沒有辦法對用戶個別回覆。$\n\n敬請期待下次的訊息內容!$", emojis=emoji))

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
