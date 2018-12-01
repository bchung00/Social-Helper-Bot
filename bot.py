from slackclient import SlackClient

slack_token = 'xoxb-493304761941-493309119797-HKQEeEajSVSQjpg5kAApFOOg'
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="#general",
  text="Hello from Python! :tada:"
)