import boto3 # AWS SDK for Python to interact with AWS services
from textblob import TextBlob # Library for processing textual data
import datetime
import json
import os

# Initialize AWS resources
dynamodb = boto3.resource("dynamodb")
# Environment variable should be set in Lambda console
TABLE_NAME = os.environ.get("TABLE_NAME", "")
table = dynamodb.Table(TABLE_NAME)
ses = boto3.client("ses")

SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "")


def lambda_handler(event, context):
    try:
        # 1. Parse the incoming request body
        # API Gateway may pass the body as a string, so we need to parse it safely.
        if isinstance(event.get("body"), str):
            body = json.loads(event["body"])
        else:
            body = event

        user_name = body.get("user_name", "Anonymous")
        review_text = body.get("review", "")
        timestamp = datetime.datetime.now().isoformat()

        # 2. Perform Sentiment Analysis using TextBlob
        # Polarity score ranges from -1.0 (Negative) to 1.0 (Positive)
        blob = TextBlob(review_text)
        polarity = blob.sentiment.polarity

        # Determine sentiment category based on polarity thresholds
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        # 3. Save the result to DynamoDB
        # Storing the exact polarity score is useful for future data analysis.
        table.put_item(
            Item={
                "user_name": user_name,
                "review": review_text,
                "sentiment": sentiment,
                "polarity_score": str(
                    polarity
                ),  # Convert float to string for DynamoDB compatibility
                "timestamp": timestamp,
            }
        )

        # 4. Send Email Notification via SES
        # Only notify for Positive reviews to reduce spam.
        # SES: In Sandbox mode, both the sender and recipient emails must be verified.
        if sentiment == "Positive":
            ses.send_email(
                Source=SENDER_EMAIL,
                Destination={"ToAddresses": [RECEIVER_EMAIL]},
                Message={
                    "Subject": {"Data": f"[{sentiment}] Review from {user_name}"},
                    "Body": {"Text": {"Data": f"Review: {review_text}"}},
                },
            )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Processed as {sentiment} (Score: {polarity:.2f})"),
        }

    except Exception as e:
        print(f"Error: {e}")
        return {"statusCode": 500, "body": "Internal Server Error"}
