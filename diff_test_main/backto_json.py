  global ran_q, actions
  msg = []
  actions = []
  numsQ = [1, 2, 3, 4, 5]  # if題目數量不同 這邊要改？試 ranint(len(questions_dic))
  ran_numsQ = random.choice(numsQ)
  ran_q = questions_dic["q" + str(ran_numsQ)]

  # 定義 存入學生回應訊息(ID、時間、訊息)
  def stuResp(user_id, time, text, sys):
    with open(f"sturesp/allresp/{user_id}.json", mode="a+",
              encoding="utf8") as resp:
      tg_text = {"ID": f"{user_id}{sys}", "時間": time, "訊息": text}
      json.dump(tg_text, resp, ensure_ascii=False, indent=0)

  # 定義 存入學生回應訊息(ID、時間、訊息)

  # 答對的題庫 若還沒有就可在此先創建
  with open(f"sturesp/okQ/{user_id}.json", mode="r", encoding="utf8") as Q:
    Q.read()
  # 定義 答對的題庫
  def okQ(user_id, time, okQnum):
    with open(f"sturesp/okQ/{user_id}.json", mode="a+", encoding="utf8") as Q:
      tg_text = {"ID": user_id, "時間": time, "題號": "q" + str(okQnum)}
      Q.write(tg_text)
  # 答對的題庫


  def judgeAns(Ans):
    if Ans == ran_q['a']:
      msg = TextSendMessage(text="答對了！" + str(ran_q['explain']))
      stuResp(user_id, time, "答對了！", "(系統)")
      # 從個人題庫(只有題號? >> X,有題目)中移除目前題號
      with open(f"sturesp/NsQ/{user_id}.json", mode="r", encoding="utf8") as f:   #讀取個人題庫   #加NsQ:還沒寫對的題目
        stu_NsQ = json.load(f)
      for i, q in enumerate(stu_NsQ):
        if q == ran_q:   # 判斷
          del questions[q]  # 從題目列表中移除已回答的題目
          break
      with open(new_file_name, 'w', encoding='utf-8') as f:
        f.write(json.dumps(my_list, indent=2))
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")
    return (msg)     
      
      
  #調用答案
  elif text.startswith('(A) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    if 'A' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, time, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")
