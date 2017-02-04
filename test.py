#!/usr/bin/python

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import sentiwordnet as swn
import numpy as np

conn = sqlite3.connect('database.sqlite')

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

df = pd.read_sql("SELECT score, body, subreddit from May2015 where LENGTH(body) > 30 AND LENGTH(body) < 100 LIMIT 100",conn)
#for row in df:
#   print(row[0], row[1], row[2], "\n")

keywords = ['Positive', 'Negative', 'Objective', 'Subjective']

content_summary = pd.DataFrame()

pos_content = []
neg_content = []
obj_content = []
sub_content = []

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
