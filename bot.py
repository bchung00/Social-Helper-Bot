from slackclient import SlackClient
import time

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

slack_token = 'xoxb-493304761941-494539529958-xxyoXNq678MuK50kPSh2EoAE'
sc = SlackClient(slack_token)

if sc.rtm_connect():
  while True:
    ob = sc.rtm_read()
    print(ob)
    i = 0
    for x in ob:
        if ('type' in x and x['type'] == 'message'):
            score = analyzer.polarity_scores(x['text'])
            sc.rtm_send_message("general", "test")
    time.sleep(3)
else:
    print ("Connection Failed")

sc.api_call(
  "chat.postMessage",
  channel="#general",
  text="Hello from Python! :tada:"
)