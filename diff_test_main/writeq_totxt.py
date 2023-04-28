  # 定義 stuResp 存入學生回應訊息(ID、時間、訊息) 若是系統訊息則sys="系統"
  def stuResp(user_id, time, text, sys):
    with open(f"sturesp/allresp/{user_id}.txt", mode="a+",
              encoding="utf8") as resp:
      resp.write(f"ID:{user_id}{sys} 時間:{time} 訊息:{text}")
  # 定義 stuResp 存入學生回應訊息(ID、時間、訊息)

  # okQ 答對的題庫 若還沒有就可在此先創建
  with open(f"sturesp/okQ/{user_id}.txt", mode="a+", encoding="utf8") as Q:
    okQ_dic = Q.read()
  # 定義 okQ 答對的題庫
  def okQ(user_id, time, okQnum):
    with open(f"sturesp/okQ/{user_id}.txt", mode="a+", encoding="utf8") as Q:
      Q.write(f"ID:{user_id} 時間:{time} 訊息:{text}")
  # okQ 答對的題庫
