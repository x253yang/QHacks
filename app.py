from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, StringField, validators
from flask_bootstrap import Bootstrap
import indicoio
import json
import pygal
from pygal.style import DarkColorizedStyle

indicoio.config.api_key = 'c938b911dce99664a3af0f077ad2edc6'
app = Flask(__name__)
Bootstrap(app)

class HelloForm(Form):
	sayhello = StringField('',[validators.DataRequired()])

@app.route('/')
def index():
	form = HelloForm(request.form)
	return render_template('index.html', form=form)

@app.route('/hello', methods=['POST'])
def hello():
	form = HelloForm(request.form)
	if request.method == 'POST' and form.validate():
		name = request.form['sayhello']
		result = indicoio.sentiment(name)
		resultEmotion = indicoio.emotion(name);
		resultTwitter = indicio.twitter_engagment(name);
		resultPersona = indicio.personas(name);
		resultPersonality = indicio.personality(name);

		#Creating chart of emotions
		pie_chart = pygal.Pie(inner_radius=.4, style=DarkColorizedStyle)
		pie_chart.title = ''
		pie_chart.add('Anger', resultEmotion['anger']*100)
		pie_chart.add('Surprise', resultEmotion['surprise']*100)
		pie_chart.add('Sadness', resultEmotion['sadness']*100)
		pie_chart.add('Fear', resultEmotion['fear']*100)
		pie_chart.add('Happiness', resultEmotion['joy']*100)
		graph_data = pie_chart.render_data_uri()
		return render_template('hello.html', result=result, emotion_graph=graph_data)
		#Need to render this somehow...
	return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
