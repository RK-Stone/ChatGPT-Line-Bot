  #定義 答對的題庫_json版
  def okQ(user_id, okQnum):
    with open(f"sturesp/okQ/{user_id}.txt", mode="a+", encoding="utf8") as Q:
      tg_text = "q" + str(okQnum)
      Q.write(tg_text + '\n')

  #答對的題庫_json版

  with open(f"sturesp/ranQ/{user_id}.txt", mode="a+", encoding='utf8') as f:
    f.write('')

  def ranQ(user_id, stu_ranQ):
    with open(f"sturesp/ranQ/{user_id}.txt", mode="w", encoding='utf8') as f:
      f.write(stu_ranQ + '\n')
  

      
json = {
  "user_id" : {
    "stu_okQnum" : ["q1", "q1", "q2"],
    "stu_ranQ" : "q5",
    "okQnum_list" : {"q1":2, "q2":1},
    "count_okQ" : 2
  }
}

json = 
{
  user_id : {
              "stu_okQnum" : ["q1", "q1", "q2"],
              "stu_ranQ" : "q5",
              "okQnum_list" : ["q1", "q2"],   #numpy.unique(stu_okQnum)
              "count_okQ" : 2   #len(okQnum_list)
             }
}

#定義 確認學生總資料是否存在 不存在則建新檔 並設定預設空dic
def stuAllData_isExist(user_id):
  if not os.path.exists(f"sturesp/allData/{user_id}.json"):
    with open(f"sturesp/allData/{user_id}.json", mode="w", encoding="utf8") as f:
      json.dump({
            user_id : {
              "stu_okQnum" : [],
              "stu_ranQ" : "",
              "okQnum_list" : {},
              "count_okQ" : 0
            }
          }, f)
#定義 確認學生總資料是否存在

#確認學生總資料是否存在
stuAllData_isExist(user_id)
#確認學生總資料是否存在

#定義 更新資料(要更新的資料)
def rvStuData(user_id, stu_okQnum=None, stu_ranQ=None, okQnum_list=None, count_okQ=None):
    #定義 寫入新資料
    def revise_allData(user_id, stu_okQnum=None, stu_ranQ=None, okQnum_list=None, count_okQ=None):
      new_allData = {}
      with open(f"sturesp/allData/{user_id}.json", mode="r", encoding="utf8") as allData:
        rAllData = json.load(allData)
        if stu_okQnum != None:
          rAllData[user_id]["stu_okQnum"].append(stu_okQnum)
        if stu_ranQ != None:
          rAllData[user_id]["stu_ranQ"] = stu_ranQ
        if okQnum_list != None:
          rAllData[user_id]["okQnum_list"] = okQnum_list
        if count_okQ != None:
          rAllData[user_id]["count_okQ"] = count_okQ
        new_allData = rAllData
      return new_allData
    #定義 寫入更新資料
    def write_allData(new_allData):
      with open(f"sturesp/allData/{user_id}.json", mode="w", encoding="utf8") as allData:
        json.dump(new_allData, allData)
    #更新資料
    write_allData(revise_allData(user_id, stu_okQnum, stu_ranQ, okQnum_list, count_okQ))
#定義 更新資料


#定義 抓取資料
def get_allData(user_id, stu_okQnum=None, stu_ranQ=None, okQnum_list=None, count_okQ=None):
  with open(f"sturesp/allData/{user_id}.json", mode="r", encoding="utf8") as allData:
      rAllData = json.load(allData)
      get_allData = {}
      if stu_okQnum != None:
        get_allData["stu_okQnum"] = rAllData[user_id]["stu_okQnum"]
      if stu_ranQ != None:
        get_allData["stu_ranQ"] = rAllData[user_id]["stu_ranQ"]
      if okQnum_list != None:
        get_allData["okQnum_list"] = rAllData[user_id]["okQnum_list"]
      if count_okQ != None:
        get_allData["count_okQ"] = rAllData[user_id]["count_okQ"]
  return get_allData
#定義 抓取資料
