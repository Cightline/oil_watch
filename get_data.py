import json
import argparse
from datetime import datetime

import requests
import quandl

from sql.db_connect import Connect


with open('config.json') as cfg:
    config = json.load(cfg)


db = Connect(config['SQLALCHEMY_DATABASE_URI'])
quandl.ApiConfig.api_key = config['quandl_api_key']

y_api = 'https://query.yahooapis.com/v1/public/yql?q=select * from yahoo.finance.quotes where symbol in ("%s");&format=json&env=store://datatables.org/alltableswithkeys&callback='

#eia_api = eia.API(config['eia_api_key'])


# proved oil reserves global
# https://www.quandl.com/data/BP?keyword=proved

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
                                      open_price=jd['Open'],
                                      previous_close=jd['PreviousClose'],
                                      price=jd['LastTradePriceOnly'])
    db.session.add(new_data)
    db.session.commit()




# https://www.quandl.com/data/JODI?keyword=crude%20oil%20production%20russia
def store_quandl(code):
    data = quandl.get(code)

    new_entry_c = 0

    print('Storing quandl data for: %s...' % (code), " ", end="")
    # index is the date
    for index, row in data.iterrows():
        date  = index
        value = row['Value']

        exists = db.session.query(db.base.classes.quandl).filter(db.base.classes.quandl.date == date).filter(db.base.classes.quandl.code == code).first()
        
        if exists:
            continue

        new_data = db.base.classes.quandl(p_time=datetime.now(),
                                          date=date,
                                          code=code,
                                          value=value)
   
        

        db.session.add(new_data)
        db.session.commit()
        new_entry_c += 1

    print('added: %s/%s entries' % (new_entry_c, len(data)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='store economic data')
    parser.add_argument('--store-comm', action='store_true', help='store commodities defined in the config')
    parser.add_argument('--store-global', action='store_true')

    args = parser.parse_args()
   
    if args.store_comm:
        for c in config['commodities']:
            store_data(config['commodities'][c])

    elif args.store_global:
        print('Storing exports...')
        for key in config['global_exports']:
            store_quandl(config['global_exports'][key])

        print('Storing imports...')
        for key in config['global_imports']:
            store_quandl(config['global_imports'][key])

        print('Storing production...')
        for key in config['global_production']:
            store_quandl(config['global_production'][key])
