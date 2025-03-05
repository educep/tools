"""
Created by Analitika at 19/10/2024
contact@analitika.fr
"""
# External imports
from celery import Celery
import urllib.parse

# Internal imports
from config.settings import (
    AWS_ACCOUNT_ID,
    AWS_ACCESS_KEY_SQS_ID,
    AWS_SECRET_ACCESS_SQS_KEY,
    AWS_SQS_QUEUE_NAME,
    AWS_REGION,
)

"""
$env:AWS_PROFILE = "ank"
aws sqs list-queues --region eu-west-3
.\activate_pws.ps1
celery -A config.celery worker --pool=solo --loglevel=info
celery -A config.celery inspect registered

from config.celery import test_task
from webapp.tasks import test_task_child
test_task_child.delay()
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
    worker_disable_remote_control=True,  # <--- Add this line
)

celery_app.autodiscover_tasks(["webapp"])


@celery_app.task
def test_task():
    import time

    time.sleep(10)
    return "Celery is working!"
