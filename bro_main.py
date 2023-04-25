from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
  MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
  ImageSendMessage, AudioMessage, ButtonsTemplate, MessageTemplateAction,
  PostbackEvent, PostbackTemplateAction, MessageAction, CarouselTemplate,
  CarouselColumn, PostbackAction, URIAction)

import os
import uuid
import re
import json #json
import datetime #轉換時間戳記
import codecs #ASCII

from src.models import OpenAIModel
from src.memory import Memory
from src.logger import logger
from src.storage import Storage
from src.utils import get_role_and_content

load_dotenv('.env')

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
storage = Storage('db.json')
#新立的變數
SM = 'You are an elementary school teacher.Answer in a way that elementary school students can understand.Answers should be short and precise.Unless it is a question that should be answered in English, it should be answered in Traditional Chinese.Give the best answer and avoid answers that may be wrong.Responses should be consistent and coherent.1公頃等於100公畝。40%off是打六折的意思。'
#
memory = Memory(system_message=os.getenv('SYSTEM_MESSAGE'),
                memory_message_count=2)
model_management = {}
api_keys = {}


@app.route("/callback", methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']
  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)
  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    print(
      "Invalid signature. Please check your channel access token/channel secret."
    )
    abort(400)
  return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
  user_id = event.source.user_id
  text = event.message.text.strip()
  logger.info(f'{user_id}: {text}')

  #抓時間
  timestamp = event.timestamp # 獲取當前時間的時間戳記
  timestamp_seconds = timestamp / 1000# 將毫秒轉換為秒
  dt = datetime.datetime.fromtimestamp(timestamp_seconds)# 將時間戳記轉換為datetime物件
  time = dt.strftime("%Y-%m-%d %H:%M:%S")# 將datetime物件轉換為指定格式的字串
  #抓時間

  #增加SYSTEM_MESSAGE
  #QtoSM=None
  QtoSM='{當前題目:同學們做體操，20個同學排成一行，前後相鄰兩個人之間相距2m。從第一人到最後一個人的距離長是多少m?}'
  memory.change_system_message(
    user_id, QtoSM +SM)
  #增加SYSTEM_MESSAGE

  #存個人發送的訊息
  with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
    id_text={"ID": user_id,"時間": time ,"訊息": text}
    json.dump(id_text, f , ensure_ascii=False, indent=0)
  #存個人發送的訊息

  #判讀文字前綴
  try:
    if text.startswith('/註冊'):
      #強制正確
      #api_key = text[3:].strip()
      api_key = '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'
      #強制正確
      model = OpenAIModel(api_key=api_key)
      is_successful, _, _ = model.check_token_valid()
      if not is_successful:
        raise ValueError('Invalid API token')
      model_management[user_id] = model
      api_keys[user_id] = api_key
      storage.save(api_keys)
      msg = TextSendMessage(text='Token 有效，註冊成功')

    elif text.startswith('「說明」'):
      msg = TextSendMessage(text="""你好!我是「賴」學習!
我是一個機器人，
我會盡力回答你問我的任何問題，但回答需要一點時間，我一次只能回答一個問題喔~

回家作業是以一次一題的方式進行，
❗按了之後就會直接送出並記錄分數且不能修改喔❗
但就算答錯了也別灰心，看看解答，多多學習。

當你準備好之後再開始下一題吧!

⬇下面是使用說明⬇
圖文選單
👉點擊圖片以觸發功能
👉👉「說明」:呼叫使用說明
👉👉「影片」:呼叫單元學習影片
👉👉「題目」:呼叫回家作業

輸入文字
👉向機器人問問題""")

      #存系統發送的訊息
      with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
        id_text={"ID": f'{user_id}(系統)',"時間戳記": time ,"訊息": '說明'}
        json.dump(id_text, f , ensure_ascii=False, indent=0)
      print('(系統:','說明',')')
      #存系統發送的訊息
    elif text.startswith('「影片」'):
      msg = TemplateSendMessage(
        #text="""還沒有資源喔~\nhttps://youtu.be/MIR5zIpWBH0""")
        alt_text='CarouselTemplate',
        template=CarouselTemplate(columns=[
          CarouselColumn(
            thumbnail_image_url=
            'https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
            title='選單 1',
            text='說明文字 1',
            actions=[
              MessageAction(label='hello', text='hello'),
              URIAction(label='oxxo.studio', uri='http://oxxo.studio')
            ]),
          CarouselColumn(
            thumbnail_image_url=
            'https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
            title='選單 2',
            text='說明文字 2',
            actions=[
              MessageAction(label='hi', text='hi'),
              URIAction(label='STEAM 教育學習網', uri='https://steam.oxxostudio.tw')
            ])
        ]))
      
      #存系統發送的訊息
      with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
        id_text={"ID": f'{user_id}(系統)',"時間戳記": time ,"訊息": '影片'}
        json.dump(id_text, f , ensure_ascii=False, indent=0)
      print('(系統:','影片',')')
      #存系統發送的訊息
    
    #調用題目
    elif text.startswith('「題目」'):
      #強制正確
      api_key = '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'
      #強制正確
      msg = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(  #裡面的東西全部換成一個變數，調出題庫裡的一題
          #thumbnail_image_url=None,
          thumbnail_image_url=
          'https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
          title='「題目」',
          text='''同學們做體操，20個同學排成一行，前後相鄰兩個人之間相距2m。從第一人到最後一個人的距離長是多少m?''',
          actions=[
            PostbackTemplateAction(
              label='(A) 38m',
              text='(A) 38m',  #A
              data='A&38m'),
            PostbackTemplateAction(
              label='(B) 40m',
              text='(B) 40m',  #B
              data='A&40m'),
            PostbackTemplateAction(
              label='(C) 18m',
              text='(C) 18m',  #C
              data='A&18m'),
            PostbackTemplateAction(
              label='(D) 20m',
              text='(D) 20m',  #D
              data='A&20m')
          ])  #裡面的東西全部換成一個變數，調出題庫裡的一題
      )

      #存系統發送的訊息
      with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
        id_text={"ID": f'{user_id}(系統)',"時間戳記": time ,"訊息": '題目'}
        json.dump(id_text, f , ensure_ascii=False, indent=0)
      print('(系統:','題目',')')
      #存系統發送的訊息
    
    #調用題目
    
    #調用答案
    elif text.startswith('(A) '):  #換成一個變數，調出上一題的選項答案，以及詳解
      msg = TextSendMessage(text="""答對了!""")
      #存系統發送的訊息
      with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
        id_text={"ID": f'{user_id}(系統)',"時間戳記": time ,"訊息": '答對了!'}
        json.dump(id_text, f , ensure_ascii=False, indent=0)
      print('(系統:','答案',' 答對了!)')
      #存系統發送的訊息
    elif text.startswith('(B) '):  #換成一個變數，調出上一題的選項答案，以及詳解
      msg = TextSendMessage(text="""答錯囉!因為...""")
      #存系統發送的訊息
      with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
        id_text={"ID": f'{user_id}(系統)',"時間戳記": time ,"訊息": '答錯囉!因為...'}
        json.dump(id_text, f , ensure_ascii=False, indent=0)
      print('(系統:','答案',' 答錯囉!因為...)')
      #存系統發送的訊息
    elif text.startswith('(C) '):  #換成一個變數，調出上一題的選項答案，以及詳解
      msg = TextSendMessage(text="""答錯囉!因為...""")
      #存系統發送的訊息
      with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
        id_text={"ID": f'{user_id}(系統)',"時間戳記": time ,"訊息": '答錯囉!因為...'}
        json.dump(id_text, f , ensure_ascii=False, indent=0)
      print('(系統:','答案',' 答錯囉!因為...)')
      #存系統發送的訊息
    elif text.startswith('(D) '):  #換成一個變數，調出上一題的選項答案，以及詳解
      msg = TextSendMessage(text="""答錯囉!因為...""")
      #存系統發送的訊息
      with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
        id_text={"ID": f'{user_id}(系統)',"時間戳記": time ,"訊息": '答錯囉!因為...'}
        json.dump(id_text, f , ensure_ascii=False, indent=0)
      print('(系統:','答案',' 答錯囉!因為...)')
      #存系統發送的訊息
    #調用答案

    elif text.startswith('/系統訊息'):
      memory.change_system_message(user_id, text[5:].strip())
      msg = TextSendMessage(text='輸入成功')

    elif text.startswith('/清除'):
      memory.remove(user_id)
      msg = TextSendMessage(text='歷史訊息清除成功')

    elif text.startswith('/圖像'):

      #強制註冊
      #api_key = text[3:].strip()
      api_key = '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'
      #強制正確
      model = OpenAIModel(api_key=api_key)
      is_successful, _, _ = model.check_token_valid()
      if not is_successful:
        raise ValueError('Invalid API token')
      model_management[user_id] = model
      api_keys[user_id] = api_key
      storage.save(api_keys)
      #msg = TextSendMessage(text='Token 有效，註冊成功')
      #強制註冊

      prompt = text[3:].strip()
      memory.append(user_id, 'user', prompt)
      is_successful, response, error_message = model_management[
        user_id].image_generations(prompt)
      if not is_successful:
        raise Exception(error_message)
      url = response['data'][0]['url']
      msg = ImageSendMessage(original_content_url=url, preview_image_url=url)
      memory.append(user_id, 'assistant', url)
    #判斷指令
    elif text.startswith('/'):
      msg = TextSendMessage(text='請輸入正確指令')
    #判斷指令

    #呼叫OpenAI
    else:
      #強制註冊
      #api_key = text[3:].strip()
      api_key = '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'
      #強制正確
      model = OpenAIModel(api_key=api_key)
      is_successful, _, _ = model.check_token_valid()
      if not is_successful:
        raise ValueError('Invalid API token')
      model_management[user_id] = model
      api_keys[user_id] = api_key
      storage.save(api_keys)
      #msg = TextSendMessage(text='Token 有效，註冊成功')
      #強制註冊

      memory.append(user_id, 'user', text)
      is_successful, response, error_message = model_management[
        user_id].chat_completions(memory.get(user_id),
                                  os.getenv('OPENAI_MODEL_ENGINE'))
      if not is_successful:
        raise Exception(error_message)
      role, response = get_role_and_content(response)
      msg = TextSendMessage(text=response)
      #test
      #print (msg.decode('unicode_escape'))
      #test
      memory.append(user_id, role, response)
      
      #存GPT-4發送的訊息
      with open(f'students/{user_id}.json', 'a', encoding="utf-8") as f:
        id_text={"ID": f'{user_id}(GPT-4)',"時間戳記": time ,"訊息": response}
        json.dump(id_text, f , ensure_ascii=False, indent=0)
      print('(GPT-4:',response,')')
      #存GPT-4發送的訊息
  
    #呼叫OpenAI

  #msg訊息格式錯誤回傳
  except ValueError:
    msg = TextSendMessage(text='Token 無效，請重新註冊，格式為 /註冊 sk-xxxxx')
  except Exception as e:
    memory.remove(user_id)
    if str(e).startswith('Incorrect API key provided'):
      msg = TextSendMessage(text='OpenAI API Token 有誤，請重新註冊。')
    elif str(e).startswith(
        'That model is currently overloaded with other requests.'):
      msg = TextSendMessage(text='已超過負荷，請稍後再試')
    else:
      msg = TextSendMessage(text=str(e))
  #msg訊息格式錯誤回傳





  #送出給LINE
  line_bot_api.reply_message(event.reply_token, msg)
  #送出給LINE
  





