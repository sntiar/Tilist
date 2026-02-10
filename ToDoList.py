import tkinter as tk
from tkinter import ttk


class ToDoList:
    def __init__(self,root):
        self.root= root
        self.root.title('To Do List')
        self.root.geometry('600x600')

        self.task_counter= 0
        self.global_font=('rubik', 11, 'bold')

        self.top_ui_setup()
        self.body_ui_setup()

    def top_ui_setup(self):
        top_font = self.global_font

        self.top_form = tk.Frame(self.root, background='steelblue', height=50)
        self.top_form.pack(side='top', fill='x')

        self.profile_btn= tk.Button(self.top_form, text='NEW POFILE', font=top_font)
        self.profile_btn.grid(column=1, row=2, padx=10, pady=20)

        self.task_btn= tk.Button(self.top_form, text='NEW TASK', font=top_font, command= self.task_creation)
        self.task_btn.grid(column=2, row=2, padx=10, pady=20)

        self.sub_task_btn= tk.Button(self.top_form, text='NEW SUBTASK', font=top_font)
        self.sub_task_btn.grid(column=3, row=2, padx=10, pady=20)

        self.save_btn= tk.Button(self.top_form, text='SAVE', font=top_font)
        self.save_btn.grid(column=4, row=2, padx=10, pady=20)

        self.clear_btn= tk.Button(self.top_form, text='CLEAR', font=top_font)
        self.clear_btn.grid(column=5, row=2, padx=10, pady=20)

        self.profile_cbx = ttk.Combobox(self.top_form, font=top_font)
        self.profile_cbx.config(width=20, justify='center', state='readonly')
        self.profile_cbx.config(values=[' -SELECT A PROFILE- '])
        self.profile_cbx.current(0)
        self.profile_cbx.grid(column=3, row=3, padx=10, pady=20, columnspan= 2)

        combo_lbl = tk.Label(self.top_form, text='Choose a profile : ', font=top_font, bg='steelblue')
        combo_lbl.grid(column=2, row=3, padx=10, pady=20)

    def body_ui_setup(self):

        border_frame = tk.Frame(self.root, bg='steelblue', ) #AUXILARY FRAME TO CHANGE THE BORDER'S COLOR
        border_frame.pack(fill='both',expand=True)
        
        self.body_frame = tk.Frame(border_frame, background='lightblue', height=50, relief='solid', border=5)
        self.body_frame.pack(padx=5, pady=5, side='bottom', fill='both',expand=True) 

        self.task_frame= tk.Frame(self.body_frame, background='lightblue')
        self.task_frame.pack(side='bottom', fill='both',expand=True)
        
        tittle_frame = tk.Frame(self.body_frame, background='lightblue') #aux frame to keep the tittle label in place
        tittle_frame.pack(side='top', fill='x')
        tittle_frame.grid_columnconfigure(0, weight=1)   # allowing the label resizing by changing the father container
        
        task_lbl = tk.Label(tittle_frame, text='TASKS : ', font=('rubik', 20, 'bold'), bg='skyblue')
        task_lbl.config(relief='solid', border=2)# border
        task_lbl.grid(column=0, row=0, padx=5, pady=5, sticky='ew') #ew = east to west (expand with the window resizing)

    def task_creation(self):
        '''NEED TO FIND A WAY TO MAKE EVERY ENTRY AND EVERY CHECK BUTTON TO BE A DIFFERENT AND INDEPENDENT ONE 
        EVERY TIME IS CREATED, SEARCHING THE INTERNET IT SAYS SOMETHING ABOUT "USING LIST OR DICTIONARIES TO
        DINAMICLY CREATE THE WIDGETS"
        '''
        self.task_counter += 1

        self.task_frame.grid_columnconfigure(1, weight=1)

        self.task_cbtn = tk.Checkbutton(self.task_frame, text=f'Task {self.task_counter} : ', font=self.global_font)
        self.task_cbtn.grid(row=self.task_counter, column=0, pady=10, padx=10, sticky='ew')

        self.task_entry = tk.Entry(self.task_frame, text='test', font=self.global_font)
        self.task_entry.grid(row=self.task_counter, column=1, padx=10, pady=10, sticky='ew')

        
        
        
if __name__ == "__main__": 
    root = tk.Tk()
    test = ToDoList(root)
    root.mainloop()