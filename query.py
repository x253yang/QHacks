#!/usr/bin/python

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys, getopt
import indicoio
from sklearn.neighbors import KNeighborsClassifier
indicoio.config.api_key = 'db91e10ba18babcf6e5e5209a5f0ab6f'

author = ""
lim = 10
group_s = 0
group_u = 0
tag_list = []
tag_length = 0

sub_list = [
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
]

conn = sqlite3.connect('../database.sqlite', timeout=6000)

log = open('./subreddits.csv', "a+")

print("created_utc,author,body,subreddit,score", file=log)

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

i = 0
for subreddit in sub_list:
    i += 1
    print(i, subreddit)
    query_string = '''
    SELECT * FROM (SELECT created_utc, author, body, subreddit, score from May2015
    where LENGTH(body) >= 30 and author is not "[deleted]"'''

    if subreddit != "":
        query_string += ' and subreddit = "' + subreddit + '"'

    query_string += ' ORDER BY score ASC'

    query_string += ' LIMIT"' + str(lim) + '")'

    query_string += ' UNION '

    query_string += '''
    SELECT * FROM (SELECT id, author, body, subreddit, score
    from May2015 where LENGTH(body) >= 30 and author is not "[deleted]"'''
    if subreddit != "":
        query_string += ' and subreddit = "' + subreddit + '"'

    query_string += ' ORDER BY score DESC'

    query_string += ' LIMIT"' + str(lim) + '")'
    df = pd.read_sql(
        query_string,
        conn
    )

    # for row in df:
    #   print(row[0], row[1], row[2], "\n")

    '''ang_content = []
    joy_content = []
    fear_content = []
    sadness_content = []
    surprise_content = []
    tags_content = []

    # get the average score for all words in the comments
    for string in df['body'].values:
        try:
            emo = get_emo(string)
        except:
            ang_content.append(-1)
            joy_content.append(-1)
            fear_content.append(-1)
            sadness_content.append(-1)
            surprise_content.append(-1)
            continue

        ang_content.append(emo[0])
        joy_content.append(emo[1])
        fear_content.append(emo[2])
        sadness_content.append(emo[3])
        surprise_content.append(emo[4])

    df['Anger'] = ang_content
    df['Joy'] = joy_content
    df['Fear'] = fear_content
    df['Sadness'] = sadness_content
    df['Surprise'] = surprise_content'''

    for row in df.iterrows():
        print(row[1][0], row[1][1], row[1][2].replace(',', '').replace('\n', ''), row[1][3], row[1][4], file=log, sep=',')

conn.close()