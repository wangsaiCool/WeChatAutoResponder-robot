#!/usr/bin/env python3.5
from wxpy import *
from chatterbot import ChatBot
import random as rd
import urllib.parse
import time
from chatterbot.trainers import ListTrainer

url = "http://www.tuling123.com/openapi/api"
APIkey1 = "36c9ea89f41844eaba5aab999406fc05"
listRecording = ["风太～大，我听不清～～你～说的～话", "我这边太吵了，我听不清楚", "虽然我听不清楚，但是不明觉厉", "你的声音那么好听，你给我讲一个笑话吧",
                 "我觉得你打字的话，我能更快的回复你",
                 "我现在不方便听语音，你打字可以吗？", "[皱眉]", "迷之微笑", "巴扎嘿", "对不起，我没有听清楚", "你的手机没电了吧", "Sorry，我没有听明白",
                 "起风了，记得回家收衣服嗯，因为我只听见你那边呼呼的声音", "真的不够明白你说的啦", "我们换个话题好不好", "我不会说话啊，因为我没有嘴巴", "我快没电了，你给我充话费吗"]
listPicture = ["[奸笑]", "[微笑]", "大头大头下雨不愁", "迷之微笑", "这边下雨了，路上好滑啊", "你的手机没电了吧", "巴扎嘿", "夸我", "嘿嘿嘿", "[捂脸]",
               "[发呆]",
               "[礼物]", "[拥抱]", "[勾引]",
               "图片不错哦", "你是盗图狂魔", "[机智]", "[皱眉]", "[耶]", "[发抖]", "[跳跳]", "[嘿哈]", "[嘿哈]", "[转圈]", "[机智]", "[嘿哈]",
               "[机智]", "[嘿哈]", "你这个表情，给你32个赞[嘿哈]"]

# 建议打开只读，防止修改数据库
my_bot = ChatBot("deepThought", read_only=True)
# my_bot.set_trainer(ListTrainer)
bot = Bot(cache_path=True)  # 用于接入微信的机器人
charP1 = None
# QA训练文件名字
QAfile = "/home/wangsai/PycharmProjects/myRobot/resources/QArepoWithTuring/QA" + str(int(time.time()))


# 匹配联系人
def matchContact():
    global charP1
    while (True):
        print("聊天人的名字：")
        targetPerson = input()
        friends = bot.friends()  # 所有的好友
        friend = None
        countPerson = 0
        greeting = getMoringOrNight()
        for friend in friends:
            countPerson += 1
            if (countPerson % 2 == 0):
                print("已经寻找【", countPerson, "】人")
            if (targetPerson in str(friend)):
                charP1 = friend
                print(str(friend), ":", end="")
                print("请问这是你需要的联系人吗？是请输入 Y，否则，请输入 N")
                isTarget = input()
                if (isTarget is "Y" or isTarget is "y"):
                    print("Robot:" + greeting + "我是高冷的笨笨,刚刚上线...[奸笑] \n(AutoResponder)")
                    charP1.send(greeting + "我是高冷的笨笨,刚刚上线...[奸笑] \n(AutoResponder)")
                    time.sleep(2)
                    print("Robot:好久不见，甚是想念啊  \n(AutoResponder)")
                    charP1.send("好久不见，甚是想念啊  \n(AutoResponder)")
                    break
        if (friend == None):
            print("未匹配到联系人,请重试...", )
        else:
            break


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


# 匹配联系人
matchContact()


@bot.register(charP1)
def reply_my_friend_1(msg):
    # 在控制台打印结果
    print("---------------")
    print(msg)
    mimeType = str(msg).split(":")[1]
    msg = getMsg(msg)
    # 不能识别语音
    if ("Recording" in mimeType):
        response = listRecording[rd.randint(0, listRecording.__len__() - 1)]
        print("Robot:", response)
        time.sleep(rd.randint(1, 3))
        return response + "\n(AutoResponder)"
    # 不能识别图片表情
    elif ("Picture" in mimeType):
        response = listPicture[rd.randint(0, listPicture.__len__() - 1)]
        print("Robot:", response)
        time.sleep(rd.randint(1, 4))
        return response + "\n(AutoResponder)"
    # 从图灵网获取问答信息，请求方式为post
    # 可以参考：http://www.tuling123.com/help/h_cent_webapi.jhtml?nav=doc
    response = getQAFromWeb(msg)
    # trainRobot(response, msg)
    # 文本信息
    if (response["code"] == 100000):
        talker = str(charP1).replace(">", "").split(":")[1].strip()
        # 收集训练数据
        genQAFile(QAfile + "." + talker + ".dialogues", question=msg, answer=response["text"])
        print("Robot:", response["text"])
        return response["text"] + "\n(AutoResponder)"  # 使用机器人进行自动回复
    # 链接
    elif (response["code"] == 200000):
        print("Robot:", response["text"])
        time.sleep(rd.randint(1, 3))
        return response["text"] + "：\n" + response["url"] + "\n(AutoResponder)"  # 使用机器人进行自动回复
    # 新闻
    elif (response["code"] == 302000):
        print("Robot:", response["text"])
        time.sleep(rd.randint(0, 3))
        news = response["list"]
        return response["text"] + "：\n" \
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
        time.sleep(rd.randint(0, 2))
        detail = response["list"]
        return response["text"] + "：\n" \
               + "\n菜名：" + detail["name"] \
               + "\n菜谱信息：" + detail["info"] \
               + "\n详细内容：" + detail["detailurl"] \
               + "\n(AutoResponder)"  # 使用机器人进行自动回复


# 格式化msg消息,提取消息内容
def getMsg(msg=None):
    msg = str(msg)
    msg = msg.split(":")[1]
    msg = msg.split("(")[0]
    return msg


# 从图灵网获取问答结果
def getQAFromWeb(msg):
    id = getID(str(charP1).split(":")[1]).replace(">", "").strip()
    id = id.replace("b' ", "")
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


def genQAFile(name=None, question="", answer=""):
    fo = open(name, "a")
    try:
        fo.write("$\n")
        fo.write("Q:" + question.strip() + "\n")
        fo.write("A:" + answer + "\n")
    finally:
        fo.close()


def getID(charP1):
    id = str(charP1.encode("utf-8")).replace("\\x", "")
    if (id.__len__() > 32):
        id = id[0:31]
    return str(id)


bot.start()
# 堵塞线程，并进入 Python 命令行
embed()
