# QHacks
QHacks project


indico.py: run this to test if indicoio works. You should get output [0.9819219949985644,0.00015202198176385973]

test.py: sentiment analysis with sentiwordnet

data.py: sentiment and tag analysis with indicoio

Both test.py and data.py use the commandline: python test.py -s <subreddit> -u <author> -l <limit> -gs -gu

-s: subreddit

-u: user/author

-l: limits number of comments. default: 100

-gs: group by subreddit

-gu: group by user/author

For test.py and data.py, inputs are invalid if they contain a non-alphanumeric character other than '-' and '_'


Running Flask app
Open up repo:
python app.py 
