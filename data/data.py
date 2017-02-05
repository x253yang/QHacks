#!/usr/bin/python

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys, getopt
import indicoio
from sklearn.neighbors import KNeighborsClassifier
indicoio.config.api_key = 'db91e10ba18babcf6e5e5209a5f0ab6f'

subreddit = ""
author = ""
lim = 10
group_s = 0
group_u = 0
tag_list = []
tag_length = 0

sub_list = '''
'AskReddit',
'leagueoflegends',
'nba',
'funny',
'pics',
'nfl',
'pcmasterrace',
'videos',
'news',
'todayilearned',
'DestinyTheGame',
'worldnews',
'soccer',
'DotA2',
'AdviceAnimals',
'WTF',
'GlobalOffensive',
'hockey',
'movies',
'SquaredCircle',
'gaming',
'fatpeoplehate',
'relationships',
'gifs',
'politics',
'CasualConversation',
'explainlikeimfive',
'anime',
'GlobalOffensiveTrade',
'witcher',
'amiibo',
'Fireteams',
'electronic_cigarette',
'asoiaf',
'gameofthrones',
'TumblrInAction',
'trees',
'Showerthoughts',
'hearthstone',
'IAmA',
'Games',
'Fitness',
'newsokur',
'gonewild',
'aww',
'tifu',
'buildapc',
'2007scape',
'AskMen',
'smashbros',
'AskWomen',
'technology',
'thebutton',
'atheism',
'wow',
'MMA',
'KotakuInAction',
'rupaulsdragrace',
'CFB',
'hiphopheads',
'personalfinance',
'unitedkingdom',
'magicTCG',
'Smite',
'Android',
'mildlyinteresting',
'baseball',
'SubredditDrama',
'india',
'PS4',
'europe',
'heroesofthestorm',
'whowouldwin',
'OkCupid',
'TwoXChromosomes',
'csgobetting',
'Bitcoin',
'Music',
'ffxiv',
'Christianity',
'TrollXChromosomes',
'xboxone',
'EliteDangerous',
'nottheonion',
'FIFA',
'television',
'cars',
'motorcycles',
'science',
'canada',
'Random_Acts_Of_Amazon',
'Guildwars2',
'Eve',
'ukpolitics',
'survivor',
'pokemontrades',
'fivenightsatfreddys',
'formula1',
'conspiracy',
'bloodborne'
'''

i = 1
while (i < len(sys.argv)):

    if sys.argv[i] == '-gs':
        group_s = 1
    elif sys.argv[i] == '-gu':
        group_u = 1
    elif (sys.argv[i] == '-help'):
        print("python test.py -s <subreddit> -u <author> -l <limit> -gs -gu")
        sys.exit(0)

    elif i+1 < len(sys.argv):
        if sys.argv[i] == '-s':
            subreddit = sys.argv[i + 1]
        elif sys.argv[i] == '-u':
            author = sys.argv[i + 1]
        elif sys.argv[i] == '-l':
            lim = sys.argv[i + 1]
        elif sys.argv[i] == '-t':
            tag_list.insert(tag_length,sys.argv[i + 1])
            tag_length += 1
        i = i + 2
        continue

    i = i + 1
    continue

conn = sqlite3.connect('../database.sqlite', timeout=60)

def get_sent(x):
    return indicoio.sentiment(x)

def get_emo(x):
    emo = indicoio.emotion(x)
    values = [0,0,0,0,0]
    values[0] = emo.get('anger')
    values[1] = emo.get('joy')
    values[2] = emo.get('fear')
    values[3] = emo.get('sadness')
    values[4] = emo.get('surprise')
    return values

def get_tags(x):
    return indicoio.text_tags(x)


query_string = '''
SELECT * FROM (SELECT id, author, body, subreddit, score from May2015
where LENGTH(body) >= 30 and author is not "[deleted]"'''
if subreddit != "":
    query_string += ' and subreddit = "' + subreddit + '"'

if author != "":
    query_string += ' and author = "' + author + '"'

if group_s:
    query_string += ' group by subreddit'
    if (group_s and group_u):
        query_string += ' and author'
elif group_u:
    query_string += ' group by author'

query_string += ' ORDER BY score ASC'

query_string += ' LIMIT"' + str(lim) + '")'

query_string += ' UNION '

query_string += '''
SELECT * FROM (SELECT id, author, body, subreddit, score
from May2015 where LENGTH(body) >= 30 and author is not "[deleted]"'''
if subreddit != "":
    query_string += ' and subreddit = "' + subreddit + '"'

if author != "":
    query_string += ' and author = "' + author + '"'

if group_s:
    query_string += ' group by subreddit'
    if (group_s and group_u):
        query_string += ' and author'
elif group_u:
    query_string += ' group by author'

query_string += ' ORDER BY score DESC'

query_string += ' LIMIT"' + str(lim) + '")'

print(query_string)

df = pd.read_sql(
    query_string,
    conn
)

# for row in df:
#   print(row[0], row[1], row[2], "\n")


ang_content = []
joy_content = []
fear_content = []
sadness_content = []
surprise_content = []
tags_content = []

# get the average score for all words in the comments
for string in df['body'].values:
    try:
        emo = get_emo(string)
        #tags = get_tags(string)
        if tag_list != []:
            tags = dict((key, value) for key, value in tags.items() if key in tag_list)
    except:
        ang_content.append(-1)
        joy_content.append(-1)
        fear_content.append(-1)
        sadness_content.append(-1)
        surprise_content.append(-1)
        continue

    #tags_content.append(tags)
    ang_content.append(emo[0])
    joy_content.append(emo[1])
    fear_content.append(emo[2])
    sadness_content.append(emo[3])
    surprise_content.append(emo[4])

#df['Tags'] = tags_content
df['Anger'] = ang_content
df['Joy'] = joy_content
df['Fear'] = fear_content
df['Sadness'] = sadness_content
df['Surprise'] = surprise_content

log = open('./subreddits.csv', "a+")

print("id,author,body,subreddit,score,anger,joy,fear,sadness,surprise", file=log)
for row in df.iterrows():
    print(row[1][0],row[1][1],row[1][2].replace(',' , '').replace('\n' , ''),row[1][3],row[1][4],row[1][5],row[1][6]
          ,row[1][7],row[1][8],row[1][9], file=log, sep=',')

conn.close()
