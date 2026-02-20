def entry_lenght_limit(limit: int, text: str):
        return True if len(text)<=limit else False

def task_empty(text: str):
        return not text.strip() #strip() function removes blank spaces 
                                #at the end or at the start of the string and 
                                #'not' converts the return into a boolean 
                                #false for empty strings
         