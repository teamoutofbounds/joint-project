'''
from .models.task import Task

@app.task
def assign_task(user):
    task = Task.objects.filter(task_status=0).first()
    if task:
        task.user = user
        # change status to automatically assigned
        task.task_status = 1
        task.save()
    return task
'''