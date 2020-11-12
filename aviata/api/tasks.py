from celery import shared_task
import time

from api.utils import try_cache


@shared_task
def take_directions():
    try_cache()
    return 'Done'