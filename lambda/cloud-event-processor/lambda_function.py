import json
import boto3
import os
import uuid
from datetime import datetime, timezone


# ============================================================
# AWS SQS CONFIGURATION
# ============================================================

sqs = boto3.client(
    "sqs",
    region_name="ap-southeast-2"
)

SQS_QUEUE_URL = os.environ["SQS_QUEUE_URL"]


# ============================================================
# EXTRACT ACTOR INFORMATION
# ============================================================

def get_actor(user_identity):

    identity_type = user_identity.get(
        "type",
        "Unknown"
    )

    # --------------------------------------------------------
    # IAM USER
    # --------------------------------------------------------

    if identity_type == "IAMUser":

        username = user_identity.get(
            "userName",
            "UnknownIAMUser"
        )

        return {
            "name": username,
            "type": "IAM User",
            "arn": user_identity.get(
                "arn",
                "Unknown ARN"
            )
        }

    # --------------------------------------------------------
    # ASSUMED IAM ROLE
    # --------------------------------------------------------

    elif identity_type == "AssumedRole":

        arn = user_identity.get(
            "arn",
            "Unknown ARN"
        )

        role_name = "UnknownRole"

        if ":assumed-role/" in arn:

            role_part = arn.split(
                ":assumed-role/"
            )[1]

            role_name = role_part.split(
                "/"
            )[0]

        return {
            "name": role_name,
            "type": "IAM Role",
            "arn": arn
        }

    # --------------------------------------------------------
    # ROOT USER
    # --------------------------------------------------------

    elif identity_type == "Root":

        return {
            "name": "AWS Root User",
            "type": "Root User",
            "arn": user_identity.get(
                "arn",
                "Unknown ARN"
            )
        }

    # --------------------------------------------------------
    # AWS SERVICE
    # --------------------------------------------------------

    elif identity_type == "AWSService":

        return {
            "name": user_identity.get(
                "invokedBy",
                "AWS Service"
            ),
            "type": "AWS Service",
            "arn": user_identity.get(
                "arn",
                "Unknown ARN"
            )
        }

    # --------------------------------------------------------
    # OTHER IDENTITY TYPES
    # --------------------------------------------------------

    else:

        return {
            "name": user_identity.get(
                "principalId",
                "UnknownUser"
            ),
            "type": identity_type,
            "arn": user_identity.get(
                "arn",
                "Unknown ARN"
            )
        }


# ============================================================
# LAMBDA HANDLER
# ============================================================

def lambda_handler(event, context):

    print(
        "========== CLOUD EVENT PROCESSOR STARTED =========="
    )

    # --------------------------------------------------------
    # Generate Task ID
    # --------------------------------------------------------

    task_id = (
        "TASK-" +
        str(uuid.uuid4())[:8].upper()
    )

    # --------------------------------------------------------
    # CloudTrail / EventBridge detail
    # --------------------------------------------------------

    detail = event.get(
        "detail",
        {}
    )

    event_name = detail.get(
        "eventName",
        "UnknownEvent"
    )

    event_source = detail.get(
        "eventSource",
        "UnknownSource"
    )

    event_time = detail.get(
        "eventTime",
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    # --------------------------------------------------------
    # User / IAM identity
    # --------------------------------------------------------

    user_identity = detail.get(
        "userIdentity",
        {}
    )

    actor = get_actor(
        user_identity
    )

    actor_name = actor["name"]
    actor_type = actor["type"]
    actor_arn = actor["arn"]

    # --------------------------------------------------------
    # Request parameters
    # --------------------------------------------------------

    request_parameters = detail.get(
        "requestParameters",
        {}
    )

    bucket_name = request_parameters.get(
        "bucketName",
        "UnknownBucket"
    )

    object_key = request_parameters.get(
        "key",
        ""
    )

    # --------------------------------------------------------
    # Resource
    # --------------------------------------------------------

    if object_key:

        resource = (
            f"s3://{bucket_name}/{object_key}"
        )

    else:

        resource = (
            f"s3://{bucket_name}"
        )

    # --------------------------------------------------------
    # Logging
    # --------------------------------------------------------

    print(f"TASK_ID     : {task_id}")
    print(f"EVENT       : {event_name}")
    print(f"ACTOR       : {actor_name}")
    print(f"ACTOR TYPE  : {actor_type}")
    print(f"ACTOR ARN   : {actor_arn}")
    print(f"BUCKET      : {bucket_name}")
    print(f"OBJECT      : {object_key}")
    print(f"RESOURCE    : {resource}")

    # --------------------------------------------------------
    # SQS message
    # --------------------------------------------------------

    message = {

        "task_id": task_id,

        "event_name": event_name,

        "event_source": event_source,

        "event_time": event_time,

        "user": actor_name,

        "user_type": actor_type,

        "user_arn": actor_arn,

        "bucket": bucket_name,

        "object_key": object_key,

        "resource": resource,

        "cloudtrail_status": "SUCCESS",

        "eventbridge_status": "SUCCESS",

        "lambda_1_status": "SUCCESS",

        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    # --------------------------------------------------------
    # Send message to SQS
    # --------------------------------------------------------

    response = sqs.send_message(

        QueueUrl=SQS_QUEUE_URL,

        MessageBody=json.dumps(
            message
        )
    )

    message_id = response.get(
        "MessageId"
    )

    print("SQS : SUCCESS")

    print(
        f"SQS Message ID : {message_id}"
    )

    print(
        "========== MESSAGE SENT TO SQS =========="
    )

    # --------------------------------------------------------
    # Return
    # --------------------------------------------------------

    return {

        "statusCode": 200,

        "body": json.dumps({

            "status": "SUCCESS",

            "task_id": task_id,

            "event": event_name,

            "actor": actor_name,

            "actor_type": actor_type,

            "bucket": bucket_name,

            "object": object_key,

            "resource": resource,

            "sqs_message_id": message_id
        })
    }
