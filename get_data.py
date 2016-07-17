import json
import argparse
from datetime import datetime

import requests

from sql.db_connect import Connect

with open('config.json') as cfg:
    config = json.load(cfg)


db = Connect(config['SQLALCHEMY_DATABASE_URI'])

y_api = 'https://query.yahooapis.com/v1/public/yql?q=select * from yahoo.finance.quotes where symbol in ("%s");&format=json&env=store://datatables.org/alltableswithkeys&callback='

def store_data(ticker):

    
    data = requests.get(y_api % ticker)

    jd = data.json()['query']['results']['quote']

    # debug
    #for key in jd.keys():
    #    print(key, jd[key])

    # We want this to fail is something isn't here
    # LastTradeDate 7/15/2016
    
    r_time = datetime.combine(datetime.strptime(jd['LastTradeDate'], '%m/%d/%Y'), datetime.strptime(jd['LastTradeTime'], '%I:%M%p').time())

    new_data = db.base.classes.prices(p_time=datetime.now(), 
                                      r_time=r_time,
                                      ticker=ticker,
                                      price=jd['LastTradePriceOnly'])
    db.session.add(new_data)
    db.session.commit()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='store economic data')
    parser.add_argument('--ticker', action='store', required=True)

    args = parser.parse_args()
    
    store_data(args.ticker)
    

