import boto3
import json
from shared.config import settings
import logging

logger = logging.getLogger(__name__)

class SQSClient:
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_ENDPOINT_URL
        )
        self.queue_url = settings.SQS_QUEUE_URL

    def send_message(self, message_body: dict):
        try:
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message_body)
            )
            return response
        except Exception as e:
            logger.error(f"Error sending message to SQS: {e}")
            raise e

sqs_client = SQSClient()
