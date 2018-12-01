const slackEventsApi = require('@slack/events-api');
const SlackClient = require('@slack/client').WebClient;
const express = require('express');

// *** Initialize an Express application
const app = express();

// *** Initialize a client with your access token
const slack = new SlackClient(process.env.SLACK_ACCESS_TOKEN);

// *** Initialize event adapter using signing secret from environment variables ***
const slackEvents = slackEventsApi.createEventAdapter(process.env.SLACK_SIGNING_SECRET);

// *** Initialize vader sentiment analyzer ***
const vader = require('vader-sentiment');

// Homepage
app.get('/', (req, res) => {
  const url = `https://${req.hostname}/slack/events`;
  res.setHeader('Content-Type', 'text/html');

  return res.send(`<pre>Copy this link to paste into the event URL field: <a href="${url}">${url}</a></pre>`);
});

// *** Plug the event adapter into the express app as middleware ***
app.use('/slack/events', slackEvents.expressMiddleware());

// *** Attach listeners to the event adapter ***

// *** Greeting any user that says "hi" ***
slackEvents.on('app_mention', (message) => {
  console.log(message);
  
  if (message.text.startsWith('hi')) {
    const input = message.text;
    const intensity = vader.SentimentIntensityAnalyzer.polarity_scores(input);
    
    // *** Respond based on user input ***
    slack.chat.postMessage({
      channel: message.channel,
      text: `Hello there <@${message.user}>! You look great today :tada:`
    })
    .catch(console.error)
    
    const response = intensity.pos > intensity.neg ?
          `<@${message.user}>, good to see you again! :blush:` :
          `<@${message.user}>, is everything alright? You look down today :sob:`
    slack.chat.postEphemeral({
      channel: message.channel,
      text: `${response}`,
      user: `${message.user}`
    })
    .catch(console.error)
  }
});

// *** Responding to reactions with the same emoji ***
slackEvents.on('reaction_added', (event) => {
  console.log(event);
  
  slack.chat.postMessage({
    channel: event.item.channel,
    text: `:${event.reaction}:`
  })
  .catch(console.error);
});

// *** Handle errors ***
slackEvents.on('error', (error) => {
  if (error.code === slackEventsApi.errorCodes.TOKEN_VERIFICATION_FAILURE) {
    // This error type also has a `body` propery containing the request body which failed verification.
    console.error(`An unverified request was sent to the Slack events Request URL. Request body: \
${JSON.stringify(error.body)}`);
  } else {
    console.error(`An error occurred while handling a Slack event: ${error.message}`);
  }
});

// Start the express application
const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`server listening on port ${port}`);
});
