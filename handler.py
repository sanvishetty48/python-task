import json
import boto3
from botocore.exceptions import ClientError
from email_validator import validate_email, EmailNotValidError

SES_REGION = "ap-south-1" 

def send_email(event, context):
    try:
        body = json.loads(event['body'])
        receiver_email = body['receiver_email']
        subject = body['subject']
        body_text = body['body_text']

        # Validate email
        try:
            validate_email(receiver_email)
        except EmailNotValidError as e:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": str(e)})
            }

        # Send email
        client = boto3.client('ses', region_name=SES_REGION)
        response = client.send_email(
            Source='sanvishetty48@gmail.com',  
            Destination={
                'ToAddresses': [receiver_email]
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Email sent successfully!"})
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Failed to send email", "error": str(e)})
        }
    except KeyError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": f"Missing required field: {str(e)}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)})
        }
