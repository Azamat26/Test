from celery import shared_task
import time

@shared_task
def say_hello():
    print("Hello from Celery task!")
    time.sleep(2)
    return "Done!"