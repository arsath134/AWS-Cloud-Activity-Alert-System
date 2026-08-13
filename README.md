# AWS-Cloud-Activity-Alert-System
A serverless AWS security monitoring system that detects S3 activity using CloudTrail and EventBridge, processes the events through AWS Lambda and SQS, and sends real-time email alerts using Amazon SNS.

# Cloud Activity Alert System

This project monitors important AWS activities and sends an email alert when something happens.

I used AWS CloudTrail to track activities, EventBridge to detect the events, Lambda to process them, SQS to pass the messages, and SNS to send the final email notification.

For example, if someone uploads or deletes an object from the selected S3 bucket, the system detects the activity and sends an alert with details like the event, user, bucket, and time.

## AWS Services Used

- Amazon S3
- AWS CloudTrail
- Amazon EventBridge
- AWS Lambda
- Amazon SQS
- Amazon SNS
- Amazon CloudWatch

## Project Flow

S3 / AWS Activity  
↓  
CloudTrail  
↓  
EventBridge  
↓  
Lambda  
↓  
SQS  
↓  
Lambda  
↓  
SNS  
↓  
Email Alert

## Main Goal

The main goal of this project is to make AWS activity easier to monitor without checking CloudTrail logs manually every time.
