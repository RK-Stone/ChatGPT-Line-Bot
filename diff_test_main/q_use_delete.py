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

      jasondothis = TextSendMessage(text=ran_q['q'])
      msg.append(message)
      msg.append(jasondothis)


#調用答案
#調用答案
  elif text.startswith('(A) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'A' == ran_q['a']:
      msg = TextSendMessage(text="答對了！" + str(ran_q['explain']))
      for i, q in enumerate(questions):
        if q == ran_q:
          del questions[q]  # 從題目列表中移除已回答的題目
          break
      aa.remove(aaa)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['explain']))

  elif text.startswith('(B) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'B' == ran_q['a']:
      msg = TextSendMessage(text="答對了！" + str(ran_q['explain']))
      for i, q in enumerate(questions):
        if q == ran_q:
          del questions[q]  # 從題目列表中移除已回答的題目
          break
      aa.remove(aaa)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['explain']))

  elif text.startswith('(C) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'C' == ran_q['a']:
      msg = TextSendMessage(text="答對了！" + str(ran_q['explain']))
      if ran_q in questions:
        questions.remove(ran_q)  # 從題目列表中移除已回答的題目
      aa.remove(aaa)  # 從題目列表中移除已回答的題目
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['explain']))

  elif text.startswith('(D) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'D' == ran_q['a']:
      msg = TextSendMessage(text="答對了！" + str(ran_q['explain']))
      if ran_q in questions:
        questions.remove(ran_q)  # 從題目列表中移除已回答的題目
      aa.remove(aaa)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['explain']))
