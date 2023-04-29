from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (
  MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage,
  ImageSendMessage, AudioMessage, ButtonsTemplate, MessageTemplateAction,
  PostbackEvent, PostbackTemplateAction, MessageAction, CarouselTemplate,
  CarouselColumn, PostbackAction, URIAction)
from IPython.display import display, HTML

import os
import uuid
import re
import random
import json  #json
import datetime  #轉換時間戳記
import codecs  #ASCII
import pandas as pd

from src.models import OpenAIModel
from src.memory import Memory
from src.logger import logger
from src.storage import Storage
from src.utils import get_role_and_content

load_dotenv('.env')

# 讀入總題庫
with open("Questions.json", encoding='utf8') as file:
  content = file.read()
  questions_dic = json.loads(content)
# 讀入總題庫

app = Flask(__name__)
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
storage = Storage('db.json')

# 新增 SYSTEM_MESSAGE
SM = 'You are an elementary school teacher.Answer in a way that elementary school students can understand.Answers should be short and precise.Unless it is a question that should be answered in English, it should be answered in Traditional Chinese.Give the best answer and avoid answers that may be wrong.Responses should be consistent and coherent.1公頃等於100公畝。40%off是打六折的意思。'
# 新增 SYSTEM_MESSAGE

memory = Memory(system_message=os.getenv('SYSTEM_MESSAGE'),
                memory_message_count=2)
model_management = {}

api_keys = {}
api_key = 'your api keys'  #直接在這裡改


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


