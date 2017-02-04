from flask import Flask, render_template, request
#from wtforms import Form, TextAreaField, validators
#from flask_bootstrap import Bootstrap
#import indicoio

import pygal

app = Flask(__name__)

@app.route('/')
def pygalexample():
		graph = pygal.Line()
		graph.title = '% Change Coolness of programming languages over time.'
		graph.x_labels = ['2011','2012','2013','2014','2015','2016']
		graph.add('Python',  [15, 31, 89, 200, 356, 900])
		graph.add('Java',    [15, 45, 76, 80,  91,  95])
		graph.add('C++',     [5,  51, 54, 102, 150, 201])
		graph.add('All others combined!',  [5, 15, 21, 55, 92, 105])
		graph_data = graph.render_data_uri()
		return render_template("graphing.html", graph_data = graph_data)

if __name__ == '__main__':
    port = 8000 #the custom port you want
    app.run(host='0.0.0.0', port=port)