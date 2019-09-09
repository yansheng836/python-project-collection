# -*- coding:utf-8 -*-
import display,fight
import re
u"""
魔王抓走了公主，玩家要进入魔塔打败魔王，救出公主。
魔塔由很多房间组成，房间里有物品、怪物，还要公主和魔王。
玩家要打败怪物升级，搜索房间获得物品，让自己属性变得更强，才能打败魔王。
要用一个引擎让这个充满房间的魔塔运行。
"""
#游戏引擎类
class Engine(object):
    def __init__(self,tower):
        self.tower = tower
    def play(self):
#游戏介绍
        print u"""
        欧洲中世纪时期，一位叫玛丽的公主被恶魔掳走了。
        国王悲痛欲绝，许下诺言说谁要是能救回公主，就把国家的国土分他一半。
        可是并没有人敢答应，因为大家都知道恶魔十分恐怖，它所住的地方--魔塔，
        更是一个阴森恐怖，极度危险的地方，到过那的人没有一个能活着回来。
        这个时候，一个叫卡尔的年轻人主动上前，表示愿意试一试。
        国王说，年轻人那就拜托你了，魔塔离这里路途遥远，不过我可以用时光之杖直接送你过去。
        只见一道白光，你被传送到了魔塔。
        """
        raw_input('>')
        print u"""
        你来到了魔塔，这里阴森恐怖，有很多怪物在这出没，也有一些地方藏着很厉害的武器，
        你要试着去找到那些武器让自己变得更加强大，挑战不同的怪物让自己升级，才能让自己
        有足够能力打败魔王！
        在游戏中，Q键可以查看你和怪物的属性，战斗预测可以告诉你打败怪物会消耗的血量。
        E键可以查看小地图，了解你在地图中的位置。
        游戏开始了，加油！
        """
        raw_input('>')
        now_room = None
        next_room = self.tower.first_room
        while True:
            room = self.tower.enter_room(next_room,now_room)
            now_room = next_room
            next_room = room

#魔塔类
class Tower(object):
    def __init__(self,first_room):
        self.room = {"room1":Room1(),"room2":Room2(),"room3":Room3(),
                "room4":Room4(),"room5":Room5(),"room6":Room6(),
                "room7":Room7(),"room8":Room8(),"room9":Room9(),
                "basement":basement(),"palace":palace()}
        self.first_room = first_room

    def enter_room(self,next_room,now_room):
        next_room = self.room.get(next_room)
        return next_room.enter(now_room)

#房间类
class Room(object):
    room_dict = {'room1':1,'room2':2,'room3':3,'room4':4,
                'room5':5,'room6':6,'room7':7,'room8':8,
                'room9':9,'palace':-1,'basement':11}
    toward_dict = {"w":"up","s":"down",
                   "a":"left","d":"right","f":"middle"}
    open_flag = 0
    def enter(self,last_room):
#显示房间剧情
        print "---------------------------------------------\n"
        num = re.findall(r"\d",self.room_name)
        if num == []:
            if self.room_name == "palace":
                print u"宫殿"
            else:
                print u"地下室"
        else:
            print u"进入房间%s" % num[0]
        print self.words

#获取玩家在房间的位置
        self.player_pos = self.get_playerpos(last_room)
#显示房间样子
        display.display_room(self.player_pos,self.monster,self.monster_pos,
        self.door_pos,self.goods)
#如果去过地下室，则可以进入宫殿
        if self.room_name == "basement":
            Room.open_flag = 1
#进入玩家选择循环
        while True:
            print u"请选择：1、搜索物品  2、消灭怪物  3、离开房间"
            print u"Q键查看玩家属性  E键显示小地图"
            choose0 = raw_input('>')
            if choose0 == "q":
                display.display_property(self.monster)
            elif choose0 == "e":
                display.display_pos(self.room_name)
            elif choose0 == "1":
                fight.find_goods(self.goods)
                self.goods = []
            elif choose0 == "2":
                print u"请选择你要挑战的怪物：W、上 S、下 A、左 D、右  F、中  R、返回"
                choose1 = raw_input('>')
                if choose1 == "r":
                    continue
                monster_toward = Room.toward_dict.get(choose1)
                if monster_toward not in self.monster_pos:
                    print u"那里没有怪物。"
                    continue
                fight.fight(self.monster)
                self.monster_pos.remove(monster_toward)
            elif choose0 == "3":
                print u"请选择你要进入的房间：W、上 S、下 A、左 D、右    R、返回"
                choose2 = raw_input('>')
                if choose2 == "r":
                    continue
                door_toward = Room.toward_dict.get(choose2)
                if door_toward not in self.door_pos:
                    print u"那是一堵墙。"
                    continue
                if door_toward in self.monster_pos:
                    print u"你必须打败门前的怪物，才能进去。"
                    continue
                #根据方向得到下个房间的名字
                num_dict = {"up":-3,"down":3,
                               "left":-1,"right":1}
                next_roomnum = Room.room_dict.get(self.room_name)
                next_roomnum += num_dict.get(door_toward)
                for key,value in Room.room_dict.items():
                    if value == next_roomnum:
                        next_room =  key
                        break
                if next_room == "palace" and Room.open_flag == 0:
                    print u"这个地方感觉很危险，我还是等会再进去吧~"
                    continue
                return next_room
            else:
                print u"指令错误。"

    def get_playerpos(self,last_room):
        if last_room == None:
            return "middle"
        last_roomnum = Room.room_dict.get(last_room)
        now_roomnum = Room.room_dict.get(self.room_name)
        num = now_roomnum - last_roomnum
        if num == 3:
            return "up"
        elif num == 1:
            return "left"
        elif num == -1:
            return "right"
        elif num == -3:
            return "down"
        else:
            print u"无法确定玩家位置！"

