import os
from pathlib import Path
from flask import Flask, request, Response
import slack
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], '/slack/events', app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

@app.route('/receive-notifications', methods = ['POST'])
def receive_notification():
    data = request.form
    print(data)
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    try:
        result = client.chat_postEphemeral(user=user_id,
            channel=channel_id,
            # Aqui vai o JSON da mensagem:
            blocks= [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "What kind of notification do you need?",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "BTCUSDT Price."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Accept",
					"emoji": True
				},
				"value": "BTCUSDT",
				"action_id": "button-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "ETHUSDT Price."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Accept",
					"emoji": True
				},
				"value": "ETHUSDT",
				"action_id": "button-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "XRPUSDT Price."
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "Accept",
					"emoji": True
				},
				"value": "XRPUSDT",
				"action_id": "button-action"
			}
		}
	]
        )
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")
    return Response(), 200



if __name__ == '__main__':
    app.run(debug=True)