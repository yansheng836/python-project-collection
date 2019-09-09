#热力图
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.misc.pilutil import imread
import matplotlib.cm as cm

#导入部分数据
deaths1 = pd.read_csv("deaths/kill_match_stats_final_0.csv")
deaths2 = pd.read_csv("deaths/kill_match_stats_final_1.csv")

deaths = pd.concat([deaths1, deaths2])

#打印前5列，理解变量
print (deaths.head(),'\n',len(deaths))

#两种地图
miramar = deaths[deaths["map"] == "MIRAMAR"]
erangel = deaths[deaths["map"] == "ERANGEL"]

#开局前100秒死亡热力图
position_data = ["killer_position_x","killer_position_y","victim_position_x","victim_position_y"]
for position in position_data:
    miramar[position] = miramar[position].apply(lambda x: x*1000/800000)
    miramar = miramar[miramar[position] != 0]

    erangel[position] = erangel[position].apply(lambda x: x*4096/800000)
    erangel = erangel[erangel[position] != 0]

n = 50000
mira_sample = miramar[miramar["time"] < 100].sample(n)
eran_sample = erangel[erangel["time"] < 100].sample(n)

# miramar热力图
bg = imread("miramar.jpg")
fig, ax = plt.subplots(1,1,figsize=(15,15))
ax.imshow(bg)
sns.kdeplot(mira_sample["victim_position_x"], mira_sample["victim_position_y"],n_levels=100, cmap=cm.Reds, alpha=0.9)

# erangel热力图
bg = imread("erangel.jpg")
fig, ax = plt.subplots(1,1,figsize=(15,15))
ax.imshow(bg)
sns.kdeplot(eran_sample["victim_position_x"], eran_sample["victim_position_y"], n_levels=100,cmap=cm.Reds, alpha=0.9)


#苟吃鸡？

library(dplyr)
library(tidyverse)
library(data.table)
library(ggplot2)
pubg_full <- fread("../agg_match_stats.csv")
# 吃鸡团队平均击杀敌人的数量
attach(pubg_full)
pubg_winner <- pubg_full %>% filter(team_placement==1&party_size<4&game_size>90) 
detach(pubg_full)
team_killed <- aggregate(pubg_winner$player_kills, by=list(pubg_winner$match_id,pubg_winner$team_id), FUN="mean")
team_killed$death_num <- ceiling(team_killed$x)
ggplot(data = team_killed) + geom_bar(mapping = aes(x = death_num, y = ..count..), color="steelblue") +
  xlim(0,70) + labs(title = "Number of Death that PUBG Winner team Killed", x="Number of death")

# 吃鸡团队最后存活的玩家击杀数量
pubg_winner <- pubg_full %>% filter(pubg_full$team_placement==1) %>% group_by(match_id,team_id)
attach(pubg_winner)
team_leader <- aggregate(player_survive_time~player_kills, data = pubg_winner, FUN="max")
detach(pubg_winner)

#吃鸡团队中击杀敌人最多的数量
pubg_winner <- pubg_full %>% filter(pubg_full$team_placement==1&pubg_full$party_size>1)
attach(pubg_winner)
team_leader <- aggregate(player_kills, by=list(match_id,team_id), FUN="max")
detach(pubg_winner)
ggplot(data = team_leader) + geom_bar(mapping = aes(x = x, y = ..count..), color="steelblue") +
  xlim(0,70) + labs(title = "Number of Death that PUBG Winner Killed", x="Number of death")


#杀人武器排名
death_causes = deaths['killed_by'].value_counts()

sns.set_context('talk')
fig = plt.figure(figsize=(30, 10))
ax = sns.barplot(x=death_causes.index, y=[v / sum(death_causes) for v in death_causes.values])
ax.set_title('Rate of Death Causes')
ax.set_xticklabels(death_causes.index, rotation=90)

#排名前20的武器
rank = 20
fig = plt.figure(figsize=(20, 10))
ax = sns.barplot(x=death_causes[:rank].index, y=[v / sum(death_causes) for v in death_causes[:rank].values])
ax.set_title('Rate of Death Causes')
ax.set_xticklabels(death_causes.index, rotation=90)

#两个地图分开取
f, axes = plt.subplots(1, 2, figsize=(30, 10))
axes[0].set_title('Death Causes Rate: Erangel (Top {})'.format(rank))
axes[1].set_title('Death Causes Rate: Miramar (Top {})'.format(rank))

counts_er = erangel['killed_by'].value_counts()
counts_mr = miramar['killed_by'].value_counts()

sns.barplot(x=counts_er[:rank].index, y=[v / sum(counts_er) for v in counts_er.values][:rank], ax=axes[0] )
sns.barplot(x=counts_mr[:rank].index, y=[v / sum(counts_mr) for v in counts_mr.values][:rank], ax=axes[1] )
axes[0].set_ylim((0, 0.20))
axes[0].set_xticklabels(counts_er.index, rotation=90)
axes[1].set_ylim((0, 0.20))
axes[1].set_xticklabels(counts_mr.index, rotation=90)

#吃鸡和武器的关系
win = deaths[deaths["killer_placement"] == 1.0]
win_causes = win['killed_by'].value_counts()

sns.set_context('talk')
fig = plt.figure(figsize=(20, 10))
ax = sns.barplot(x=win_causes[:20].index, y=[v / sum(win_causes) for v in win_causes[:20].values])
ax.set_title('Rate of Death Causes of Win')
ax.set_xticklabels(win_causes.index, rotation=90)

