import logging
import azure.functions as func
import http.client
import urllib.request
import urllib.parse
import urllib.error
import json
import requests
from azure.storage.blob import BlockBlobService
from PIL import Image
#from face_API import detectFace,findSimilar,getCharacterName,faceAPI_func
#from python_origin import face_API
import http.client, urllib, base64,json,ast
import json
import pandas as pd
from bs4 import BeautifulSoup
import re
import pandas as pd
import wikipedia
token="Bearer 7p1ma5fM0ylFKf3xbpTMBA+KY1Bc6B3nPsYzcZtwydordOcaNNcACfI7Bwj9jgPuzo47eqZ4sTVKyQHSNug8sAbaJElOCl7BOBwenqACHr0CqU1FubWP/T6NrbyBodFODIMLmKeWsW3nlEeWyAcyowdB04t89/1O/w1cDnyilFU="
wikipedia.set_lang("ja")
def id_check_func(line_user_id):
    df = pd.read_csv("http://ik1-334-27288.vs.sakura.ne.jp/intern_data/user_data.csv",encoding="SHIFT-JIS")
    i=0
    for x in df["line_user_id"]:
        if line_user_id == x  :
            return df["appUserId"][i]
        i=i+1
    return "error"

def title_geter(line_user_id):
    appUserId=id_check_func(line_user_id)
    url="https://api.repl-ai.jp/v1/dialogue"
    apikey="z1frsJuv5oyEjoFYiHTPQP79WZvthvysGEAQ24bW"
    header={"Content-Type":"application/json", "x-api-key":apikey}
    body = {"appUserId":appUserId , 'botId':'sample' ,"voiceText": "title_geter", "initTalkingFlag":False ,"initTopicId":"s4uidwo0op7o0an" }
    r = requests.post(url,headers=header, json=body)
    data = json.loads(r.text)["systemText"]['expression']
    return data
"""
def reminder_func(inn , line_user_id="U6cd5b495a02aed272d8b647c092c48d5"):
    now = datetime.now()
    title= title_geter(line_user_id)
    now_ts = now.timestamp()
    
    x=datetime.strptime(inn, "%Y/%m/%d %H:%M")
    send_data= x.strftime("%Y_%m_%d_%H_%M")
    
    x = x.timestamp()
    print(x - now_ts)
    if x - now_ts <0:
        print("時刻を過ぎていますね")
    
    elif  x - now_ts < 300:
        print("設定時刻5分以内")
    else:
        print("リマインダセットok!")
        payload = {"user_id" :user_id  ,"title":title ,"date":send_data}
        requests.post("http://ik1-334-27288.vs.sakura.ne.jp/intern_data/make_cron.php", data=payload)
"""
def colums_member():
    dc = {
        "title": "時間を設定します",
        "text": "5分以内または過ぎた時刻は設定できません",
        "defaultAction": {
            "type": "uri",
            "label": "View detail",
            "uri": "http://example.com/page/123"
        },
        "actions": [
                    {
                    "type":"datetimepicker",
                    "label":"ここから",
                    "data":"action=date",
                    "mode":"datetime"
                    }
                    ]
}
    return dc
def create_ranking():
    dx = {
    "type": "template",
    "altText": "this is a carousel template",
    "template": {
        "type": "carousel",
        "columns": [colums_member()],
        "imageAspectRatio": "rectangle",
        "imageSize": "cover"
    }
    }
    return dx


def  time_message(user_id):
    url="https://api.line.me/v2/bot/message/push"
    head = {"Content-Type": "application/json","Authorization" :token }
    x = create_ranking()
    r = requests.post(url,headers =head ,json={'to':user_id ,'messages':[x]})

def id_check_func(line_user_id):
    df = pd.read_csv("http://ik1-334-27288.vs.sakura.ne.jp/intern_data/user_data.csv",encoding="SHIFT-JIS")
    i=0
    for x in df["line_user_id"]:
        if line_user_id == x  :
            return df["appUserId"][i]
        i=i+1
    return "error"

def create_func(line_user_id):
    apikey="z1frsJuv5oyEjoFYiHTPQP79WZvthvysGEAQ24bW"
    url = "https://api.repl-ai.jp/v1/registration"
    header={"Content-Type":"application/json", "x-api-key":apikey}
    body = {'botId':'sample'}
    r = requests.post(url,headers=header, json=body)
    appUserId = json.loads(r.text)['appUserId']
    #getでサーバにappUserId を送る
    csv_get="http://ik1-334-27288.vs.sakura.ne.jp/intern_data/example.php?line_user_id="+line_user_id+"&appUserId="+appUserId
    r = requests.get(csv_get)
    url="https://api.repl-ai.jp/v1/dialogue"
    apikey="z1frsJuv5oyEjoFYiHTPQP79WZvthvysGEAQ24bW"

    header={"Content-Type":"application/json", "x-api-key":apikey}
    body = {"appUserId":appUserId , 'botId':'sample' ,"voiceText": "init", "initTalkingFlag":False ,"initTopicId":"s4uidwo0op7o0an" }

    r = requests.post(url,headers=header, json=body)
    return 100 ,appUserId
    
