task_queue = []

def add_task(task):

    task_queue.append({
        "task": task,
        "status": "pending"
    })


def get_next_task():

    for t in task_queue:
        if t["status"] == "pending":
            t["status"] = "running"
            return t

    return None


def complete_task(task):

    task["status"] = "done"