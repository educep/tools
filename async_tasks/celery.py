"""
Created by Analitika at 19/10/2024
contact@analitika.fr
"""
# External imports
from celery import Celery
import urllib.parse

# Internal imports
from config import (
    AWS_ACCOUNT_ID,
    AWS_ACCESS_KEY_SQS_ID,
    AWS_SECRET_ACCESS_SQS_KEY,
    AWS_SQS_QUEUE_NAME,
    AWS_REGION,
)

"""
$env:AWS_PROFILE = "ank"
aws sqs list-queues --region eu-west-3
celery -A async_tasks.celery worker --pool=solo --loglevel=info
celery -A async_tasks.celery inspect registered

from async_tasks.celery import test_task
test_task.delay()
# don't forget to add folders_with_tasks so that
# from folders_with_tasks.tasks import test_task_child
# test_task_child.delay()
"""

# URL-encode the AWS secret key and access key
encoded_access_key = urllib.parse.quote_plus(AWS_ACCESS_KEY_SQS_ID)
encoded_secret_key = urllib.parse.quote_plus(AWS_SECRET_ACCESS_SQS_KEY)

celery_app = Celery(
    "celery_publisher",
    broker_url=f"sqs://{encoded_access_key}:{encoded_secret_key}@",
    broker_connection_retry_on_startup=True,
    broker_connection_retry=True,
    broker_transport_options={
        "region": AWS_REGION,
        "queue_name_prefix": "",
        "visibility_timeout": 30,
        "polling_interval": 1,
        "predefined_queues": {
            f"{AWS_SQS_QUEUE_NAME}": {  # it must be called celery
                "url": f"https://sqs.{AWS_REGION}.amazonaws.com/{AWS_ACCOUNT_ID}/{AWS_SQS_QUEUE_NAME}",
                "access_key_id": AWS_ACCESS_KEY_SQS_ID,
                "secret_access_key": AWS_SECRET_ACCESS_SQS_KEY,
            }
        },
    },
    task_create_missing_queues=False,
    worker_disable_remote_control=True,
)

# here add the folder of your project with tasks
folders_with_tasks = []
celery_app.autodiscover_tasks(folders_with_tasks)


@celery_app.task
def test_task():
    import time

    time.sleep(10)
    return "Celery is working!"
