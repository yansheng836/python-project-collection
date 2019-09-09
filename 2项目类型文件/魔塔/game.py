# -*- coding:utf-8 -*-
import display
import fight
class Room(object):
    def choose_do(self,lastroom):

        #根据上个房间的号码和当前房间号码的差得到当前玩家在房间里的位置
        compare = lastroom - self.roomnum
        if compare == -3:
            self.player_pos = "up"
        elif compare == -1:
            self.player_pos = "left"
        elif compare == 1:
            self.player_pos = "right"
        elif compare == 3:
            self.player_pos = "down"
        else:
            pass

        #显示房间场景
        display.display_room(self.player_pos,self.monster,
                        self.monster_pos,self.door_pos,self.goods)

        while True:
            print u"你可以选择：1、搜索房间  2、离开房间  3、查看小地图  4、查看自己的属性 5、消灭怪物"
            choice = raw_input(">")
            if choice == '1':
                if self.goods != []:
                    print self.word
                    fight.use_goods(self.goods)
                    self.goods = []
                else:
                    print u"\t什么也没有！\n"
            elif choice == '2':
                while True:
                    print u"请选择你要进入的房间：W:上 A:左 S：下 D：右 Q:返回"
                    choose_room = raw_input('>')

                    if choose_room == "w":
                        choose_room = "up"
                    elif choose_room == "a":
                        choose_room = "left"
                    elif choose_room == "s":
                        choose_room = "down"
                    elif choose_room == "d":
                        choose_room = "right"
                    elif choose_room == 'q':
                        break
                    else:
                        pass

                    if choose_room not in self.door_pos:
                        print u"选择错误！"
                    else:
                        if choose_room in self.monster_pos:
                            print u"你必须打败门口的守卫，才能进入这个房间！"
                        else:
                            if choose_room == "up":
                                return self.roomnum - 3
                            elif choose_room == "left":
                                return self.roomnum - 1
                            elif choose_room == "down":
                                return self.roomnum + 3
                            elif choose_room == "right":
                                return self.roomnum + 1
                            else:
                                pass
            elif choice == '3':
                display.display_pos(self.roomnum)
            elif choice == '4':
                display.display_property(self.monster)
            elif choice == '5':
                if self.monster_pos == []:
                    print u"没有怪物！"
                else:
                    print u"请选择你要攻击的怪物：W:上 A:左 S：下 D：右  E:中 Q:返回"
                    choose_monster = raw_input('>')

                    if choose_monster == "w":
                        choose_monster = "up"
                    elif choose_monster == "a":
                        choose_monster = "left"
                    elif choose_monster == "s":
                        choose_monster = "down"
                    elif choose_monster == "d":
                        choose_monster = "right"
                    elif choose_monster == "e":
                        choose_monster = "middle"
                    elif choose_monster == 'q':
                        continue
                    else:
                        pass
                    if choose_monster not in self.monster_pos:
                        print u"这个地方没有怪物!"
                        continue
                    fight.fight(self.monster)
                    self.monster_pos.remove(choose_monster)
            else:
                print u"输入错误！"

class Room1(Room):
    def __init__(self):
        self.roomnum = 1
        self.player_pos = "right"
        self.goods = [u"圣剑",u"钥匙",u"中血瓶"]
        self.monster = 0
        self.monster_pos = []
        self.door_pos = ["right"]
        self.word = u"""
得到一把圣剑 +---，攻击力上升100！
得到一个中血瓶 (oo)，生命值上升200！
得到一把钥匙 C=--！
        """
    def story_room(self,lastroom):
        u"""
        函数功能：交代room1剧情，显示房间场景，获取用户选择，做相应处理。
        输入参数：无
        返回参数：self.nextroom--下个房间的号码，类型--数字类型
        0--神秘房间   10--地下室
        """
        print u"房间1"
        if self.goods != []:
            print u"你进入了一个昏暗的房间，房间里似乎有一些东西在发光！"
        else:
            print u"你进入了一个昏暗的房间，房间里空无一物。"
        #进入游戏循环
        return Room.choose_do(self,lastroom)

class Room2(Room):
    def __init__(self):
        self.roomnum = 2
        self.player_pos = " "
        self.goods = []
        self.monster = u"巫师"
        self.monster_pos = ["up","middle","left","right"]
        self.door_pos = ["left","up","down"]
        self.word = u"""
        """
    def story_room(self,lastroom):
        u"""
        函数功能：交代room2剧情，显示房间场景，获取用户选择，做相应处理。
        输入参数：无
        返回参数：self.nextroom--下个房间的号码，类型--数字类型
        -1--神秘房间   11--地下室
        """
        #剧情交代
        print u"房间2"
        if self.monster_pos != []:
            print u"你进入了一个昏暗的房间，房间里似乎有一些可怕的生物！"
        else:
            print u"你进入了一个昏暗的房间，房间里空无一物。"
        #进入游戏循环
        return Room.choose_do(self,lastroom)
# room1 = Room1(1)
# room1.story_room1()

#启动游戏的类
class Game(object):
    def start(self):
        last_room = 1
        room1 = Room1()
        room2 = Room2()
        nextroom = room1.story_room(last_room)
        while True:
            if nextroom == 1:
                nextroom = room1.story_room(last_room)
                last_room = 1
            elif nextroom == 2:
                nextroom = room2.story_room(last_room)
                last_room = 2
            else:
                pass

playgame = Game()
playgame.start()
