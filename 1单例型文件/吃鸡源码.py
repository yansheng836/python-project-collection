# coding=utf-8
import os
import json
import datetime
import math
 
from conf import settings
 
 
class UserTeamTypeData:
    def __init__(self, team_type, player_count):
        self.team_type = team_type
        self.player_count = player_count
        self.label = {}
        self.dead_poison_circle_no = {}
        self.count = 0
        self.damage = 0
        self.survival_duration = 0  # 生存时间
        self.driving_distance = 0
        self.forward_distance = 0
        self.times_assist = 0  # 助攻
        self.times_head_shot = 0
        self.times_kill = 0
        self.times_reborn = 0  # 被救次数
        self.times_save = 0  # 救人次数
        self.top_kill_distance = []
        self.top_kill_distance_weapon_use = {}
        self.vehicle_kill = 0  # 车辆杀死
        self.award_gold = 0
        self.times_reborn_by_role_sex = {0: 0, 1: 0}  # 0 男 1 女
        self.times_save_by_role_sex = {0: 0, 1: 0}  # 0 男 1 女
 
    def update_dead_poison_circle_no(self, dead_poison_circle_no):
        if dead_poison_circle_no in self.dead_poison_circle_no:
            self.dead_poison_circle_no[dead_poison_circle_no] += 1
        else:
            self.dead_poison_circle_no[dead_poison_circle_no] = 1
 
    def update_times_reborn_and_save_by_role_sex(self, role, times_reborn, times_save):
        if role not in self.times_reborn_by_role_sex:
            return
 
        self.times_reborn_by_role_sex[role] += times_reborn
        self.times_save_by_role_sex[role] += times_save
 
    def update_top_kill_distance_weapon_use(self, weaponid):
        if weaponid not in self.top_kill_distance_weapon_use:
            self.top_kill_distance_weapon_use[weaponid] = 1
        else:
            self.top_kill_distance_weapon_use[weaponid] += 1
 
 
class UserBattleData:
 
    def __init__(self, openid):
        self.openid = openid
        self.team_type_res = {}
        self.label = {}
        self.hour_counter = {}
        self.weekday_counter = {}
        self.usetime = 0
        self.day_record = set()
        self.battle_counter = 0
 
    def get_avg_use_time_per_day(self):
        # print "get_avg_use_time_per_day:", self.openid, self.usetime, len(self.day_record), self.usetime / len(self.day_record)
        return self.usetime / len(self.day_record)
 
    def update_label(self, lable):
        if lable in self.label:
            self.label[lable] += 1
        else:
            self.label[lable] = 1
 
    def get_team_type_data(self, team_type, player_count):
        player_count = int(math.ceil(float(player_count) / 10))
        team_type_key = '%d_%d' % (team_type, player_count)
 
        if team_type_key not in self.team_type_res:
            userteamtypedata = UserTeamTypeData(team_type, player_count)
            self.team_type_res[team_type_key] = userteamtypedata
        else:
            userteamtypedata = self.team_type_res[team_type_key]
 
        return userteamtypedata
 
    def update_user_time_property(self, dt_event_time):
        dt_event_time = datetime.datetime.fromtimestamp(dt_event_time)
        hour = dt_event_time.hour
        if hour in self.hour_counter:
            self.hour_counter[hour] += 1
        else:
            self.hour_counter[hour] = 1
 
        weekday = dt_event_time.weekday()
        if weekday in self.weekday_counter:
            self.weekday_counter[weekday] += 1
        else:
            self.weekday_counter[weekday] = 1
 
        self.day_record.add(dt_event_time.date())
 
    def update_battle_info_by_room(self, roomid):
        # print '  load ', self.openid, roomid
        file = os.path.join(settings.Res_UserBattleInfo_Dir, self.openid, '%s.txt' % roomid)
 
        with open(file, 'r') as rf:
            battledata = json.load(rf)
 
        self.battle_counter += 1
        base_info = battledata['base_info']
        self.update_user_time_property(base_info['dt_event_time'])
        battle_info = battledata['battle_info']
 
        userteamtypedata = self.get_team_type_data(base_info['team_type'], base_info['player_count'])
        userteamtypedata.count += 1
        userteamtypedata.award_gold += battle_info['award_gold']
        userteamtypedata.damage += battle_info['damage']
        userteamtypedata.update_dead_poison_circle_no(battle_info['dead_poison_circle_no'])
        userteamtypedata.driving_distance += battle_info['driving_distance']
        userteamtypedata.forward_distance += battle_info['forward_distance']
        self.update_label(battle_info['label'])
        userteamtypedata.survival_duration += battle_info['survival_duration']
        self.usetime += battle_info['survival_duration']/60
        userteamtypedata.times_assist += battle_info['times_assist']
        userteamtypedata.times_head_shot += battle_info['times_head_shot']
        userteamtypedata.times_kill += battle_info['times_kill']
        userteamtypedata.times_reborn += battle_info['times_reborn']
        userteamtypedata.times_save += battle_info['times_save']
        userteamtypedata.damage += battle_info['damage']
        userteamtypedata.top_kill_distance.append(battle_info['top_kill_distance'])
        userteamtypedata.update_times_reborn_and_save_by_role_sex(base_info['role_sex'], battle_info['times_reborn'],
                                                                  battle_info['times_save'])
 
    def get_user_battleinfo_rooms(self):
        user_dir = os.path.join(settings.Res_UserBattleInfo_Dir, self.openid)
        r = [room for room in os.listdir(user_dir)]
        r = [rr.replace('.txt', '') for rr in r]
        return r
 
