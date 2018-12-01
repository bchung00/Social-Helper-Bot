from slackclient import SlackClient

slack_token = open("bot-token.txt","r").read()
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="#general",
  text="Hello from Python! :tada:"
)