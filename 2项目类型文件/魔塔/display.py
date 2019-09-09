# -*- coding:utf-8 -*-
import copy
import fight

u"""
这个模块提供一些实现显示功能的函数。
"""

def display_pos(room):
    u"""
    函数功能：显示当前所在位置
    输入参数：room--房间号 ，类型--字符串
    """
    room_dict = {'room1':1,'room2':2,'room3':3,'room4':4,'room5':5,
                 'room6':6,'room7':7,'room8':8,'room9':9,
                 'palace':0,'basement':10}
    pos = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
    pos[room_dict.get(room)] = 2
    print u"""
        ================
        |   神秘房间   |
        |      %c       |
    ==========---===========
    | 房间1 | 房间2 | 房间3 |
    |  %c    |  %c    |  %c    |
    |       |       |       |
    |=======|=======|=======|
    | 房间4 | 房间5 | 房间6 |
    |  %c    |  %c    |  %c    |
    |       |       |       |
    |=======|=======|=======|
    | 房间7 | 房间8 | 房间9 |
    |  %c    |  %c    |  %c    |
    |       |       |       |
    ===========---===========
        |    地下室    |
        |      %c       |
        ================
    """ % (pos[0],pos[1],pos[2],pos[3],pos[4],pos[5],pos[6],pos[7],pos[8],pos[9],pos[10])



def display_room(player_pos,monster,monster_pos,door_pos,goods):
    u"""
    函数功能：显示房间内的景象。
    输入参数：
    玩家的位置--player_pos，类型--字符串,有效的值--"up","left","right","down","middle",0（不存在）

    怪物的种类--monster，类型--字符串
        有效的值：  "史莱姆"   ~0Y0~
                   "巫师"   >@Y@<
                   "骑士"   \OYO/
                   "小魔王"  ~/-Y-\~
                   "大魔王"  ~~//-Y-\\\~~
                   "公主"   ^o^
                   ""     不存在怪物

    怪物的位置--monster_pos,类型--列表  空列表表示不存在怪物
    列表中每个元素，代表一个怪物的位置，类型--字符串,有效的值--"up","left","right","down","middle"

    门的位置--door_pos,类型--列表     空列表表示不存在门
    列表中每个元素--代表一个门的位置，类型--字符串,有效的值--"up","left","right","down"

    物品的种类--goods,类型--列表     空列表表示不存在物品
    列表中每个元素--代表一种物品，类型--字符串
        有效的值："Excalibur" 圣剑   +---
                 "圣盾"       [+]
                 "钥匙"    C=--
                 "小血瓶"    (o)
                 "中血瓶"    (oo)
                 "大血瓶"    (ooo)
                 "超大血瓶"    (oooo)
                 "圣水"   [o]
                 "地图"    [|]

    备注：玩家图形：  (^_^)
    """
    drawlist = []
    good_pos = [6,7,9]
    for i in range(14):
        drawlist.append('  ')

    if player_pos == "up":          #根据输入参数，让玩家图形在对应的位置显示
        drawlist[2] = convert_sign(fight.player_property[u"符号"])
    elif player_pos == "down":
         drawlist[12] = convert_sign(fight.player_property[u"符号"])
    elif player_pos == "left":
         drawlist[5] = convert_sign(fight.player_property[u"符号"])
    elif player_pos == "right":
         drawlist[10] = convert_sign(fight.player_property[u"符号"])
    elif player_pos == "middle":
         drawlist[7] = convert_sign(fight.player_property[u"符号"])
    else:
        print u"玩家位置错误！"

    if monster == u"史莱姆":      #根据输入参数，设置怪物图形
        monster_sign = convert_sign(fight.Slime_property[u"符号"])
    elif monster == u"巫师":
        monster_sign = convert_sign(fight.wizard_property[u"符号"])
    elif monster == u"骑士":
        monster_sign = convert_sign(fight.knight_property[u"符号"])
    elif monster == u"公主":
        monster_sign = convert_sign(fight.princess_property[u"符号"])
    elif monster == u"小魔王":
        monster_sign = convert_sign(fight.s_devil_property[u"符号"])
    elif monster == u"大魔王":
        monster_sign = convert_sign(fight.g_devil_property[u"符号"])
    elif monster == "":
        pass
    else:
        print u"怪物名称错误！"
        monster_sign = convert_sign("  ")

    for mon in monster_pos:           #根据输入参数，让怪物图形在对应的位置显示
        if mon == "up":
            drawlist[2] = monster_sign
        elif mon == "down":
             drawlist[12] = monster_sign
        elif mon == "left":
             drawlist[5] = monster_sign
        elif mon == "right":
             drawlist[10] = monster_sign
        elif mon == "middle":
             drawlist[7] = monster_sign
        else:
            print u"怪物位置错误!"

    for door in door_pos:           #根据输入参数，让门图形在对应的位置显示
        if door == "up":
            drawlist[0] = '_ '
            drawlist[1] = '\b| |'
        elif door == "down":
             drawlist[13] = '\b|_|'
        elif door == "left":
             drawlist[3] = '|\\'
             drawlist[4] = ' \\'
        elif door == "right":
             drawlist[8] = '/|'
             drawlist[11] = '/ '
        else:
            print u"门位置错误!"

    for good in goods:             #根据输入参数判断是什么物品，并显示在指定的位置
        if good == u"圣剑":
            gooddraw = convert_sign("+---")
        elif good == u"圣盾":
            gooddraw = convert_sign("[+]")
        elif good == u"钥匙":
            gooddraw = convert_sign("C=--")
        elif good == u"小血瓶":
            gooddraw = convert_sign("(o)")
        elif good == u"中血瓶":
            gooddraw = convert_sign("(oo)")
        elif good == u"大血瓶":
            gooddraw = convert_sign("(ooo)")
        elif good == u"超大血瓶":
            gooddraw = convert_sign("(oooo)")
        elif good == u"圣水":
            gooddraw = convert_sign("[o]")
        elif good == u"地图":
            gooddraw = convert_sign("[|]")
        else:
            print u"物品名称错误！"
            continue
        drawlist[good_pos.pop(0)] = gooddraw


    draw = (drawlist[0],drawlist[1],drawlist[2],drawlist[3],drawlist[4],
    drawlist[5],drawlist[6],drawlist[7],drawlist[8],drawlist[9],drawlist[10],
    drawlist[11],drawlist[12],drawlist[13])

    print """
    ==================================
    |-                              -|
    | -                   %s       - |
    |  -                  %s      -  |
    |   --------------------------   |
    |   -                  %s    -   |
    |%s -                        -   |
    |%s -    %s       %s         -   |
    |   -             %s         - %s|
    |   -             %s      %s - %s|
    |   -      %s                -   |
    |   --------------------------   |
    | -       %s                   - |
    ==================================
    """ % draw
