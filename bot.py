from slackclient import SlackClient
import time
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime
import pandas 
import numpy


analyzer = SentimentIntensityAnalyzer()

slack_token = 'xoxb-493304761941-494539529958-xxyoXNq678MuK50kPSh2EoAE'
sc = SlackClient(slack_token)

PosMsg = 'That seemed really positive! Good going!'
BitPosMsg = 'Looks pretty positive. Nice.'
NeutralMsg = 'I have no strong feelings one way or the other.'
BitNegMsg = 'Looks a bit negative. Maybe try rephrasing.'
NegMsg = 'Seems pretty negative. Consider rephrasing.'

if sc.rtm_connect():
    print('success')

def calcMsg(score):
    if(score >0.5):
        msg = PosMsg
    elif(score >= 0.2 and score <= 0.5):
        msg = BitPosMsg
    elif(score >= -0.2 and score < 0.2):
        msg =  NeutralMsg
    elif(score < -0.2 and score > -0.5):
        msg = BitNegMsg
    elif(score <= -0.5):
        msg = NegMsg
    msg = "Quote: '" + x['text'] + "'\n " + msg
    return msg


if sc.rtm_connect():
  while True:
    ob = sc.rtm_read()
    print(ob)
    i = 0
    for x in ob:
        if ('type' in x and x['type'] == 'message'):
            try:
                score = analyzer.polarity_scores(x['text'])['compound']
                msg = calcMsg(score)
                if x['channel'][0] == 'C':
                    sc.api_call(
                        "chat.postEphemeral",
                        channel= x['channel'],
                        text= msg,
                        user= x['user']
                        )
                
                else:
                    sc.rtm_send_message(x['channel'], msg)
            except: 
                pass
    time.sleep(1)
else:
    print ("Connection Failed")
