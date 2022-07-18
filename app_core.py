from __future__ import unicode_literals
from datetime import datetime
from email import message
import os
import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

import configparser

import random

app = Flask(__name__)

# LINE 聊天機器人的基本資料
#config = configparser.ConfigParser()
#config.read('config.ini')

#line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
#handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
line_bot_api = LineBotApi("K1emrUH+v/Ck1vOYJAHW34ebQybv4f6c6FneFyAp0DPQHGE5z0vQoR+3kbBJObbXXhCNUvA+KgwLa9gGSWbuEZ9+8+hUj7i9/c6zGrLISzEGGnTd5QJap1hFpymFBPQsgH455e+RnUz307W8luokgwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("90ef930e626a620628a53e95ce77e51f")

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        print(body, signature)
        handler.handle(body, signature)
        
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
       
        line_bot_api.reply_message(
            event.reply_token,
            message_response(event)
            )

# 以下功能列表
BotNormalFunction=['網路','倒垃圾','房租','公車']
BotFunFunction=['謝謝阿姨','下雨','阿姨','水果']
# 以上功能列表
FunctionWaitAdd=[]
def message_response(event):
    receiveText=event.message.text
    if receiveText=='功能':
        NormalFunction=''
        for i in range(len(BotNormalFunction)):
            NormalFunction+=BotNormalFunction[i]+'\n'
        responseText=NormalFunction
    elif receiveText=='隱藏功能':
        FunFunction=''
        for i in range(len(BotFunFunction)):
            FunFunction+=BotFunFunction[i]+'\n'
        responseText=FunFunction
    #===============Normal Function====================
    elif receiveText==BotNormalFunction[0]:
        responseText='不能裝300M/100M只能100M/40M 不舒服'
    elif receiveText==BotNormalFunction[1]:
        responseText='臺北市垃圾分類、收運方式及收運時間\n一般垃圾及廚餘：星期一、二、四、五、六\n資源回收物：\n（1）平面類(乾淨舊衣物、廢紙類、塑膠袋類)：星期一、五\n（2）立體類(保麗龍類、一般類)：星期二、四、六\n（3）星期三、日停止收運'
    elif receiveText==BotNormalFunction[2]:
        responseText='每月14號之前\n真馬特6000\n小野人7500\n布萊恩賴8500\n山姆度8000'
    elif receiveText==BotNormalFunction[3]:
        responseText='236區間車\n253\n530\n羅斯福路幹線\n606'
    #===============Fun Function=======================
    elif receiveText==BotFunFunction[0]:
        responseText='OK'
    elif receiveText==BotFunFunction[1]:
        responseText='我先把雨水擦乾\n大家一起維護'
    elif receiveText==BotFunFunction[2]:
        responseText='水果放在桌上了喔'
    elif receiveText==BotFunFunction[3]:
        responseText='想吃水果嗎?'
    elif receiveText== "新功能":
    	if FunctionWaitAdd!=[]:
            newfunction=''
            for i in range(len(FunctionWaitAdd)):
                newfunction+=FunctionWaitAdd[i]+"\n"
            responseText=newfunction
        
        
    #===============New Function=======================
    
    if "nf" in receiveText:
        temptext=str(receiveText).replace("nf")
        FunctionWaitAdd.append(temptext)
        responseText=temptext+' added successfully'
	
    #分開回覆textMessage 與 StickerMessage
    if receiveText=='讚':
        BotResponse=StickerMessage(
            package_id="11537",
            sticker_id="52002735"
        )
    elif receiveText=='天氣':
        FlexMessage = json.load(open('weather.json','r',encoding='utf-8'))
        BotResponse=FlexSendMessage('天氣',FlexMessage)
    else:
        BotResponse=TextSendMessage(responseText)
    return BotResponse

if __name__ == "__main__":
    app.run()