  # 定義 判斷答案
  def judgeAns(Ans):
    if Ans == ran_q['a']:
        msg = TextSendMessage(text="答對了！")
        stuResp(user_id, time, "答對了！", "(系統)")
        okQ(user_id, time, ran_numsQ)
    else:
        msg = TextSendMessage(text="答錯了！" + str(ran_q['tip']))
        stuResp(user_id, time, f"答錯了！{str(ran_q['tip'])}", "(系統)")
    return(msg)
  # 定義 判斷答案
        
  
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
