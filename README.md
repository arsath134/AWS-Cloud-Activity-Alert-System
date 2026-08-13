# AWS-Cloud-Activity-Alert-System
A serverless AWS security monitoring system that detects S3 activity using CloudTrail and EventBridge, processes the events through AWS Lambda and SQS, and sends real-time email alerts using Amazon SNS.

# Cloud Activity Alert System

This project monitors important AWS activities and sends an email alert when something happens.

I used CloudTrail to record AWS activity, EventBridge to detect events, Lambda to process them, SQS to pass messages, and SNS to send the final email notification.

For example, when someone uploads or deletes an object from the monitored S3 bucket, the system detects the activity and sends an alert with details such as the event, user, bucket, and time.

## AWS Services Used

- Amazon S3
- AWS CloudTrail
- Amazon EventBridge
- AWS Lambda
- Amazon SQS
- Amazon SNS
- Amazon CloudWatch

## Project Flow

S3
->
CloudTrail
->
EventBridge
->
Lambda
->
SQS
->
Lambda
->
SNS
->
Email

## Configuration

Before using the project, replace the example values with your own:

- `YOUR_BUCKET_NAME`
- `YOUR_LAMBDA_ARN`
- `YOUR_SQS_QUEUE_URL`
- `YOUR_SNS_TOPIC_ARN`
- `YOUR_AWS_REGION`

Do not upload real AWS credentials, account details, or private keys to GitHub.
