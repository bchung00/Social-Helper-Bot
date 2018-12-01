from slackclient import SlackClient

slack_token = open("bot-token.txt","r").read()
sc = SlackClient(slack_token)
