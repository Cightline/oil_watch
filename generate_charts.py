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




def generate_chart(operation, title, x_axis_label, y_axis_label):
    now       = date.today()
    past      = now + relativedelta(months=-48)

    data_x = []
    data_y = {}
    traces = []

  
    # Use months as a common iterator across all the data
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=past, until=now):
        print(dt.month, dt.year)

        # Store which month we are working on 
        data_x.append(dt) 


        # Then store all the data from that month
        for country in config[operation]:
            # Get all the items for the matching month and year
            q = db.session.query(quandl).filter(extract('month', quandl.date) == dt.month).filter(extract('year', quandl.date) == dt.year).filter(quandl.code == config[operation][country]).all()
            
            # Initialize the dictionary if it doesn't exist yet and add the data
            for item in q:
                if item.code not in data_y:
                    data_y[item.code] = []

                # Check and see if the data exists, and if it does append it to the list

                if item.value:
                    data_y[item.code].append(item.value)

                else:
                    data_y[item.code].append([])


    # Each "key" is a code (JODI/OIL_CRIMKB_CHN), we need to lookup the key name (get_country) and add it to traces
    for key in data_y:
        traces.append(go.Scatter(x=data_x, y=data_y[key], name=get_country(key, operation)))

    
    
    layout = dict(title = title, xaxis = dict(title = x_axis_label), yaxis = dict(title = y_axis_label))

    fig = dict(data=traces, layout=layout)
    py.plot(fig, filename=operation)




generate_chart('global_imports',    'Global Crude Oil Imports', '',    'thousands of barrels')
generate_chart('global_exports',    'Global Crude Oil Exports', '',    'thousands of barrels')
generate_chart('global_production', 'Global Crude Oil Production', '', 'thousands of barrels')

