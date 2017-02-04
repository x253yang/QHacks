#!/usr/bin/python

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys, getopt
import indicoio
indicoio.config.api_key = 'c938b911dce99664a3af0f077ad2edc6'

subreddit = ""
author = ""
lim = 100
group_s = 0
group_u = 0
tag_list = []
tag_length = 0

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

conn = sqlite3.connect('../database.sqlite')

def get_sent(x):
    return indicoio.sentiment(x)

def get_tags(x):
    return indicoio.text_tags(x)


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


df = pd.read_sql(
    query_string,
    conn
)

# for row in df:
#   print(row[0], row[1], row[2], "\n")

keywords = ['Positive', 'Tags']

content_summary = pd.DataFrame()

pos_content = []
tags_content = []

# get the average score for all words in the comments
for string in df['body'].values:
    pos = get_sent(string)
    tags = get_tags(string)
    if tag_list != []:
        tags = dict((key,value) for key, value in tags.items() if key in tag_list)

    pos_content.append(pos)
    tags_content.append(tags)


df['Positive'] = pos_content
df['Tags'] = tags_content

print(df)

conn.close()
