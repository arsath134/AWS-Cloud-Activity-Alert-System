# Setup

Create an S3 bucket and replace `YOUR_BUCKET_NAME` with your bucket name.

Enable CloudTrail to record AWS activity.

Create an EventBridge rule using the event pattern provided in this project.

Connect EventBridge to your first Lambda function.

Connect the first Lambda to SQS and SQS to the second Lambda.

Finally, connect the second Lambda to an SNS topic and confirm your email subscription.

Update the required IAM permissions and environment variables with your own AWS resources.
