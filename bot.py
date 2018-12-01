from slackclient import SlackClient
import time

slack_token = 'xoxb-493304761941-494539529958-xxyoXNq678MuK50kPSh2EoAE'
sc = SlackClient(slack_token)

if sc.rtm_connect():
  while sc.server.connected is True:
        print (sc.rtm_read())
        time.sleep(1)
else:
    print ("Connection Failed")

sc.api_call(
  "chat.postMessage",
  channel="#general",
  text="Hello from Python! :tada:"
)