def state_func(line_user_id):
    #line_user_id からappUserIdを求める
    appUserId = id_check_func(line_user_id)  
    #print(appUserId)
    #もし、見つけなければcreate_func
    if appUserId == "error"  :
        return create_func(line_user_id)#新規作成 100を返す
    
    url="https://api.repl-ai.jp/v1/dialogue"
    apikey="z1frsJuv5oyEjoFYiHTPQP79WZvthvysGEAQ24bW"

    header={"Content-Type":"application/json", "x-api-key":apikey}
    body = {"appUserId":appUserId , 'botId':'sample' ,"voiceText": "state_check", "initTalkingFlag":False ,"initTopicId":"s4uidwo0op7o0an" }

    r = requests.post(url,headers=header, json=body)


    data = json.loads(r.text)["systemText"]['expression']
    state_list = data.split(",")
    logging.info(state_list)
    # index...  0 -->mix    1-->male    2-->female   -1-->設定してない
    c=0
    for i in state_list:
        if i =="True":
            logging.info("モード"+str(c))
            return c ,appUserId
        c=c+1
    return -1,appUserId


def talk_func(message,appUserId ):
    url="https://api.repl-ai.jp/v1/dialogue"
    apikey="z1frsJuv5oyEjoFYiHTPQP79WZvthvysGEAQ24bW"

    header={"Content-Type":"application/json", "x-api-key":apikey}
    body = {"appUserId":appUserId , 'botId':'sample' ,"voiceText": message, "initTalkingFlag":False ,"initTopicId":"s4uidwo0op7o0an" }

    r = requests.post(url,headers=header, json=body)
    res = json.loads(r.text)["systemText"]['expression']
    res=res.replace('##', '\n')
    return res

def anime_match(character):
     df = pd.read_csv('http://ik1-334-27288.vs.sakura.ne.jp/intern_data/anime_data3.csv',encoding="SHIFT-JIS")#csv全表示
     dfs = df[ df["character"]==character]#行抽出
     dfs_r = dfs.reset_index()#indexを0にリセット
     df_name = dfs_r["chara-ja"] #dfs_rから列抽出
     dfu = dfs_r["url"]
     df_uri=dfs_r["image"]
     
     return dfu[0],df_name[0],df_uri[0]

def wikipediaSearch(search_text):
	response_string = ""
	search_response = wikipedia.search(search_text)
	if not search_response:
		response_string = "その単語は登録されていません。"
		return response_string
	try:
		wiki_page = wikipedia.page(search_response[0])
	except Exception as e:
		response_string = "エラーが発生しました。\n{}\n{}".format(e.message, str(e))
		return response_string
	wiki_content = wiki_page.content
	response_string += wiki_content[0:wiki_content.find("。")] + "。\n"
	response_string += "リンクはこちら：" + wiki_page.url
	return response_string

def title_func(url):
    if(url == 'https://www.tdc.co.jp'):
        text = "TDCソフト"
        return text
    elif(url == 'https://www.youtube.com/channel/UC4YaOt1yT-ZeyB0OmxHgolA'):
        text = "Vtuber AI"
        return text
    else:
        html = urllib.request.urlopen(url)
        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")
        text = soup.body(class_="itemTitle")
        #print(cleanhtml(hyoka),end = "")
        text = cleanhtml(text)
        return text 

def hyoka(url):
    if(url == 'https://www.tdc.co.jp'):
        text = ("TDCソフトのホームページはこちら↓")
        return text
    elif(url == 'https://www.youtube.com/channel/UC4YaOt1yT-ZeyB0OmxHgolA'):
        text = wikipediaSearch('キズナアイ')
        return text
    else:
    # アクセスするURL
    #url = "https://akiba-souken.com/anime/19063/"
    # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
        html = urllib.request.urlopen(url)
    # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")
        hyoka = soup.body(class_="score")
        #print(cleanhtml(hyoka),end = "")
        text = cleanhtml(hyoka)
        text = re.sub("満足度", "", text)
        return text 