#房间1
class Room1(Room):
    def __init__(self):
        self.room_name = "room1"
        self.goods = [u"圣剑",u"中血瓶"]
        self.monster = ""
        self.monster_pos = []
        self.door_pos = ["right"]
        self.words = u"这是个存放物品的房间，说不定藏着什么好东西！"



#房间2
class Room2(Room):
    def __init__(self):
        self.room_name = "room2"
        self.goods = []
        self.monster = u"巫师"
        self.monster_pos = ["left","middle","up","right"]
        self.door_pos = ["left","up","down"]
        self.words = u"房间里似乎有一些可怕的生物，你要打败门口的怪物，才能打开相应的门。"

#房间3
class Room3(Room):
    def __init__(self):
        self.room_name = "room3"
        self.goods = [u"圣盾",u"超大血瓶"]
        self.monster = ""
        self.monster_pos = []
        self.door_pos = ["down"]
        self.words = u"这是个存放物品的房间，说不定藏着什么好东西！"

#房间4
class Room4(Room):
    def __init__(self):
        self.room_name = "room4"
        self.goods = []
        self.monster = u"史莱姆"
        self.monster_pos = ["left","middle","up","down"]
        self.door_pos = ["right","down"]
        self.words = u"房间里似乎有一些可怕的生物，你要打败门口的怪物，才能打开相应的门。"

#房间5
class Room5(Room):
    def __init__(self):
        self.room_name = "room5"
        self.goods = []
        self.monster = ""
        self.monster_pos = []
        self.door_pos = ["left","right","up","down"]
        self.words = u"这是一个空荡荡的房间，可以通向四面八方。"

#房间6
class Room6(Room):
    def __init__(self):
        self.room_name = "room6"
        self.goods = []
        self.monster = u"小魔王"
        self.monster_pos = ["up"]
        self.door_pos = ["left","up"]
        self.words = u"你走进了小恶魔的房间，这是魔塔里十分强大的怪物，最好不要惹他。"

#房间7
class Room7(Room):
    def __init__(self):
        self.room_name = "room7"
        self.goods = [u"小血瓶"]
        self.monster = ""
        self.monster_pos = []
        self.door_pos = ["up"]
        self.words = u"这是个存放物品的房间，说不定藏着什么好东西！"

#房间8
class Room8(Room):
    def __init__(self):
        self.room_name = "room8"
        self.goods = []
        self.monster = u"骑士"
        self.monster_pos = ["left","down","right","middle"]
        self.door_pos = ["down","up","right"]
        self.words = u"房间里似乎有一些可怕的生物，你要打败门口的怪物，才能打开相应的门。"

#房间9
class Room9(Room):
    def __init__(self):
        self.room_name = "room9"
        self.goods = [u"大血瓶",u"圣水"]
        self.monster = ""
        self.monster_pos = []
        self.door_pos = ["left"]
        self.words = u"这是个存放物品的房间，说不定藏着什么好东西！"

#地下室
class basement(Room):
    def __init__(self):
        self.room_name = "basement"
        self.goods = []
        self.monster = u"公主"
        self.monster_pos = ["middle"]
        self.door_pos = ["up"]
        self.words = u"""
        这是一个的地下室，有个人被囚禁在其中。原来是公主！
        你叫醒了公主，说到"公主，我是你父王派来救你的，快跟我走吧！"
        公主揉了揉眼睛，说："非常感谢你英雄，可是我被魔王用法术禁锢在这里了，
        只有打败大魔王，才能离开。大魔王的位置在地图最上边的神秘房间里，
        那个地方十分危险，在进去之前一定要做好充分的准备！"
        "恩，等我的好消息吧！"，你说到。
        """
""
#魔王宫殿
class palace(Room):
    def __init__(self):
        self.room_name = "palace"
        self.goods = []
        self.monster = u"大魔王"
        self.monster_pos = ["middle"]
        self.door_pos = []
        self.words = u"""你走进了大魔王的宫殿。
        "年轻人，你终于来了，我等你很久了。我要告诉你一个不幸的消息，这个房子不打败我
        是无法离开的。哈哈哈，乖乖受死吧！"
        """

#角色类
class Role(object):
    pass




tower = Tower("room5")
game = Engine(tower)
game.play()
