from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, StringField, validators
from flask_bootstrap import Bootstrap
import pandas as pd
from bs4 import BeautifulSoup
import re
import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier
import indicoio
import json
import pygal
from pygal.style import DarkStyle

indicoio.config.api_key = 'c938b911dce99664a3af0f077ad2edc6'


#Takes a comment and prepares it for processing
def body_to_words(raw_body):

	#Remove any existing HTML (for sanity sake)
	body_text = BeautifulSoup(raw_body).get_text()

	#Remove any punctuation and non-letters
	letters_only = re.sub("[^a-zA-Z]", " ", body_text)

	#Convert to lowercase
	words = letters_only.lower().split()

	#convert stop words to a set (for speed purposes)

	stops = set(stopwords.words("english"))

	#removing stop words

	meaningful_words = [w for w in words if not w in stops]

	#Joining the words into a single string separated by space and return the result

	return( " ".join( meaningful_words ))


def buildBagOfWords(comments):
	#fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform(clean_train_reviews) should be a list of strings
	train_data_features = vectorizer.fit_transform(comments)

	train_data_features = train_data_features.toarray()

	return train_data_features

def trainForestModel(train_data_features, trainValue):
	forest = RandomForestClassifier(n_estimators = 100)

	#Fit the forest to the training set, using the bag of words as features
	#trainValue is what we will be training for (response variable)
	forest = forest.fit(train_data_features, train[trainValue])

	return forest



#importing training data
train = pd.read_csv("subreddits.csv")
vectorizer = CountVectorizer(analyzer="word", tokenizer = None, preprocessor= None, stop_words = None, max_features = 5000)

num_reviews = train["body"].size

clean_train_comments = []

for i in xrange(0, num_reviews):
	#call our function for each one, and add the result to the list
	clean_train_comments.append(body_to_words(train["body"][i]))
train_data_features = buildBagOfWords(clean_train_comments)
vocab = vectorizer.get_feature_names()
#Sum up contents of all the vocab words
dist = np.sum(train_data_features, axis=0)
print("training model 1")
forest = trainForestModel(train_data_features, "subreddit")
print("training model 2")
forest2 = trainForestModel(train_data_features, "score")
print("Done training")
app = Flask(__name__)
Bootstrap(app)


class HelloForm(Form):
	sayhello = StringField('',[validators.DataRequired()])
def getSubRedditRec(value):
	#This is what we will pass the input to get the recommended subreddit
	#pass in a value #using forest
	clean_test_posts = []
	clean_post = body_to_words(value)
	clean_test_posts.append(clean_post)

	test_data_features = vectorizer.transform(clean_test_posts)
    #test_data_features = test_data_features.toarray()

	result = forest.predict(test_data_features)

	return result

def getScore(value):
	#pass in a value using forest2
	print("Called")
	clean_test_posts = []
	clean_post = body_to_words(value)
	clean_test_posts.append(clean_post)

	test_data_features = vectorizer.transform(clean_test_posts)
    #test_data_features = test_data_features.toarray()

	result = forest2.predict(test_data_features)

	return result
@app.route('/')
def index():
	form = HelloForm(request.form)
	return render_template('index.html', form=form)

@app.route('/hello', methods=['POST'])
def results():
	form = HelloForm(request.form)
	if request.method == 'POST' and form.validate():
		name = request.form['sayhello']
		sentimentResult = indicoio.sentiment(name)
		resultEmotion = indicoio.emotion(name)
		resultTwitter = indicoio.twitter_engagement(name)
		resultPersona = indicoio.personas(name)
		resultPersonality = indicoio.personality(name)
		score = getScore(name)
		subredditRec = getSubRedditRec(name)

		#Creating chart of emotions
		radar_chart = pygal.Radar(style=DarkStyle)
		radar_chart.add('Anger', resultEmotion['anger']*100)
		radar_chart.add('Surprise', resultEmotion['surprise']*100)
		radar_chart.add('Sadness', resultEmotion['sadness']*100)
		radar_chart.add('Fear', resultEmotion['fear']*100)
		radar_chart.add('Happiness', resultEmotion['joy']*100)
		graph_data = radar_chart.render_data_uri()

		#Creating personality
		pie_chart = pygal.Pie(inner_radius=.4, style=DarkStyle)
		pie_chart.add('extraversion', resultPersonality['extraversion']*100)
		pie_chart.add('openness', resultPersonality['openness']*100)
		pie_chart.add('agreeableness', resultPersonality['agreeableness']*100)
		pie_chart.add('conscientiousness', resultPersonality['conscientiousness']*100)
		pie_chart= pie_chart.render_data_uri()
		#Creating personas

		#sentiment
		line_chart = pygal.HorizontalBar(style=DarkStyle)
		line_chart.add('Sentiment Of Your Post', sentimentResult*100)
		line_chart.add('Sentiment Of Reddit (Avg)',  45)
		line_chart = line_chart.render_data_uri()

		#Personas chart
		persona_chart = pygal.Pie(inner_radius=.75, style=DarkStyle)
		persona_chart.add('Advocate', resultPersona['advocate']*100)
		persona_chart.add('Mediator', resultPersona['mediator']*100)
		persona_chart.add('Consul', resultPersona['consul']*100)
		persona_chart.add('Architect', resultPersona['architect']*100)
		persona_chart.add('Logician', resultPersona['logician']*100)
		persona_chart.add('Commander', resultPersona['commander']*100)
		persona_chart.add('Debater', resultPersona['debater']*100)
		persona_chart.add('Protagonist', resultPersona['protagonist']*100)
		persona_chart.add('Campaigner', resultPersona['campaigner']*100)
		persona_chart.add('Logisitican', resultPersona['logistician']*100)
		persona_chart.add('Defender', resultPersona['defender']*100)
		persona_chart.add('Executive', resultPersona['executive']*100)
		persona_chart.add('Consul', resultPersona['consul']*100)
		persona_chart.add('Adventurer', resultPersona['adventurer']*100)
		persona_chart.add('Entrepreneur', resultPersona['entrepreneur']*100)
		persona_chart = persona_chart.render_data_uri()

		return render_template('dashboard.html', twitter=resultTwitter*100, graph_data=graph_data, sentiment_chart=line_chart, personas_chart=persona_chart, pie_chart=pie_chart, score=score[0], subred=subredditRec[0], post=name)
		#Need to render this somehow...
	return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