# 每傳一次"文字"訊息判斷一次
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
  user_id = event.source.user_id
  text = event.message.text.strip()
  logger.info(f'{user_id}: {text}')
  global api_keys, api_key
  api_keys[user_id] = api_key  #直接註冊

  #抓時間
  timestamp = event.timestamp  # 獲取當前時間的時間戳記
  timestamp_seconds = timestamp / 1000  # 將毫秒轉換為秒
  dt = datetime.datetime.fromtimestamp(timestamp_seconds)  # 將時間戳記轉換為datetime物件
  time = dt.strftime("%Y-%m-%d %H:%M:%S")  # 將datetime物件轉換為指定格式的字串
  #抓時間

  global ran_q
  msg = []
  actions = []

  # 定義存入學生回應訊息(ID、時間、訊息)
  def stuResp(user_id, time, text, sys):
    os.makedirs("sturesp/allresp", exist_ok=True)
    with open(f"sturesp/allresp/{user_id}.txt", mode="a+",
              encoding="utf8") as resp:
      tg_text = {"ID": f"{user_id}{sys}", "時間": time, "訊息": text}
      resp.write(str(tg_text) + '\n')

  # 定義 存入學生回應訊息(ID、時間、訊息)

  # 答對的題庫 若還沒有就可在此先創建
  with open(f"sturesp/okQ/{user_id}.txt", mode="a+", encoding="utf8") as Q:
    Q.read()

  # 定義 答對的題庫
  def okQ(user_id, okQnum):
    with open(f"sturesp/okQ/{user_id}.txt", mode="a+", encoding="utf8") as Q:
      tg_text = "q" + str(okQnum)
      Q.write(tg_text + '\n')

  # 答對的題庫

  #存個人發送的訊息
  stuResp(user_id, time, text, "")
  #存個人發送的訊息

  if text.startswith('「題目」'):
    global ran_q, numsQ, ran_nums, count
    with open(f"sturesp/okQ/{user_id}.txt", mode="r", encoding='utf8') as f:
      global count
      count = 0
      for line in f:
        count += 1
        
    numsQ = []
    for i in range(len(questions_dic)):
      numsQ.append(i + 1)
    ran_numsQ = random.choice(numsQ)
    ran_q = questions_dic["q" + str(ran_numsQ)]
    #增加SYSTEM_MESSAGE
    #QtoSM=None
    QtoSM = '當前題目' + ran_q['q']
    memory.change_system_message(user_id, QtoSM + SM)
    #增加SYSTEM_MESSAGE

    if count == len(questions_dic):  # 若所有題目都回答正確
      msg = TextSendMessage(text="恭喜你~已經完成今天的題目囉！")
    elif count == 0:
      for option in ['A', 'B', 'C', 'D']:
        action = PostbackTemplateAction(
          label=f"({option}) {ran_q['options'][option]}",
          text=f"({option}) {ran_q['options'][option]}",
          data=f"{option}&{ran_q['options'][option]}")
        actions.append(action)
      template = ButtonsTemplate(title=f"{count}",
                                 text=ran_q['q'],
                                 actions=actions)
      message = TemplateSendMessage(alt_text='題目：' + str(ran_q['q']) +
                                    '\n選項：' + str(ran_q['options']),
                                    template=template)
      msg.append(message)
      stuResp(user_id, time, f"題目：{ran_q['q']}選項：{str(ran_q['options'])}",
              "(系統)")
    else:  # 若所有題目都回答正確
      with open(f"sturesp/okQ/{user_id}.txt", mode="a+", encoding='utf8') as f:
        f.seek(0)
        for q_num in f:
          if q_num == ran_q:  # 題目已在做對題庫中
            message = TextSendMessage(text="！")
          else:
            for option in ['A', 'B', 'C', 'D']:
              action = PostbackTemplateAction(
                label=f"({option}) {ran_q['options'][option]}",
                text=f"({option}) {ran_q['options'][option]}",
                data=f"{option}&{ran_q['options'][option]}")
              actions.append(action)
            template = ButtonsTemplate(title='題目111',
                                       text=ran_q['q'],
                                       actions=actions)
            message = TemplateSendMessage(alt_text='題目：' + str(ran_q['q']) +
                                          '\n選項：' + str(ran_q['options']),
                                          template=template)
            msg.append(message)
            stuResp(user_id, time,
                    f"題目：{ran_q['q']}選項：{str(ran_q['options'])}", "(系統)")
            
  #調用答案
  elif text.startswith('(A) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'A' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")

  elif text.startswith('(B) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'B' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")

  elif text.startswith('(C) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'C' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")

  elif text.startswith('(D) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'D' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")
  #調用答案

  else:
    #判讀文字前綴
    try:
      if text.startswith('「註冊」'):
        #強制正確
        #api_key = text[3:].strip()
        api_key = 'your api keys'
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
        stuResp(user_id, time, "說明", "(系統)")
        print('(系統:', '說明', ')')
        #存系統發送的訊息

      elif text.startswith('「系統訊息」'):
        memory.change_system_message(user_id, text[5:].strip())
        msg = TextSendMessage(text='輸入成功')

      elif text.startswith('「清除」'):
        memory.remove(user_id)
        msg = TextSendMessage(text='歷史訊息清除成功')

      elif text.startswith('「圖像」'):
        #強制註冊
        #api_key = text[3:].strip()
        api_key = 'your api keys'
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
                URIAction(label='STEAM 教育學習網',
                          uri='https://steam.oxxostudio.tw')
              ])
          ]))

        #存系統發送的訊息
        stuResp(user_id, time, "影片", "(系統)")
        print('(系統:', '影片', ')')
        #存系統發送的訊息

      
      #呼叫OpenAI
      else:
        #強制註冊
        #api_key = text[3:].strip()
        api_key = 'your api keys'
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
        stuResp(user_id, time, response, "(GPT-4)")
        print('(GPT-4:', response, ')')
        #存GPT-4發送的訊息

      #呼叫OpenAI

    #msg訊息格式錯誤回傳
    except ValueError:
      msg = TextSendMessage(text='Token 無效，請重新註冊，格式為 「註冊」 sk-xxxxx')
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
  print(count)

  
  #送出給LINE
  line_bot_api.reply_message(event.reply_token, msg) 
  #送出給LINE


  
  # 檢查檔案是否存在，如果存在就讀取之前的資料，否則建立一個新的檔案
  if os.path.isfile('sturecord.html'):
    with open('sturecord.html', 'r', encoding='utf-8') as f:
      previous_data = f.readlines()
      # 只保留前54行的內容
      previous_data = previous_data[:54]
  else:
    previous_data = []

  # 取得路徑下所有的txt檔案
  txt_files = [f for f in os.listdir('sturesp/allresp') if f.endswith('.txt')]

  # 創建一個 dictionary 來儲存每個使用者最新的 DataFrame
  user_tables = {}

  # 逐一讀取每個txt檔案，整理成DataFrame，並存儲在 user_tables 中
  for txt_file in txt_files:
    user_id = txt_file.split('.')[0]
    with open(f'sturesp/allresp/{txt_file}', 'r') as f:
      data = [eval(line) for line in f]

    # 提取 ID、時間、訊息
    rows = []
    for item in data:
      rows.append({'ID': item['ID'], '時間': item['時間'], '訊息': item['訊息']})

    # 將資料轉換成 DataFrame
    df = pd.DataFrame(rows)

    # 如果使用者已經有表格，則將新的訊息更新至原表格，否則就新增一個新表格
    if user_id in user_tables:
      # 找出更新後的資料
      updated_df = df[df['時間'] > user_tables[user_id]['時間'].max()]
      if not updated_df.empty:
        # 將更新後的表格與原本的表格合併
        user_tables[user_id] = pd.concat([user_tables[user_id], updated_df])
    else:
      user_tables[user_id] = df

  # 將每個使用者的 DataFrame 轉換成 HTML 表格，並連接起來
  html_tables = []
  for user_id, df in user_tables.items():
    html_tables.append(f"<h2>{user_id}</h2>" + df.to_html(index=False))

  all_html_tables = '<br>'.join(html_tables)

  # 在 sturecord.html 檔案的末尾繼續添加 HTML 表格
  with open('sturecord.html', 'w', encoding='utf-8') as f:
    # 將表格包裝在一個<div>元素中，加上padding-left樣式屬性讓表格向右移
    html = f"<div style='text-align:center; padding-left: 50px;'>{all_html_tables}</div>"
    f.write(''.join(previous_data) + html)


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
    msg = TextSendMessage(text='請先註冊你的 API Token，格式為 「註冊」 [API TOKEN]')
  except Exception as e:
    memory.remove(user_id)
    if str(e).startswith('Incorrect API key provided'):
      msg = TextSendMessage(text='OpenAI API Token 有誤，請重新註冊。')
    else:
      msg = TextSendMessage(text=str(e))
  os.remove(input_audio_path)
  
  line_bot_api.reply_message(event.reply_token, msg)


