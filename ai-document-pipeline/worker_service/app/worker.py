import boto3
import json
import time
import signal
import sys
import logging
from shared.config import settings
from shared.database import SessionLocal
from shared.models import Job
from worker_service.app.services.document_parser import processor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Worker:
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_ENDPOINT_URL
        )
        self.queue_url = settings.SQS_QUEUE_URL
        self.running = True

    def start(self):
        logger.info("Worker started, polling for messages...")
        while self.running:
            try:
                response = self.sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=10 # Long polling
                )

                if 'Messages' in response:
                    for msg in response['Messages']:
                        self.handle_message(msg)
                
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                time.sleep(5)

    def handle_message(self, msg):
        receipt_handle = msg['ReceiptHandle']
        try:
            body = json.loads(msg['Body'])
            job_id = body.get('job_id')
            file_path = body.get('file_path')

            logger.info(f"Received job {job_id}")

            # Update DB to PROCESSING
            db = SessionLocal()
            job = db.query(Job).filter(Job.id == job_id).first()
            if job:
                job.status = "PROCESSING"
                db.commit()

            # Process
            result = processor.process(file_path)

            # Update DB to COMPLETED
            if job:
                job.status = "COMPLETED"
                job.result = result
                db.commit()
                db.close()

            # Delete message
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.info(f"Job {job_id} completed and message deleted.")

        except Exception as e:
            logger.error(f"Failed to process message: {e}")

    def stop(self, signum, frame):
        logger.info("Shutdown signal received")
        self.running = False

if __name__ == "__main__":
    worker = Worker()
    signal.signal(signal.SIGINT, worker.stop)
    signal.signal(signal.SIGTERM, worker.stop)
    worker.start()
