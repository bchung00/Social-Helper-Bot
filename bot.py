from slackclient import SlackClient
import time

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

slack_token = 'xoxb-493304761941-494539529958-xxyoXNq678MuK50kPSh2EoAE'
sc = SlackClient(slack_token)

if sc.rtm_connect():
    print('success')
if sc.rtm_connect():
  while True:
    ob = sc.rtm_read()
    print(ob)
    i = 0
    for x in ob:
        if ('type' in x and x['type'] == 'message'):
            try:
                score = analyzer.polarity_scores(x['text'])['compound']
                
                if(score >0.5):
                    msg = 'That seemed really positive! Good going!'
                elif(score >= 0.2 and score <= 0.5):
                    msg = 'Looks pretty positive. Nice.'
                elif(score >= -0.2 and score < 0.2):
                    msg =  'I have no strong feelings one way or the other.'
                elif(score < -0.2 and score > -0.5):
                    msg = 'Looks a bit negative. Maybe try rephrasing.'
                elif(score <= -0.5):
                    msg = 'That seems negative. Rephrasing seems like a good idea.'
                #sc.rtm_send_message(x['channel'], "Postivity score: " + str(score['compound']*100) + "%",x['ts'],False)
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

sc.api_call(
  "chat.postMessage",
  channel="#general",
  text="Hello from Python! :tada:"
)