#救队友
library(dplyr)
library(tidyverse)
library(data.table)
library(ggplot2)
pubg_full <- fread("E:/aggregate/agg_match_stats_0.csv")
attach(pubg_full)
pubg_winner <- pubg_full %>% filter(team_placement==1) 
detach(pubg_full)
ggplot(data = pubg_winner) + geom_bar(mapping = aes(x = player_assists, y = ..count..), fill="#E69F00") +
  xlim(0,10) + labs(title = "Number of Player assisted", x="Number of death")
11ggplot(data = pubg_winner) + geom_bar(mapping = aes(x = player_assists, y = ..prop..), fill="#56B4E9") +
  xlim(0,10) + labs(title = "Number of Player assisted", x="Number of death")


# python代码：杀人和距离的关系
import math
def get_dist(df): #距离函数
    dist = []
    for row in df.itertuples():
        subset = (row.killer_position_x - row.victim_position_x)**2 + (row.killer_position_y - row.victim_position_y)**2
        if subset > 0:
            dist.append(math.sqrt(subset) / 100)
        else:
            dist.append(0)
    return dist

df_dist = pd.DataFrame.from_dict({'dist(m)': get_dist(erangel)})
df_dist.index = erangel.index

erangel_dist = pd.concat([erangel,df_dist], axis=1)

df_dist = pd.DataFrame.from_dict({'dist(m)': get_dist(miramar)})
df_dist.index = miramar.index

miramar_dist = pd.concat([miramar,df_dist], axis=1)

f, axes = plt.subplots(1, 2, figsize=(30, 10))
plot_dist = 150

axes[0].set_title('Engagement Dist. : Erangel')
axes[1].set_title('Engagement Dist.: Miramar')

plot_dist_er = erangel_dist[erangel_dist['dist(m)'] <= plot_dist]
plot_dist_mr = miramar_dist[miramar_dist['dist(m)'] <= plot_dist]

sns.distplot(plot_dist_er['dist(m)'], ax=axes[0])
sns.distplot(plot_dist_mr['dist(m)'], ax=axes[1])


# R语言代码如下：
library(magrittr)
library(dplyr)
library(survival)
library(tidyverse)
library(data.table)
library(ggplot2)
library(survminer)
pubg_full <- fread("../agg_match_stats.csv")
# 数据预处理，将连续变量划为分类变量
pubg_sub <- pubg_full %>%
  filter(player_survive_time<2100) %>%
  mutate(drive = ifelse(player_dist_ride>0, 1, 0)) %>%
  mutate(size = ifelse(game_size<33, 1,ifelse(game_size>=33 &game_size<66,2,3)))
# 创建生存对象
surv_object <- Surv(time = pubg_sub$player_survive_time)
fit1 <- survfit(surv_object~party_size,data = pubg_sub)
# 可视化生存率
ggsurvplot(fit1, data = pubg_sub, pval = TRUE, xlab="Playing time [s]", surv.median.line="hv",
           legend.labs=c("SOLO","DUO","SQUAD"), ggtheme = theme_light(),risk.table="percentage")
fit2 <- survfit(surv_object~drive,data=pubg_sub)
ggsurvplot(fit2, data = pubg_sub, pval = TRUE, xlab="Playing time [s]", surv.median.line="hv",
           legend.labs=c("walk","walk&drive"), ggtheme = theme_light(),risk.table="percentage")
fit3 <- survfit(surv_object~size,data=pubg_sub)
ggsurvplot(fit3, data = pubg_sub, pval = TRUE, xlab="Playing time [s]", surv.median.line="hv",
           legend.labs=c("small","medium","big"), ggtheme = theme_light(),risk.table="percentage")


#最后毒圈位置
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.misc.pilutil import imread
import matplotlib.cm as cm

#导入部分数据
deaths = pd.read_csv("deaths/kill_match_stats_final_0.csv")
#导入aggregate数据
aggregate = pd.read_csv("aggregate/agg_match_stats_0.csv")
print(aggregate.head())
#找出最后三人死亡的位置

team_win = aggregate[aggregate["team_placement"]==1] #排名第一的队伍
#找出每次比赛第一名队伍活的最久的那个player
grouped = team_win.groupby('match_id').apply(lambda t: t[t.player_survive_time==t.player_survive_time.max()])

deaths_solo = deaths[deaths['match_id'].isin(grouped['match_id'].values)]
deaths_solo_er = deaths_solo[deaths_solo['map'] == 'ERANGEL']
deaths_solo_mr = deaths_solo[deaths_solo['map'] == 'MIRAMAR']

df_second_er = deaths_solo_er[(deaths_solo_er['victim_placement'] == 2)].dropna()
df_second_mr = deaths_solo_mr[(deaths_solo_mr['victim_placement'] == 2)].dropna()
print (df_second_er)

position_data = ["killer_position_x","killer_position_y","victim_position_x","victim_position_y"]
for position in position_data:
    df_second_mr[position] = df_second_mr[position].apply(lambda x: x*1000/800000)
    df_second_mr = df_second_mr[df_second_mr[position] != 0]

    df_second_er[position] = df_second_er[position].apply(lambda x: x*4096/800000)
    df_second_er = df_second_er[df_second_er[position] != 0]

df_second_er=df_second_er
# erangel热力图
sns.set_context('talk')
bg = imread("erangel.jpg")
fig, ax = plt.subplots(1,1,figsize=(15,15))
ax.imshow(bg)
sns.kdeplot(df_second_er["victim_position_x"], df_second_er["victim_position_y"], cmap=cm.Blues, alpha=0.7,shade=True)

# miramar热力图
bg = imread("miramar.jpg")
fig, ax = plt.subplots(1,1,figsize=(15,15))
ax.imshow(bg)
sns.kdeplot(df_second_mr["victim_position_x"], df_second_mr["victim_position_y"], cmap=cm.Blues,alpha=0.8,shade=True)