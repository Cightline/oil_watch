import json
import argparse
from datetime import datetime

import requests
import eia

from sql.db_connect import Connect

with open('config.json') as cfg:
    config = json.load(cfg)


db = Connect(config['SQLALCHEMY_DATABASE_URI'])

y_api = 'https://query.yahooapis.com/v1/public/yql?q=select * from yahoo.finance.quotes where symbol in ("%s");&format=json&env=store://datatables.org/alltableswithkeys&callback='

eia_api = eia.API(config['eia_api_key'])

def store_eia_imports():
    # PET_IMPORTS.WORLD-US-ALL.M 
    # Imports of all grades of crude oil from World to Total U.S. (US), Monthly

    search = eia_api.data_by_series('PET_IMPORTS.WORLD-US-ALL.M')

    #for key, value in search.items():
    #    print(key, value)

    # First key is a long as name
    # This was fucking confusing as fuck, fuck you EIA
    # Thats cool EIA, I'll strip the whitespace
    
    # The good stuff (dict)
    data = search[list(search.keys())[0]]

    for key in data.keys():
        date  = datetime.strptime(key.strip(), '%Y %m')
        value = data[key]
    
        exists = db.session.query(db.base.classes.eia_imports).filter(db.base.classes.eia_imports.date == date).first()

        if exists:
            continue 

        print(date, value)

        new_data = db.base.classes.eia_imports(p_time=datetime.now(),
                                               date=date,
                                               value=value)

        db.session.add(new_data)
        db.session.commit()



def store_data(ticker):

    
    data = requests.get(y_api % ticker)

    jd = data.json()['query']['results']['quote']

    # debug
    for key in jd.keys():
        print(key, jd[key])

    # We want this to fail is something isn't here
    # LastTradeDate 7/15/2016
    
    r_time = datetime.combine(datetime.strptime(jd['LastTradeDate'], '%m/%d/%Y'), datetime.strptime(jd['LastTradeTime'], '%I:%M%p').time())

    new_data = db.base.classes.prices(p_time=datetime.now(), 
                                      r_time=r_time,
                                      ticker=ticker,
                                      name=jd['Name'],
                                      change=float(jd['LastTradePriceOnly']) - float(jd['PreviousClose']),
                                      open_price=jd['Open'],
                                      previous_close=jd['PreviousClose'],
                                      price=jd['LastTradePriceOnly'])
    db.session.add(new_data)
    db.session.commit()
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='store economic data')
    parser.add_argument('--store-ticker', action='store')
    parser.add_argument('--store-eia-imports', action='store_true')

    args = parser.parse_args()
   
    if args.store_ticker:
        store_data(args.store_ticker)
    
    elif args.store_eia_imports:
        store_eia_imports()
