# AWS Automation - Cloud Watch Events Notifier

## Notifier
Project that uses CloudWatch Events with Lambda to notify Slack users of changes to your AWS account resources.

### Features
Currently targeted to AutoScaling Group events.
You can easily target other AWS resources and their events via the serverless.yml config file.

### Configuration
Secret values currently being supplied by a locally hosted (not committed), environment tagged config file
(eg config.dev.json)