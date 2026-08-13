# Troubleshooting

If you don't receive an email, check the CloudWatch logs of both Lambda functions.

Also check whether EventBridge received the event and whether SQS contains the message.

Make sure your SNS email subscription is confirmed.

If the user information is incorrect, check the `userIdentity` section of the CloudTrail event.

For IAM role activity, check the role ARN and session information to identify which role performed the action.
