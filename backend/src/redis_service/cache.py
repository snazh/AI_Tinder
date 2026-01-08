APP = "fastapi_app"


def task_queue():
    return f"{APP}:queue:tasks"


def processing_queue():
    return f"{APP}:queue:processing"
