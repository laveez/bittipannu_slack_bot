import datetime
import urllib
import json
import os
from flask import Flask, request
from slackclient import SlackClient

app = Flask(__name__)

# flask
# slackclient

def cb(update_data):
    pass

@app.route("/verify", methods=['GET', 'POST'])
def verify():
    print('DATA: {}'.format(request.data))
    if request.data:
        return json.loads(request.data).get('challenge', '')
    else:
        return ''

@app.route("/")
def hello():
    slack_credentials = dict()
    url = 'https://www.sodexo.fi/ruokalistat/output/daily_json/5865/' + datetime.date.today().strftime('%Y/%m/%d') + '/fi';

    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    res_str = '*Bittipannun päivän ruokalista:*\n - ' + '\n - '.join([
        '{} ({})'.format(item['title_fi'], item['price'][:4]) 
        for item in data['courses'] 
        if item['category'] not in ['Sweet', 'Mix & Match']
    ])

    with open(os.environ['SLACK_CREDENTIAL_PATH'], 'r') as f:
        slack_credentials = json.load(f)    
    
    sc = SlackClient(
        refresh_token=slack_credentials.get('refresh_token', ''),
        client_id=slack_credentials.get('client_id', ''),
        client_secret=slack_credentials.get('client_secret', ''),
        token_update_callback=cb 
    )

    sc.api_call(
        "chat.postMessage",
        channel="opiskelijaruoka",
        user="bittipannuruokalista",
        icon=":tonni:",
        text=res_str
    )

    # $message = $this->slackClient->createMessage()
    #     ->to($slackIncomingWebHook->getChannelName())
    #     ->from('Bittipannu ruokalista')
    #     ->setIcon(':tonni:')
    #     ->setText($text);

    # $this->slackClient->sendMessage($message);
    return '<pre>' + res_str + '</pre>'