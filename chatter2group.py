#!/usr/bin/env python3.5

from wxpy import *
from chatterbot import ChatBot
import random as rd
import urllib.parse
import time

url = "http://www.tuling123.com/openapi/api"
APIkey1 = "36c9ea89f41844eaba5aab999406fc05"
listPicture = ["[奸笑]", "[微笑]", "大头大头下雨不愁", "迷之微笑", "这边下雨了，路上好滑啊", "你的手机没电了吧", "巴扎嘿", "夸我", "嘿嘿嘿", "[捂脸]",
               "[发呆]",
               "[礼物]", "[拥抱]", "[勾引]",
               "图片不错哦", "你是盗图狂魔", "[机智]", "[皱眉]", "[耶]", "[发抖]", "[跳跳]", "[嘿哈]", "[嘿哈]", "[转圈]", "[机智]",
               "[嘿哈]",
               "[机智]", "[嘿哈]", "你这个表情，给你32个赞[嘿哈]"]
listRecording = ["风太～大，我听不清～～你～说的～话", "我这边太吵了，我听不清楚", "虽然我听不清楚，但是不明觉厉", "你的声音那么好听，你给我讲一个笑话吧",
                 "我觉得你打字的话，我能更快的回复你",
                 "我现在不方便听语音，你打字可以吗？", "[皱眉]", "迷之微笑", "巴扎嘿", "对不起，我没有听清楚", "你的手机没电了吧", "Sorry，我没有听明白",
                 "起风了，记得回家收衣服嗯，因为我只听见你那边呼呼的声音", "真的不够明白你说的啦", "我们换个话题好不好", "我不会说话啊，因为我没有嘴巴",
                 "我快没电了，你给我充话费吗"]

isWho1 = "@Sai.W"
isWho2 = "@王赛"
myGroup = None
# 建议打开只读，防止修改数据库
my_bot = ChatBot("deepThought", read_only=True)
bot = Bot(cache_path=True)  # 用于接入微信的机器人


def getGroup():
    # 获取指定群名字
    while (True):
        # 交互信息
        print("请输入群名字：")
        targetGroup = input()
        groups = bot.groups("What")  # 进行测试的群
        greeting = getMoringOrNight()
        print("greeting" + greeting)
        for group in groups:
            if (targetGroup in str(group)):
                print("群名字：", group)
                mylist = list(group)
                if (mylist.__len__() > 10):
                    print("群成员有：", mylist[:9])
                else:
                    print("群成员有：", mylist)
                print("请问这是你需要的群聊吗？是请输入 Y，否则，请输入 N")
                myGroup = group
                instr = input()
                if (instr is "Y" or instr is "y"):
                    break
        if (myGroup == None):
            print("没有找到您输入的相关群名字，请重新输入：")
        else:
            print("Robot:" + greeting + "我是高冷的笨笨 [奸笑] \n(AutoResponder)")
            myGroup.send(greeting + "我是高冷的笨笨[奸笑]" + "\n(AutoResponder)")
            time.sleep(3)
            print("Robot:好久不见，甚是想念。你可以通过@ 我，跟我对话哦 \n(AutoResponder)")
            myGroup.send("好久不见，甚是想念。你可以通过@ 我，跟我对话哦 \n(AutoResponder)")
            break


def getQAFromWeb(msg):
    id = getID(str(myGroup).split(":")[1]).replace(">", "").strip()
    id = id.replace("b' ", "")
    msg = str(msg)
    msg = msg.split(":")[1]
    msg = msg.split("(")[0]
    data = urllib.parse.urlencode(
        {'key': APIkey1,
         'info': msg,
         "userid": id})
    data = data.encode('utf-8')
    request = urllib.request.Request(url)
    # adding charset parameter to the Content-Type header.
    answer = urllib.request.urlopen(request, data)
    # response = {}
    response = answer.read().decode('utf-8')
    response = eval(response)
    return response


def getMoringOrNight():
    currentTime = time.localtime(time.time())
    Hour = int(time.strftime("%H", currentTime))
    if (Hour > 6 and Hour < 12):
        return "上午好，"
    elif (Hour >= 12 and Hour < 18):
        return "下午好，"
    elif (Hour >= 18 and Hour <= 23):
        return "晚上好，"
    elif (Hour >= 0 and Hour <= 6):
        return "晚上好，"
    else:
        return "你好，"


def getID(charP1):
    id = str(charP1.encode("utf-8")).replace("\\x", "")
    if (id.__len__() > 32):
        id = id[0:31]
    return str(id)

getGroup()

@bot.register(myGroup)
def reply_my_friend(msg):
    mimeType = str(msg).split(":")[1]
    name = str(msg).split(":")[0]
    talker = name.split("›")[1].strip()
    if (isWho1 in mimeType or isWho2 in mimeType):
        print("-------------")
        print("talker:", talker, ":", msg.split(":")[1])
        # 不能识别语音
        if ("Recording" in mimeType):
            return "@" + talker + " " + listRecording[
                rd.randint(0, listRecording.__len__() - 1)] + "\n(AutoResponder)"
        # 不能识别图片表情
        elif ("Picture" in mimeType):
            return "@" + talker + " " + listPicture[rd.randint(0, listPicture.__len__() - 1)] + "\n(AutoResponder)"
        # response = my_bot.get_response(msg.text).text
        # print("Robot：", response)
        # print(" ")
        # return response + "\n[奸笑]"  # 使用机器人进行自动回复
        # 从图灵网获取问答信息，请求方式为post
        # 可以参考：http://www.tuling123.com/help/h_cent_webapi.jhtml?nav=doc
        response = getQAFromWeb(msg)
        # 文本信息
        if (response["code"] == 100000):
            print("Robot:", response["text"])
            time.sleep(rd.randint(0, 3))
            return "@" + talker + " " + response["text"] + "\n(AutoResponder)"  # 使用机器人进行自动回复
        # 链接
        elif (response["code"] == 200000):
            print("Robot:", response["text"])
            time.sleep(rd.randint(0, 3))
            return "@" + talker + " " + response["text"] + "：\n" + response[
                "url"] + "\n(AutoResponder)"  # 使用机器人进行自动回复
        # 新闻
        elif (response["code"] == 302000):
            print("Robot:", response["text"])
            time.sleep(rd.randint(0, 3))
            news = response["list"]
            return "@" + talker + " " + response["text"] + "：\n" \
                   + "\n新闻标题：" + news[0]["article"] \
                   + "\n新闻来源：" + news[0]["source"] \
                   + "\n详细内容：" + news[0]["detailurl"] \
                   + "\n\n新闻标题：" + news[1]["article"] \
                   + "\n新闻来源：" + news[1]["source"] \
                   + "\n详细内容：" + news[1]["detailurl"] \
                   + "\n\n新闻标题：" + news[2]["article"] \
                   + "\n新闻来源：" + news[2]["source"] \
                   + "\n详细内容：" + news[2]["detailurl"] \
                   + "\n(AutoResponder)"  # 使用机器人进行自动回复
            # 菜谱
        elif (response["code"] == 308000):
            print("Robot:", response["text"])
            time.sleep(rd.randint(0, 3))
            detail = response["list"]
            return "@" + talker + " " + response["text"] + "：\n" \
                   + "\n菜名：" + detail["name"] \
                   + "\n菜谱信息：" + detail["info"] \
                   + "\n详细内容：" + detail["detailurl"] \
                   + "\n(AutoResponder)"  # 使用机器人进行自动回复  # 从图灵网获取问答结果


# 堵塞线程，并进入 Python 命令行
embed()
