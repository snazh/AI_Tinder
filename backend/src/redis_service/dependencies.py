from .queues import Queue
from .keys import AI_QUEUE, EMAILS_QUEUE


def get_email_queue() -> Queue:
    return Queue(queue=EMAILS_QUEUE)


def get_ai_task_queue() -> Queue:
    return Queue(queue=AI_QUEUE)
