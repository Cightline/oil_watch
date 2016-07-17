import json

from flask import Flask



app = Flask(__name__)

with open('config.json') as cfg:
    config = json.load(cfg)


app.config.update(config)

@app.route("/")
def index():
    return 'index'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=config['port'])