def coment(url):
    if(url == 'https://www.tdc.co.jp'):
        return url
    elif(url == 'https://www.youtube.com/channel/UC4YaOt1yT-ZeyB0OmxHgolA'):
        t = ''
        return t
    else:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")
        #-----
        t = str(soup)
        c = re.search('commentary',t)
        if(c == None):
            c = re.search('<p class="storyLine"></p>',t)
            if(c == None):
                story = soup.body(class_="storyLine")
                print("")
                #print(cleanhtml(story),end ="")
                story = cleanhtml(story)
                return story
            else:
                info = soup.body(class_="info_main")
                info = cleanhtml(info)
                info = adj(info)
                inf = soup.body(class_="info_staff")
                inf = cleanhtml(inf)
                inf = adj2(inf)
                text = info + inf
                return text

        else:
            #-----
            coment = soup.body(class_="commentary")
            #print(cleanhtml(coment),end = "")
            text = cleanhtml(coment)
            return text

def cleanhtml(raw_html):
    raw_html = raw_html[0]
    raw_html = str(raw_html)
    #cleanr = re.compile('<.*?>')
    cleantext = re.sub('<.*?>', '', raw_html)
    return cleantext

def adj(text):
    v1 = text.replace('～\n\n\n','～')
    v2 = v1.replace('\n\n\n','')
    v3 = v2.replace('\n\n','')
    v4 = v3.replace('制作会社：','\n制作会社：')
    return v4

def adj2(text):
    v1 = text.replace('：\n','：')
    v2 = v1.replace('\n\n\n','\n\n')
    v3 = v2.replace('\n\n','\n')
    return v3

def curl(num):
    num = int(num)
    if num == -1:
        url = ("https://www.tdc.co.jp")
    elif num == -2:
        url = ("https://www.youtube.com/channel/UC4YaOt1yT-ZeyB0OmxHgolA")
    else:
        num = str(num)
        url = ("https://akiba-souken.com/anime/" + num)
    #-1のときは例外処理
    #テスト用のprint、urlの生成が上手くいってるか確認できます↓
    # print(url)
    return url