@app.route("/", methods=['GET'])
def index():
  with open(os.path.join('index.html'), 'r', encoding='utf-8') as index:
    html_index = index.read()
  return (html_index)


@app.route("/stuall/", methods=['GET'])
def stuall():
  with open(os.path.join('stuall.html'), 'r', encoding='utf-8') as stuall:
    html_stuall = stuall.read()
  return (html_stuall)


@app.route("/stuone/", methods=['GET'])
def stuone():
  with open(os.path.join('stuone.html'), 'r', encoding='utf-8') as stuone:
    html_stuone = stuone.read()
  return (html_stuone)


@app.route("/contact/", methods=['GET'])
def contact():
  with open(os.path.join('contact.html'), 'r', encoding='utf-8') as contact:
    html_contact = contact.read()
  return (html_contact)


@app.route("/sturecord/", methods=['GET'])
def sturecord():
  with open(os.path.join('sturecord.html'), 'r',
            encoding='utf-8') as sturecord:
    html_sturecord = sturecord.read()
  return (html_sturecord)


if __name__ == "__main__":
  try:
    data = storage.load()
    for user_id in data.keys():
      model_management[user_id] = OpenAIModel(api_key=data[user_id])
  except FileNotFoundError:
    pass
  app.run(host='0.0.0.0', port=8080)
