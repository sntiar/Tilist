from task import Task

class Profile:
    def __init__(self, name):
        self.name = name
        self.task_list = []

    def add_task(self, task: Task):
        task.profile= self #attach the profile object to the taskS
        task.id= len(self.task_list)
        self.task_list.append(task)
        return task.profile, task.id

    

