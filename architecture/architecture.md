# Architecture

This project monitors activity in a selected S3 bucket and sends an email alert when an important action happens.

CloudTrail records the activity and EventBridge detects the event. The event is sent to Lambda 1, which processes the details and sends them to SQS.

Lambda 2 receives the message from SQS and sends the final notification through SNS.

## Flow

S3 Bucket
↓
CloudTrail
↓
EventBridge
↓
Lambda 1
↓
SQS
↓
Lambda 2
↓
SNS
↓
Email