@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
  user_id = event.source.user_id
  audio_content = line_bot_api.get_message_content(event.message.id)
  input_audio_path = f'{str(uuid.uuid4())}.m4a'
  with open(input_audio_path, 'wb') as fd:
    for chunk in audio_content.iter_content():
      fd.write(chunk)

  try:
    if not model_management.get(user_id):
      raise ValueError('Invalid API token')
    else:
      is_successful, response, error_message = model_management[
        user_id].audio_transcriptions(input_audio_path, 'whisper-1')
      if not is_successful:
        raise Exception(error_message)
      memory.append(user_id, 'user', response['text'])
      is_successful, response, error_message = model_management[
        user_id].chat_completions(memory.get(user_id), 'gpt-3.5-turbo')
      if not is_successful:
        raise Exception(error_message)
      role, response = get_role_and_content(response)
      memory.append(user_id, role, response)
      msg = TextSendMessage(text=response)
  except ValueError:
    msg = TextSendMessage(text='請先註冊你的 API Token，格式為 /註冊 [API TOKEN]')
  except Exception as e:
    memory.remove(user_id)
    if str(e).startswith('Incorrect API key provided'):
      msg = TextSendMessage(text='OpenAI API Token 有誤，請重新註冊。')
    else:
      msg = TextSendMessage(text=str(e))
  os.remove(input_audio_path)
  line_bot_api.reply_message(event.reply_token, msg)


@app.route("/", methods=['GET'])
def home():
  return (
    #只要打HTML就會顯示
    """
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var data = google.visualization.arrayToDataTable([
          ['Task', 'Hours per Day'],
          ['工作',     11],
          ['吃飯',      2],
          ['Commute',  1],
          ['滑手機',  1],
          ['Watch TV', 2],
          ['Sleep',    7]
        ]);

        var options = {
          title: 'My Daily Activities'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="piechart" style="width: 900px; height: 500px;"></div>
  </body>
</html>
""")
  #只要打HTML就會顯示


if __name__ == "__main__":
  try:
    data = storage.load()
    for user_id in data.keys():
      model_management[user_id] = OpenAIModel(api_key=data[user_id])
  except FileNotFoundError:
    pass
  app.run(host='0.0.0.0', port=8080)
