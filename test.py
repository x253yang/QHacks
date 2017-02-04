#!/usr/bin/python

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import sentiwordnet as swn
import numpy as np
import sys, getopt

subreddit = ""
author = ""
lim = 100
group_s = 0
group_u = 0

i = 1
while (i < len(sys.argv)):

    if sys.argv[i] == '-gs':
        group_s = 1
    elif sys.argv[i] == '-gu':
        group_u = 1
    elif (sys.argv[i] == '-help' or sys.argv[i] == 'help'):
        print("python test.py -s <subreddit> -u <author> -l <limit> -gs -gu")
        sys.exit(0)

    elif i+1 < len(sys.argv):
        if sys.argv[i] == '-s':
            subreddit = sys.argv[i + 1]
        elif sys.argv[i] == '-u':
            author = sys.argv[i + 1]
        elif sys.argv[i] == '-l':
            lim = sys.argv[i + 1]
        i = i + 2
        continue

    i = i + 1
    continue

conn = sqlite3.connect('../database.sqlite')


def get_scores(x):
    return list(swn.senti_synsets(x))


def get_positive_score(sentiments):
    if len(sentiments) > 0:
        return sentiments[0].pos_score()
    return 0


def get_negative_score(sentiments):
    if len(sentiments) > 0:
        return sentiments[0].neg_score()
    return 0


def get_objective_score(sentiments):
    if len(sentiments) > 0:
        return sentiments[0].obj_score()
    return 0


query_string = 'SELECT author, body, subreddit, score, created_utc, edited from May2015 where LENGTH(body) > 0 and author is not "[deleted]"'
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

query_string += ' LIMIT"' + str(lim) + '"'
query_string += ' COLLATE NOCASE'

print(query_string)

df = pd.read_sql(
    query_string,
    conn
)

# for row in df:
#   print(row[0], row[1], row[2], "\n")

keywords = ['Positive', 'Negative', 'Objective', 'Indicoio', 'Diff']

content_summary = pd.DataFrame()

pos_content = []
neg_content = []
obj_content = []

# get the average score for all words in the comments
for string in df['body'].values:
    strings = string.split(" ")
    string_scores = list(map(lambda x: get_scores(x), strings))
    pos_scores = list(map(lambda x: get_positive_score(x), string_scores))
    neg_scores = list(map(lambda x: get_negative_score(x), string_scores))
    obj_scores = list(map(lambda x: get_objective_score(x), string_scores))

    pos_content.append(np.mean(pos_scores))
    neg_content.append(np.mean(neg_scores))
    obj_content.append(np.mean(obj_scores))

df['Positive'] = pos_content
df['Negative'] = neg_content
df['Objective'] = obj_content

print(df)

conn.close()
