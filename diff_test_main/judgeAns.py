  #調用答案
  elif text.startswith('(A) '):
    if 'A' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, time, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")

  elif text.startswith('(B) '):
    if 'B' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, time, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")

  elif text.startswith('(C) '):
    if 'C' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, time, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")

  elif text.startswith('(D) '):
    if 'D' == ran_q['a']:
      msg = TextSendMessage(text="答對了！")
      stuResp(user_id, time, "答對了！", "(系統)")
      okQ(user_id, time, ran_numsQ)
    else:
      msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
      stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")
  #調用答案
