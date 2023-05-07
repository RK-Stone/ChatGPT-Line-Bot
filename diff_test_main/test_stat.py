  #調用答案
  elif text.startswith('(A) '):
    #print("278判斷答案")
    stu_nowq_dic = questions_dic[get_allData(user_id, stu_ranQ=1)["stu_ranQ"]]
    if 'A' == stu_nowq_dic['a']:
      count_FQnum_list = get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])
      if count_FQnum_list == 0:
        questions_resp_stast[get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])]['ans_1st']['A'].append(user_id)
        text_score = '太好了!第一次就答對了!(+3分)'
        score = 3
      elif count_FQnum_list == 1:
        text_score = '訂正後答對了!(+2分)'
        score = 2
      elif count_FQnum_list == 2:
        text_score = '訂正後答對了!(+2分)'
        score = 2
      else:
        text_score = '答對了!(+1分)'
        score = 1
      msg = TextSendMessage(text=text_score)
      stuResp(user_id, time, text_score, "(系統)")
      #print("283 答對呼叫rvStuData寫stu_score")
      #print("\tscore:+", score)
      if get_allData(user_id, stu_ranQ=1)["stu_ranQ"] not in get_allData(
          user_id, stu_okQnum=1)["stu_okQnum"]:
        rvStuData(user_id,
                  stu_score=json.dumps(
                    int(get_allData(user_id, stu_score=1)["stu_score"]) +
                    score))
        #print("\t", int(get_allData(user_id, stu_score=1)["stu_score"]))
      #print("\t再一次呼叫rvStuData寫stu_okQnum")
      rvStuData(user_id,
                stu_okQnum=json.dumps(
                  str(get_allData(user_id,
                                  stu_ranQ=1)["stu_ranQ"]).replace('"', '')))
      #print("\t再一次呼叫rvStuData寫FQnum_list")
      rvStuData(user_id,
                count_okQ=json.dumps(
                  len(get_allData(user_id, stu_okQnum=1)["stu_okQnum"])))
      #print("成功!")
    else:
      #print("\tdumps進FQnum_list")
      rvStuData(user_id,
                FQnum_list=json.dumps(
                  str(get_allData(user_id,
                                  stu_ranQ=1)["stu_ranQ"]).replace('"', '')))
      count_FQnum_list = get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])
      #print('\t錯了:', count_FQnum_list, '次')
      if count_FQnum_list == 1:
        questions_resp_stast[get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])]['ans_1st']['A'].append(user_id)
        text_score = '答錯囉!冷靜檢查後再回答吧!'
      if count_FQnum_list == 2:
        text_score = '答錯囉!冷靜檢查後再回答吧!'
      elif count_FQnum_list == 3:
        text_score = '或許你可以尋求幫助...' + '(' + str(stu_nowq_dic['tip']) + ')'
      else:
        text_score = '別灰心!訂正好後再做答吧!' + '(' + str(stu_nowq_dic['explain']) + ')'
      msg = TextSendMessage(text=text_score)
      stuResp(user_id, time, text_score, "(系統)")
  elif text.startswith('(B) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    #print("278判斷答案")
    stu_nowq_dic = questions_dic[get_allData(user_id, stu_ranQ=1)["stu_ranQ"]]
    if 'B' == stu_nowq_dic['a']:
      count_FQnum_list = get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])
      if count_FQnum_list == 0:
        questions_resp_stast[get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])]['ans_1st']['B'].append(user_id)
        text_score = '太好了!第一次就答對了!(+3分)'
        score = 3
      elif count_FQnum_list == 1:
        text_score = '訂正後答對了!(+2分)'
        score = 2
      elif count_FQnum_list == 2:
        text_score = '訂正後答對了!(+2分)'
        score = 2
      else:
        text_score = '答對了!(+1分)'
        score = 1
      msg = TextSendMessage(text=text_score)
      stuResp(user_id, time, text_score, "(系統)")
      #print("283 答對呼叫rvStuData寫stu_score")
      #print("\tscore:+", score)
      if get_allData(user_id, stu_ranQ=1)["stu_ranQ"] not in get_allData(
          user_id, stu_okQnum=1)["stu_okQnum"]:
        rvStuData(user_id,
                  stu_score=json.dumps(
                    int(get_allData(user_id, stu_score=1)["stu_score"]) +
                    score))
        #print("\t", int(get_allData(user_id, stu_score=1)["stu_score"]))
      #print("\t再一次呼叫rvStuData寫stu_okQnum")
      rvStuData(user_id,
                stu_okQnum=json.dumps(
                  str(get_allData(user_id,
                                  stu_ranQ=1)["stu_ranQ"]).replace('"', '')))
      #print("\t再一次呼叫rvStuData寫FQnum_list")
      rvStuData(user_id,
                count_okQ=json.dumps(
                  len(get_allData(user_id, stu_okQnum=1)["stu_okQnum"])))
      #print("成功!")
    else:
      #print("\tdumps進FQnum_list")
      rvStuData(user_id,
                FQnum_list=json.dumps(
                  str(get_allData(user_id,
                                  stu_ranQ=1)["stu_ranQ"]).replace('"', '')))
      count_FQnum_list = get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])
      #print('\t錯了:', count_FQnum_list, '次')
      if count_FQnum_list == 1:
        questions_resp_stast[get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])]['ans_1st']['B'].append(user_id)
        text_score = '答錯囉!冷靜檢查後再回答吧!'
      if count_FQnum_list == 2:
        text_score = '答錯囉!冷靜檢查後再回答吧!'
      elif count_FQnum_list == 3:
        text_score = '或許你可以尋求幫助...' + '(' + str(stu_nowq_dic['tip']) + ')'
      else:
        text_score = '別灰心!訂正好後再做答吧!' + '(' + str(stu_nowq_dic['explain']) + ')'
      msg = TextSendMessage(text=text_score)
      stuResp(user_id, time, text_score, "(系統)")
  elif text.startswith('(C) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    #print("278判斷答案")
    stu_nowq_dic = questions_dic[get_allData(user_id, stu_ranQ=1)["stu_ranQ"]]
    if 'C' == stu_nowq_dic['a']:
      count_FQnum_list = get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])
      if count_FQnum_list == 0:
        questions_resp_stast[get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])]['ans_1st']['C'].append(user_id)
        text_score = '太好了!第一次就答對了!(+3分)'
        score = 3
      elif count_FQnum_list == 1:
        text_score = '訂正後答對了!(+2分)'
        score = 2
      elif count_FQnum_list == 2:
        text_score = '訂正後答對了!(+2分)'
        score = 2
      else:
        text_score = '答對了!(+1分)'
        score = 1
      msg = TextSendMessage(text=text_score)
      stuResp(user_id, time, text_score, "(系統)")
      #print("283 答對呼叫rvStuData寫stu_score")
      #print("\tscore:+", score)
      if get_allData(user_id, stu_ranQ=1)["stu_ranQ"] not in get_allData(
          user_id, stu_okQnum=1)["stu_okQnum"]:
        rvStuData(user_id,
                  stu_score=json.dumps(
                    int(get_allData(user_id, stu_score=1)["stu_score"]) +
                    score))
        #print("\t", int(get_allData(user_id, stu_score=1)["stu_score"]))
      #print("\t再一次呼叫rvStuData寫stu_okQnum")
      rvStuData(user_id,
                stu_okQnum=json.dumps(
                  str(get_allData(user_id,
                                  stu_ranQ=1)["stu_ranQ"]).replace('"', '')))
      #print("\t再一次呼叫rvStuData寫FQnum_list")
      rvStuData(user_id,
                count_okQ=json.dumps(
                  len(get_allData(user_id, stu_okQnum=1)["stu_okQnum"])))
      #print("成功!")
    else:
      #print("\tdumps進FQnum_list")
      rvStuData(user_id,
                FQnum_list=json.dumps(
                  str(get_allData(user_id,
                                  stu_ranQ=1)["stu_ranQ"]).replace('"', '')))
      count_FQnum_list = get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])
      #print('\t錯了:', count_FQnum_list, '次')
      if count_FQnum_list == 1:
        questions_resp_stast[get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])]['ans_1st']['C'].append(user_id)
        text_score = '答錯囉!冷靜檢查後再回答吧!'
      if count_FQnum_list == 2:
        text_score = '答錯囉!冷靜檢查後再回答吧!'
      elif count_FQnum_list == 3:
        text_score = '或許你可以尋求幫助...' + '(' + str(stu_nowq_dic['tip']) + ')'
      else:
        text_score = '別灰心!訂正好後再做答吧!' + '(' + str(stu_nowq_dic['explain']) + ')'
      msg = TextSendMessage(text=text_score)
      stuResp(user_id, time, text_score, "(系統)")
  elif text.startswith('(D) '):  #換成一個變數，調出上一題的選項答案，以及詳解
    #print("278判斷答案")
    stu_nowq_dic = questions_dic[get_allData(user_id, stu_ranQ=1)["stu_ranQ"]]
    if 'D' == stu_nowq_dic['a']:
      count_FQnum_list = get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])
      if count_FQnum_list == 0:
        questions_resp_stast[get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])]['ans_1st']['D'].append(user_id)
        text_score = '太好了!第一次就答對了!(+3分)'
        score = 3
      elif count_FQnum_list == 1:
        text_score = '訂正後答對了!(+2分)'
        score = 2
      elif count_FQnum_list == 2:
        text_score = '訂正後答對了!(+2分)'
        score = 2
      else:
        text_score = '答對了!(+1分)'
        score = 1
      msg = TextSendMessage(text=text_score)
      stuResp(user_id, time, text_score, "(系統)")
      #print("283 答對呼叫rvStuData寫stu_score")
      #print("\tscore:+", score)
      if get_allData(user_id, stu_ranQ=1)["stu_ranQ"] not in get_allData(
          user_id, stu_okQnum=1)["stu_okQnum"]:
        rvStuData(user_id,
                  stu_score=json.dumps(
                    int(get_allData(user_id, stu_score=1)["stu_score"]) +
                    score))
        #print("\t", int(get_allData(user_id, stu_score=1)["stu_score"]))
      #print("\t再一次呼叫rvStuData寫stu_okQnum")
      rvStuData(user_id,
                stu_okQnum=json.dumps(
                  str(get_allData(user_id,
                                  stu_ranQ=1)["stu_ranQ"]).replace('"', '')))
      #print("\t再一次呼叫rvStuData寫FQnum_list")
      rvStuData(user_id,
                count_okQ=json.dumps(
                  len(get_allData(user_id, stu_okQnum=1)["stu_okQnum"])))
      #print("成功!")
    else:
      #print("\tdumps進FQnum_list")
      rvStuData(user_id,
                FQnum_list=json.dumps(
                  str(get_allData(user_id,
                                  stu_ranQ=1)["stu_ranQ"]).replace('"', '')))
      count_FQnum_list = get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])
      #print('\t錯了:', count_FQnum_list, '次')
      if count_FQnum_list == 1:
        questions_resp_stast[get_allData(user_id,
                                     FQnum_list=1)["FQnum_list"].count(
                                       get_allData(user_id,
                                                   stu_ranQ=1)["stu_ranQ"])]['ans_1st']['D'].append(user_id)
        text_score = '答錯囉!冷靜檢查後再回答吧!'
      if count_FQnum_list == 2:
        text_score = '答錯囉!冷靜檢查後再回答吧!'
      elif count_FQnum_list == 3:
        text_score = '或許你可以尋求幫助...' + '(' + str(stu_nowq_dic['tip']) + ')'
      else:
        text_score = '別灰心!訂正好後再做答吧!' + '(' + str(stu_nowq_dic['explain']) + ')'
      msg = TextSendMessage(text=text_score)
      stuResp(user_id, time, text_score, "(系統)")
  #調用答案
