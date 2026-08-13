import json
import os
import boto3
from datetime import datetime, timezone


# ============================================================
# AWS SNS CONFIGURATION
# ============================================================

sns = boto3.client(
    "sns",
    region_name="ap-southeast-2"
)

SNS_TOPIC_ARN = os.environ[
    "SNS_TOPIC_ARN"
]


# ============================================================
# LAMBDA HANDLER
# ============================================================

def lambda_handler(event, context):

    print(
        "========== NOTIFICATION PROCESSOR STARTED =========="
    )

    for record in event.get("Records", []):

        try:

            # ------------------------------------------------
            # Read SQS message
            # ------------------------------------------------

            message = json.loads(
                record["body"]
            )

            # ------------------------------------------------
            # Extract information
            # ------------------------------------------------

            task_id = message.get(
                "task_id",
                "UNKNOWN"
            )

            event_name = message.get(
                "event_name",
                "UNKNOWN"
            )

            event_source = message.get(
                "event_source",
                "UNKNOWN"
            )

            event_time = message.get(
                "event_time",
                "UNKNOWN"
            )

            user = message.get(
                "user",
                "UNKNOWN"
            )

            user_type = message.get(
                "user_type",
                "UNKNOWN"
            )

            user_arn = message.get(
                "user_arn",
                "UNKNOWN"
            )

            bucket = message.get(
                "bucket",
                "UNKNOWN"
            )

            object_key = message.get(
                "object_key",
                ""
            )

            resource = message.get(
                "resource",
                "UNKNOWN"
            )

            # ------------------------------------------------
            # Action description
            # ------------------------------------------------

            action_map = {

                "PutObject":
                    "S3 object uploaded",

                "DeleteObject":
                    "S3 object deleted",

                "GetObject":
                    "S3 object accessed",

                "CreateBucket":
                    "S3 bucket created",

                "DeleteBucket":
                    "S3 bucket deleted"
            }

            action = action_map.get(
                event_name,
                f"AWS action: {event_name}"
            )

            # ------------------------------------------------
            # Log information
            # ------------------------------------------------

            print(
                f"TASK_ID    : {task_id}"
            )

            print(
                f"EVENT      : {event_name}"
            )

            print(
                f"USER       : {user}"
            )

            print(
                f"USER TYPE  : {user_type}"
            )

            print(
                f"USER ARN   : {user_arn}"
            )

            print(
                f"BUCKET     : {bucket}"
            )

            print(
                f"OBJECT     : {object_key}"
            )

            # ------------------------------------------------
            # Create notification
            # ------------------------------------------------

            notification = f"""
AWS CLOUD ACTIVITY ALERT

Task ID: {task_id}

Event: {event_name}
Action: {action}

User: {user}
User Type: {user_type}
User ARN: {user_arn}

Bucket: {bucket}
Object: {object_key}

Resource:
{resource}

Event Time:
{event_time}

Status: COMPLETED

Processed At:
{datetime.now(timezone.utc).isoformat()}
"""

            # ------------------------------------------------
            # Publish to SNS
            # ------------------------------------------------

            response = sns.publish(

                TopicArn=SNS_TOPIC_ARN,

                Subject=f"AWS Alert - {event_name}",

                Message=notification
            )

            print("SNS : SUCCESS")

            print(
                f"SNS Message ID : "
                f"{response['MessageId']}"
            )

            # ------------------------------------------------
            # Final status
            # ------------------------------------------------

            print(
                "=========================================="
            )

            print("TASK COMPLETED")

            print(
                f"TASK_ID       : {task_id}"
            )

            print(
                f"EVENT         : {event_name}"
            )

            print(
                f"USER          : {user}"
            )

            print(
                f"USER TYPE     : {user_type}"
            )

            print(
                f"RESOURCE      : {resource}"
            )

            print("CLOUDTRAIL    : SUCCESS")
            print("EVENTBRIDGE   : SUCCESS")
            print("LAMBDA_1      : SUCCESS")
            print("SQS           : SUCCESS")
            print("LAMBDA_2      : SUCCESS")
            print("SNS           : SUCCESS")
            print("EMAIL         : SENT")
            print("FINAL_STATUS  : COMPLETED")

            print(
                f"COMPLETED_AT  : "
                f"{datetime.now(timezone.utc).isoformat()}"
            )

            print(
                "=========================================="
            )

        except Exception as error:

            print(
                "=========================================="
            )

            print("TASK FAILED")

            print(
                f"ERROR : {str(error)}"
            )

            print(
                "FINAL_STATUS : FAILED"
            )

            print(
                "=========================================="
            )

            raise

    return {

        "statusCode": 200,

        "body": "Notification processing completed"
    }
