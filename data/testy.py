import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


print("Forming Connection")

sql_conn = sqlite3.connect('../database.sqlite')
print("Connection formed")
subreddits = sql_conn.execute("Select subreddit, body, max(score) From May2015 group by subreddit order by score DESC")
print(subreddits.shape)
print("got thing")
lista = subreddits.fetchmany(100)
for x in lista:
    try:
        print(">>Subreddit: " + x[0] + " -> score:" + str(x[2]) + "<<\n" + x[1] + "\n_____________________________________________________________\n")
    except:
        continue
