import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class ToDoList:
    def __init__(self,root):
        self.root = root
        self.root.title('To Do List')
        self.root.geometry('600x600')

        self.task_counter = 0
        self.task_dict = {}
        self.task_check_var = None

        self.global_font = ('rubik', 11, 'bold')

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
        self.modify_task_button_status() #disable new task btn until save is pressed

        self.task_check_var = tk.IntVar() #check button variable
       
        self.task_frame.grid_columnconfigure(0, weight=1)

        self.task_individual_frame = tk.Frame(self.task_frame, background='skyblue')
        self.task_individual_frame.grid(column=0, row=self.task_counter, sticky='ew')
        self.task_individual_frame.grid_columnconfigure(1, weight=1)


        self.task_cbtn = tk.Checkbutton(
            self.task_individual_frame, 
            text=f'Task {self.task_counter} : ', 
            font=self.global_font,
            variable=self.task_check_var,
            bg='skyblue',
            relief='solid',
            border=2
            )
        self.task_cbtn.grid(row=0, column=0, pady=10, padx=10, sticky='ew')

        self.task_entry = tk.Entry(self.task_individual_frame, font=self.global_font)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        #dictionary to store dinamicaly created widgets
        self.task_dict[self.task_counter] = {
            'variable': self.task_check_var, 
            'entry': self.task_entry, 
            'frame':self.task_individual_frame
            }

        self.task_save_btn = tk.Button(
            self.task_individual_frame, 
            text='SAVE', 
            font=('rubik',8,'normal'), 
            command=lambda:self.save_pressed(self.task_counter-1) 
            )
        self.task_save_btn.grid(row=0, column=2, padx=5, pady=5)
        '''
        had to substract 1 from the counter used as id in save btn and cancel btn 
        because the counter augments as the new task btn is pressed so if i didnt
        the id would be wrong for these btn functions as they only executes after
        the respective buttons are pressed
        '''
        self.task_cancel_btn = tk.Button(
            self.task_individual_frame, 
            text='CANCEL', 
            font=('rubik',8,'normal'), 
            command=lambda:self.cancel_pressed(self.task_counter-1) ) 
        self.task_cancel_btn.grid(row=0, column=3, padx=5, pady=5)

        self.task_counter += 1
            
    def entry_lenght_limit(self,text):
        return True if len(text)<=100 else False
   
    def forced_task_lenght(self,id):
        task_text = self.task_dict[id]['entry']
        if self.entry_lenght_limit(task_text.get()) is False: #if its under the limit ...
            task_text.delete(100,tk.END)

    def check_task_empty(self,id):
        task_text = self.task_dict[id]['entry']
        if task_text.get() != '': 
            return False
        messagebox.showerror('ERROR', ' Task is empty! ')
        return True      
            
    def modify_task_button_status(self):
        if self.task_btn['state'] == tk.NORMAL:
            self.task_btn.config(state='disabled')
        else:
            self.task_btn.config(state='normal')
    
    def entry_to_label(self, id):
        task_frame = self.task_dict[int(id)]['frame']
        entry_info = self.task_dict[int(id)]['entry'].grid_info()
        text = self.task_dict[int(id)]['entry'].get()
        self.task_dict[int(id)]['entry'].destroy()
        converted_task_lbl = tk.Label(task_frame,text=text,font=self.global_font, bg='skyblue')
        converted_task_lbl.grid(column=entry_info['column'], row=entry_info['row'])

    def save_pressed(self,counter):
        if self.check_task_empty(counter) is True:
            pass
        else:
            self.forced_task_lenght(counter)
            self.entry_to_label(counter)
            self.task_save_btn.destroy()
            self.task_cancel_btn.destroy()
            self.modify_task_button_status() # enable new task button again
    
    def cancel_pressed(self,id):
        self.task_dict[id]['frame'].destroy()
        self.modify_task_button_status()
        self.task_counter-=1 # reduces the counter as it is always augmented on new task btn press
        
        
if __name__ == "__main__": 
    root = tk.Tk()
    test = ToDoList(root)
    root.mainloop()