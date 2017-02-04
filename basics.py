
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import sentiwordnet as swn
import numpy as np
import sys, getopt

plt.style.use('ggplot')
conn = sqlite3.connect("../database.sqlite")


#taking in time, subreddit, author, score
#author is not deleted


query_string = """ Select created_utc, subreddit, author, score
                        FROM May2015
                        WHERE author != '[deleted]' and
                        ORDER BY score ASC LIMIT 20 """

df = pd.read_sql(query_string,conn)
print df

#
# people = df["author"].tolist()
# y_pos = np.arange(len(people))
# #performance = 3 + 10 * np.random.rand(len(people))
# performance = df["score"].tolist()
# error = np.random.rand(len(people))
#
# plt.rcdefaults()
# fig, ax = plt.subplots()
#
# ax.barh(y_pos, performance, xerr=error, align='center',
#         color='green', ecolor='black')
# ax.set_yticks(y_pos)
# ax.set_yticklabels(people)
# ax.invert_yaxis()  # labels read top-to-bottom
# ax.set_xlabel('Performance')
# ax.set_title(list(df.columns.values)[0]+ " vs " + list(df.columns.values)[1])
# plt.show()
#
# #df.ix[].plot(kind='bar'); plt.axhline(0, color='k')
