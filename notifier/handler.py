import os
import requests


def post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']  # this matches the serverless.yml environment variable

    # can get the full event message by printing the event to cloudwatch
    slack_message = f"From {event['source']} at {event['detail']['StartTime']}: {event['detail']['Description']}\nReason: {event['detail']['Cause']}"
    data = { "text": slack_message }
    requests.post(slack_webhook_url, json=data)
    return