import sys

def testing(task):
    print(f"References to task: {sys.getrefcount(task)}")