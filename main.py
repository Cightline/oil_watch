import json

from flask import Flask, render_template

from sql.db_connect import Connect

app   = Flask(__name__)

with open('config.json') as cfg:
    config = json.load(cfg)


app.config.update(config)

db = Connect(app.config['SQLALCHEMY_DATABASE_URI'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/commodities')
def commodities():
    return render_template('commodities.html', db=db)

if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'])
