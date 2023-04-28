  global ran_q, actions
  msg = []
  actions = []
  numsQ = [1, 2, 3, 4, 5]  # if題目數量不同 這邊要改？試 ranint(len(questions_dic))
  ran_numsQ = random.choice(numsQ)
  ran_q = questions_dic["q" + str(ran_numsQ)]

  #增加SYSTEM_MESSAGE
  #QtoSM=None
  QtoSM = ran_q['q']
  memory.change_system_message(user_id, QtoSM + SM)

  #增加SYSTEM_MESSAGE

  # 定義 stuResp 存入學生回應訊息(ID、時間、訊息) 若是系統訊息則sys="系統"
  def stuResp(user_id, time, text, sys):
    with open(f"sturesp/allresp/{user_id}.json", mode="a+", encoding="utf8") as resp:
      tg_text = {"ID": f"{user_id}{sys}", "時間": time, "訊息": text}
      json.dump(tg_text, resp, ensure_ascii=False, indent=0)
  # 定義 stuResp 存入學生回應訊息(ID、時間、訊息)

  # okQ 答對的題庫 若還沒有就可在此先創建
  with open(f"sturesp/okQ/{user_id}.json", mode="r", encoding="utf8") as okQ_dic:
    okQ_dic.read()
  # 定義 okQ 答對的題庫
  def okQ(user_id, time, ran_q):
    with open(f"sturesp/okQ/{user_id}.json", mode="a+", encoding="utf8") as Q:
      tg_text = {"ID": user_id, "時間": time, "題目": ran_q}
      json.dump(tg_text, Q, ensure_ascii=False, indent=0)
  # okQ 答對的題庫

  # 定義 判斷答案
  def judgeAns(Ans):
    if Ans == ran_q['a']:
      msg = TextSendMessage(text="答對了！" + str(ran_q['tip']))
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, time, ran_q)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")
    return (msg)
  # 定義 判斷答案

  #存個人發送的訊息
  stuResp(user_id, time, text, "")
  #存個人發送的訊息

  #調用題目
  if text.startswith('「題目」'):
    if len(okQ_dic) == len(questions_dic):  # 若所有題目都回答正確
      msg = TextSendMessage(text="恭喜你~已經完成今天的題目囉！")
    else:
      with open(f"sturesp/okQ/{user_id}.json", mode="a+", encoding="utf8") as f:   #讀取個人已完成題庫
        stu_Q = json.load(f)
      for i, q in enumerate(stu_Q):
        if q == ran_q:   # 題目已在做對題庫中
          continue
        else:
          for option in ['A', 'B', 'C', 'D']:
            action = PostbackTemplateAction(
              label=f"({option}) {ran_q['options'][option]}",
              text=f"({option}) {ran_q['options'][option]}",
              data=f"{option}&{ran_q['options'][option]}")
            actions.append(action)
          template = ButtonsTemplate(title='題目', text=ran_q['q'], actions=actions)
          message = TemplateSendMessage(alt_text='題目：' + str(ran_q['q']) + '\n選項：' + str(ran_q['options']), template=template)
          msg.append(message)
          stuResp(user_id, time, f"題目：{ran_q['q']}選項：{str(ran_q['options'])}", "(系統)")
          break
  #調用題目

  #調用答案
  elif text.startswith('(A) '):
    judgeAns('A')
    
  elif text.startswith('(B) '):
    judgeAns('B')
    
  elif text.startswith('(C) '):
    judgeAns('C')

  elif text.startswith('(D) '):
    judgeAns('D')
  #調用答案
