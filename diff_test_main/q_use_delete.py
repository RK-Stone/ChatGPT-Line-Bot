aa = [1, 2, 3, 4, 5]


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
  user_id = event.source.user_id
  text = event.message.text.strip()
  logger.info(f'{user_id}: {text}')

  global ran_q, aaa
  msg = []
  actions = []
  questions = []

  if text.startswith('「題目」'):
    for i in range(len(questions)):
      questions.append(questions_dic["q" + str(i + 1)])

    global ran_q
    ran_q = random.choice(questions)

    for option in ['A', 'B', 'C', 'D']:
      action = PostbackTemplateAction(
        label=f"({option}) {ran_q['options'][option]}",
        text=f"({option}) {ran_q['options'][option]}",
        data=f"{option}&{ran_q['options'][option]}")
      actions.append(action)
    template = ButtonsTemplate(title='題目', text=ran_q['q'], actions=actions)
    message = TemplateSendMessage(alt_text='題目：' + str(ran_q['q']) + '\n選項：' +
                                  str(ran_q['options']),
                                  template=template)
    msg.append(message)
    if len(aa) == 0:  # 若所有題目都回答正確
      msg = TextSendMessage(text="你已經完成所有題目囉！")
    else:
      aaa = random.choice(aa)
      ran_q = questions_dic["q" + str(aaa)]

      for option in ['A', 'B', 'C', 'D']:
        action = PostbackTemplateAction(
          label=f"({option}) {ran_q['options'][option]}",
          text=f"({option}) {ran_q['options'][option]}",
          data=f"{option}&{ran_q['options'][option]}")
        actions.append(action)
      template = ButtonsTemplate(title='題目' + str(aaa),
                                 text=ran_q['q'],
                                 actions=actions)
      message = TemplateSendMessage(alt_text='題目：' + str(ran_q['q']) +
                                    '\n選項：' + str(ran_q['options']),
                                    template=template)
      msg.append(message)


  def judgeAns(Ans):
    with open(f"sturesp/okQ/{user_id}.txt", mode="a+", encoding="utf8") as Q:
      okQ_dic = Q.read()
    with open(file_name, 'r', encoding='utf-8') as f:
      my_list = json.load(f)
    for idx, obj in enumerate(my_list):
        if obj['id'] == 2:
            my_list.pop(idx)
    if Ans == ran_q['a']:
      msg = TextSendMessage(text="答對了！" + str(ran_q['explain']))
      stuResp(user_id, time, "答對了！", "(系統)")
      aa.remove(aaa)
    with open(new_file_name, 'w', encoding='utf-8') as f:
      f.write(json.dumps(my_list, indent=2))
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")
    return (msg)

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
