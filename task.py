class Task:
    def __init__(self, content):
        self.content= content
        self.is_completed= False
        self.subtask_list = []

    def add_subtask(self, subtask):
         self.subtask_list.append(subtask)

    def __repr__(self):
        return f'Task : {self.content}. Status:{self.is_completed}'
    

if __name__=="__main__":
        test = Task("This is a test task")

        print(test)
        