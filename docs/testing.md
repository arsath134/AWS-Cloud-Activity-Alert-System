# Testing

Upload a file to your S3 bucket and check whether CloudTrail records the activity.

Then check EventBridge and the Lambda CloudWatch logs.

Make sure the message reaches SQS and Lambda 2 processes it successfully.

Finally, check your email for the SNS notification.
