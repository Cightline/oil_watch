from datetime import datetime, date
import json

from dateutil import rrule
from dateutil.relativedelta import relativedelta
from sqlalchemy.sql import func, extract

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

from sql.db_connect import Connect


with open('config.json') as cfg:
    config = json.load(cfg)

db = Connect(config['SQLALCHEMY_DATABASE_URI'])
plotly.tools.set_credentials_file(username=config['plotly_username'], api_key=config['plotly_api_key'])

quandl = db.base.classes.quandl

def get_country(code, operation):
    
    for country in config[operation]:
        if config[operation][country] == code:
            return country




def generate_chart(operation):
    now  = date.today()
    past = now + relativedelta(months=-48)

    data_x = []
    data_y = {}
    traces = []

   
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=past, until=now):
        print(dt.month, dt.year)

        data_x.append(dt) 

        for country in config[operation]:
            q = db.session.query(quandl).filter(extract('month', quandl.date) == dt.month).filter(extract('year', quandl.date) == dt.year).filter(quandl.code == config[operation][country]).all()

            for item in q:
                if item.code not in data_y:
                    data_y[item.code] = []

                data_y[item.code].append(item.value)

        
    for key in data_y:
       

        traces.append(go.Scatter(x=data_x, y=data_y[key], name=get_country(key, operation)))


    py.plot(traces, filename=operation)




generate_chart('global_imports')
generate_chart('global_exports')
generate_chart('global_production')

