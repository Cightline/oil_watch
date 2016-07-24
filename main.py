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
    commodities = {}

    for key in config['commodities']:
        commodities[key] = db.session.query(db.base.classes.prices).filter(db.base.classes.prices.ticker == config['commodities'][key]).first()


    return render_template('commodities.html', db=db, commodities=commodities)

@app.route('/stats')
def production():
    limit = 50
    productions = {}
    chart_list  = []


    return render_template('stats.html')

if __name__ == '__main__':
    app.run(host=config['host'], port=config['port'])