##输入图形格式转换函数,保证%s所在位置就是字符串的最右端,用于对齐格式
def convert_sign(sign):
    return '\b'*(len(sign)-2) + sign

def display_property(monster):
    u"""
    函数功能：显示玩家和怪物属性
    输入参数：monster--怪物名字，类型：字符串
        有效的值： u"史莱姆"，u"巫师"，u"骑士"，u"小魔王"，u"大魔王",""(不存在怪物)
    """
    monster_exist = True
    #判断是什么怪物
    if monster == fight.Slime_property[u"名字"]:
        monster_property = copy.deepcopy(fight.Slime_property)
    elif monster == fight.wizard_property[u"名字"]:
        monster_property = copy.deepcopy(fight.wizard_property)
    elif monster == fight.knight_property[u"名字"]:
        monster_property = copy.deepcopy(fight.knight_property)
    elif monster == fight.s_devil_property[u"名字"]:
        monster_property = copy.deepcopy(fight.s_devil_property)
    elif monster == fight.g_devil_property[u"名字"]:
        monster_property = copy.deepcopy(fight.g_devil_property)
    elif monster == "":
        monster_exist = False
    else:
        print u"怪物名字输入错误！"
        exit()

    if monster_exist == True:
        draw = (convert_sign(fight.player_property[u"符号"]),convert_sign(fight.player_property[u"名字"]),
        fight.player_property[u"生命值"],fight.player_property[u"攻击力"],fight.player_property[u"护甲"],
        convert_sign(monster_property[u"符号"]),convert_sign(monster_property[u"名字"]),
        monster_property[u"生命值"],monster_property[u"攻击力"],monster_property[u"护甲"],
        fight.forecast_fight(monster_property[u"名字"]))
    else:
        draw = (convert_sign(fight.player_property[u"符号"]),convert_sign(fight.player_property[u"名字"]) ,
        fight.player_property[u"生命值"],fight.player_property[u"攻击力"],
        fight.player_property[u"护甲"],"","","","","","")
    print u"""
    _________________________________________________
              生命值    攻击力    护甲    战斗预测
        %s
      %s      %s       %s       %s

        %s
      %s      %s       %s       %s      %s
    _________________________________________________
    """ % draw


# #测试
# display_property(0)
# display_property(u"史莱姆")
# display_property(u"骑士")
# display_property(u"大魔王")
# # #房间1
# # print u"房间1"
# display_room("right",0,[],["right"],[u"圣剑",u"钥匙",u"中血瓶"])
# # #房间2
# # print u"房间2"
# display_room("down",u"巫师",["left","right","up","middle"],["left","up","down"],[])
# # #房间3
# print u"房间3"
# display_room("down",0,[],["down"],[u"大血瓶",u"圣盾"])
# # #房间4
# print u"房间4"
# display_room("right",u"史莱姆",["left","down","up","middle"],["right","down"],[])
# # #房间5
# print u"房间5"
# display_room("middle",0,[],["up","left","right","down"],[])
# # #房间4
# print u"房间6"
# display_room("left",u"小魔王",["middle"],["left","up"],[])
# # #房间1
# print u"房间7"
# display_room("up",0,[],["up"],[u"地图",u"小血瓶"])
# # #房间8
# print u"房间8"
# display_room("up",u"骑士",["left","down","right","middle"],["up","right","down"],[])
# print u"房间9"
# display_room("left",0,[],["left"],[u"圣水",u"大血瓶"])
# # #恐怖之地
# print u"恐怖之地"
# display_room("down",u"大魔王",["middle"],["down"],[])
# # #地下室
# print u"地下室"
# display_room("up",u"公主",["middle"],["up"],[])
