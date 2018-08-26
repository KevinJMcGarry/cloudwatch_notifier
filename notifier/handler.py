import os


def post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']  # this matches the serverless.yml environment variable
    print(slack_webhook_url)
    print(event)
    
    return