class AllUserCounter:
 
    def __init__(self):
        self.hour_counter = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0}
 
        self.weekday_counter = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        self.times_reborn_by_role_sex = {0: 0, 1: 0}  # 0 男 1 女
        self.times_save_by_role_sex = {0: 0, 1: 0}  # 0 男 1 女
        self.user_count = 0
        self.battle_count = 0
        self.every_user_use_time_per_day = []
        self.top_kill_distance = 0
 
    def avg_use_time(self):
        return sum(self.every_user_use_time_per_day) / len(self.every_user_use_time_per_day)
 
    def add_user_data(self, userbattledata):
        self.every_user_use_time_per_day.append(userbattledata.get_avg_use_time_per_day())
        self.battle_count += userbattledata.battle_counter
        self.user_count += 1
 
        for k in userbattledata.hour_counter:
            if k in self.hour_counter:
                self.hour_counter[k] += userbattledata.hour_counter[k]
            else:
                self.hour_counter[k] = userbattledata.hour_counter[k]
 
        for weekday in userbattledata.weekday_counter:
            if weekday in self.weekday_counter:
                self.weekday_counter[weekday] += userbattledata.weekday_counter[weekday]
            else:
                self.weekday_counter[weekday] = userbattledata.weekday_counter[weekday]
 
        for userteamtype in userbattledata.team_type_res:
            userteamtypedata = userbattledata.team_type_res[userteamtype]
            for k in userteamtypedata.times_reborn_by_role_sex:
                self.times_reborn_by_role_sex[k] += userteamtypedata.times_reborn_by_role_sex[k]
 
            for k in userteamtypedata.times_save_by_role_sex:
                self.times_save_by_role_sex[k] += userteamtypedata.times_save_by_role_sex[k]
 
            if userteamtypedata.top_kill_distance > self.top_kill_distance:
                self.top_kill_distance = userteamtypedata.top_kill_distance
 
    def __str__(self):
        res = []
        res.append('总用户数\t%d' % self.user_count)
        res.append('总战斗数\t%d' % self.battle_count)
        res.append('平均日耗时\t%d' % self.avg_use_time())
        res.append('最远击杀\t%d' % max(self.top_kill_distance))
        res.append('男性角色\t被救%d次\t救人%d次' % (self.times_reborn_by_role_sex[0], self.times_save_by_role_sex[0]))
        res.append('女性角色\t被救%d次\t救人%d次' % (self.times_reborn_by_role_sex[1], self.times_save_by_role_sex[1]))
 
        res.append('小时分布')
        for hour in range(0, 24):
            # res.append('\t%d: %d' % (hour, self.hour_counter[hour]))
            res.append('\t%d: %d %.2f%%' % (hour, self.hour_counter[hour], self.hour_counter[hour]/float(self.battle_count)*100))
        res.append('星期分布')
        # res.append(self.weekday_counter.__str__())
        for weekday in range(0, 7):
            res.append('\t%d: %d %.2f%%' % (weekday+1, self.weekday_counter[weekday], (self.weekday_counter[weekday]/float(self.battle_count)*100)))
 
        return '\n'.join(res)
 
 
def get_user_battleinfo_rooms(openid):
    user_dir = os.path.join(settings.Res_UserBattleInfo_Dir, openid)
 
    # files = os.listdir(user_dir)
    r = [room for room in os.listdir(user_dir)]
    r = [rr.replace('.txt', '') for rr in r]
    return r
 
 
if __name__ == '__main__':
    alluserconter = AllUserCounter()
    
    folders = os.listdir(settings.Res_UserBattleInfo_Dir)
    i = 0
    for folder in folders:
        i+=1
        print i, '/' , len(folders), folder
        userbattledata = UserBattleData(folder)
        for room in userbattledata.get_user_battleinfo_rooms():
            userbattledata.update_battle_info_by_room(room)
        alluserconter.add_user_data(userbattledata)
 
    print "\n" * 3
    print "---------------------------------------"
 
    print alluserconter