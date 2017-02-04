from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
from flask_bootstrap import Bootstrap
import indicoio

import pygal

indicoio.config.api_key = 'c938b911dce99664a3af0f077ad2edc6'
app = Flask(__name__)
Bootstrap(app)

class HelloForm(Form):
	sayhello = TextAreaField('',[validators.DataRequired()])

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
		return render_template('hello.html', name=result)
	return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