def detectFace(image_url):
    result = None
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'b7c1219c20a44080a73bab3c46b6ef29',
    }
    body = {
        #画像データ
        'url': image_url
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'gender',
        'recognitionModel': 'recognition_01',
        'returnRecognitionModel': 'false',
        'detectionModel': 'detection_01',
    })

    try:
        conn = http.client.HTTPSConnection('ganmenapi.cognitiveservices.azure.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = response.read()
        str_data = data.decode()#strに変換
        dic = ast.literal_eval(str_data)#辞書に変換
        if not dic:
            return "-1" ,"-1"
        result = dic[0]["faceId"]
        gender = dic[0]["faceAttributes"]["gender"]

        return result ,gender
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def findSimilar(image_id,list_type):
    result = None
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'b7c1219c20a44080a73bab3c46b6ef29',
    }

    body = {
        # Request body
        # list_type -- anime_man/male_data/female_data
        "faceId": image_id,
        "faceListId":list_type,
        "maxNumOfCandidatesReturned": 20,
        "mode": "matchFace" #matchPerson が　完全一致
    }
    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('ganmenapi.cognitiveservices.azure.com')
        conn.request("POST", "/face/v1.0/findsimilars?%s" % params, json.dumps(body), headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        result = data[0]["persistedFaceId"]
        return result
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def getCharacterName(x):
    #FaceListのデータを取得　GET使用
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'b7c1219c20a44080a73bab3c46b6ef29',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'returnRecognitionModel': 'false',
    })
    #anime_man 男女混合FaceList
    #male_data 男FaeList
    #female_data 女FaceList
    try:

        conn = http.client.HTTPSConnection('ganmenapi.cognitiveservices.azure.com')
        conn.request("GET", "/face/v1.0/facelists/"+x+"?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()

        conn.close()
        return data.decode()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
        return "Error"

def faceAPI_func(url="https://pbs.twimg.com/media/DGotdkXUIAAXYPF.jpg",mode_flag=0):
    imageid ,gender= detectFace(url)

    if gender == "-1":
        return "Error"
    if mode_flag == 0:
        x = gender +'_data'
    elif mode_flag == 1:
        x = "male_data"
    elif mode_flag == 2:
        x = "female_data"


    result = findSimilar(imageid, x)


    dic = json.loads( getCharacterName(x) )['persistedFaces']
    for i in dic :
      if i['persistedFaceId'] == result :
        print(i['userData'])
        return   i['userData']

def blob_save(img_src,messageId):
    with open("img.raw", 'wb') as img:
        img.write(img_src)
            
    # BLOB Storageサービスに接続
    blobService = BlockBlobService(
        account_name='blobgroup2', 
        account_key='WSI5jstdLvIrx4YxWxlV6lUCsidQn5CDn3HBwjl4V0DfZCWGY+6EcacvkmrQg18W08UcXqJLTDZiPsuUhbuH3A=='
    )

    save_name= messageId+".raw"
    # BLOB コンテナーにファイルを追加
    blobService.create_blob_from_path(
        "morita2",
        save_name,
        "img.raw"
    )  
def line_img_get(messageId):
    url="https://api.line.me/v2/bot/message/"+messageId+"/content"
    head = {"Authorization" :token }

    r = requests.get(url,headers =head)
    return r.content

def create_message(chacacter, title , uri, description ,ans_img="https://i.gzn.jp/img/2018/01/15/google-gorilla-ban/00.jpg"):    
    box1={ "thumbnailImageUrl":ans_img, 
        "imageBackgroundColor": "#FFFFFF", 
        "title": chacacter, 
        "text": title,  
        "actions": [ { "type": "uri", "label": "View detail", "uri": uri }
    ] }

    if len(description)>120:
        description = description[0:119]
    box2={ "text": description,  
        "actions": [ { "type": "uri", "label": "more info", "uri": uri }
    ] }

    d1= [ box1]
    d2 =[ box2]
    x1 = { "type": "template", "altText": "this is a carousel template", "template": { "type": "carousel", "columns": d1 } }
    x2 = { "type": "template", "altText": "this is a carousel template", "template": { "type": "carousel", "columns": d2 } }
    return [x1, x2]

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        
        body = req.get_json()
        logging.info(body["events"][0]["message"]['type'])
        logging.info("userId : "+body["events"][0]["source"]['userId'])
        line_user_id =body["events"][0]["source"]['userId']
        replyToken=body["events"][0]['replyToken']
        type_name = body["events"][0]["message"]['type']
        
        #bot reminderに流す
        if type_name  == 'text':
            #line_user_id からappUserIdを求める
            appUserId = id_check_func(line_user_id)  
            #もし、見つけなければcreate_func
            if appUserId == "error"  :
                _ ,appUserId=create_func(line_user_id)#新規作成 100を返す
            
            text=body["events"][0]["message"]['text']
            text_message = talk_func( text,appUserId )
            if text_message.split("#S#")[-1]=="REMINDERGO":
                time_message(line_user_id)
            else :
                url="https://api.line.me/v2/bot/message/reply"
                head = {"Content-Type": "application/json","Authorization" :token }
                mess={"type":"text", "text": text_message}
                r = requests.post(url,headers =head ,json={"replyToken":replyToken,"messages": [mess]})
                logging.info(r.text)

        
        
        elif type_name == 'image':
            num , appUserId =state_func( line_user_id )
            #ここから　画像を　Azureに保存
            messageId=body["events"][0]["message"]['id']
            img_src = line_img_get(messageId)

            blob_save(img_src,messageId)

            save_url = "https://blobgroup2.blob.core.windows.net/morita2/"+messageId+".raw" #保存先のURL

            """  ここから Face API をおこなう"""
            character = faceAPI_func(url=save_url ,mode_flag=num)
            text_message="あなたは"+character+"に似ていますね！！"
            url="https://api.line.me/v2/bot/message/reply"
            head = {"Content-Type": "application/json","Authorization" :token }
            
            if character == "Error":
                text_message="残念！！顔が認識されませんでした"
                x={"type":"text", "text": text_message }
                r = requests.post(url,headers =head ,json={"replyToken":replyToken,"messages": [x] })
                logging.info(r.text)
            else:
                url_num , name ,uri= anime_match(character)
                logging.info(name)
                logging.info(url_num)
                t = curl(url_num)
                d_json=create_message(chacacter=name, title= title_func(t) ,uri=t, description = coment(t),ans_img=uri)
                r = requests.post(url,headers =head ,json={"replyToken":replyToken,"messages": d_json })
                logging.info(r.text)
        #elif type_name == 'datetimepicker':
        #リマインダーセット
        #ライブラリ　from datetime import datetime
        #inn=選択された日付データを取得(2019/08/28 22:13)この形に変更
        #reminder_func(inn , line_user_id="U6cd5b495a02aed272d8b647c092c48d5")
        
        else : 
            
            url="https://api.line.me/v2/bot/message/reply"
            head = {"Content-Type": "application/json","Authorization" :token }
            x={"type":"text", "text": "そのメッセージは受け付けませんよ！？" }
            r = requests.post(url,headers =head ,json={"replyToken":replyToken,"messages": [x] })
            
            logging.info(r.text)
            
 


    except ValueError:
        logging.error('Body Value Error')
    return func.HttpResponse("{\"statusCode\": 200}", status_code=200)





