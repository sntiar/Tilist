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

        self.global_font = ('rubik', 11, 'bold')

        self.profiles_dict = {} #add a default
        #self.profile_name = ''
        
        self.active_frame = None

        self.top_ui_setup()
        self.body_ui_setup()


    def top_ui_setup(self):
        top_font = self.global_font

        self.top_form = tk.Frame(self.root, background='steelblue', height=50)
        self.top_form.pack(side='top', fill='x')

        self.profile_btn= tk.Button(self.top_form, text='NEW POFILE', font=top_font, command=self.profile_gui)
        self.profile_btn.grid(column=1, row=2, padx=10, pady=20)

        self.task_btn= tk.Button(self.top_form, text='NEW TASK', font=top_font, command= self.task_creation)
        self.task_btn.grid(column=2, row=2, padx=10, pady=20)
        self.task_btn.config(state='disabled')

        self.sub_task_btn= tk.Button(self.top_form, text='NEW SUBTASK', font=top_font)
        self.sub_task_btn.grid(column=3, row=2, padx=10, pady=20)
        

        self.save_btn= tk.Button(self.top_form, text='SAVE', font=top_font)
        self.save_btn.grid(column=4, row=2, padx=10, pady=20)

        self.clear_btn= tk.Button(self.top_form, text='CLEAR', font=top_font)
        self.clear_btn.grid(column=5, row=2, padx=10, pady=20)

        self.profile_cbx = ttk.Combobox(self.top_form, font=top_font)
        self.profile_cbx.config(width=20, justify='center', state='readonly')
        self.profile_cbx.config(values=['default'])
        self.profile_cbx.current(0)
        self.profile_cbx.bind("<<ComboboxSelected>>",self.profile_cb)
        self.profile_cbx.grid(column=3, row=3, padx=10, pady=20, columnspan= 2)

        combo_lbl = tk.Label(self.top_form, text='Choose a profile : ', font=top_font, bg='steelblue')
        combo_lbl.grid(column=2, row=3, padx=10, pady=20)

    def body_ui_setup(self):

        border_frame = tk.Frame(self.root, bg='steelblue', ) #AUXILARY FRAME TO CHANGE THE BORDER'S COLOR
        border_frame.pack(fill='both',expand=True)
        
        self.body_frame = tk.Frame(border_frame, background='lightblue', height=50, relief='solid', border=5)
        self.body_frame.pack(padx=5, pady=5, side='bottom', fill='both',expand=True) 

        """self.task_frame= tk.Frame(self.body_frame, background='lightblue')
        self.task_frame.pack(side='bottom', fill='both',expand=True)"""
        
        tittle_frame = tk.Frame(self.body_frame, background='lightblue') #aux frame to keep the tittle label in place
        tittle_frame.pack(side='top', fill='x')
        tittle_frame.grid_columnconfigure(0, weight=1)   # allowing the label resizing by changing the father container
        
        task_lbl = tk.Label(tittle_frame, text='TASKS : ', font=('rubik', 20, 'bold'), bg='skyblue')
        task_lbl.config(relief='solid', border=2)# border
        task_lbl.grid(column=0, row=0, padx=5, pady=5, sticky='ew') #ew = east to west (expand with the window resizing)

    def task_creation(self):

        profile = self.profile_cbx.get()

        profile_counter = self.profiles_dict[profile][f'{profile}_counter']

        self.profiles_dict[profile][f'{profile}_counter'] = profile_counter+1

        p_frame = self.profiles_dict[profile]['frame']

        self.active_frame=p_frame

        #self.check_profile()

        self.modify_task_button_status() #disable new task btn until save is pressed

        task_check_var = tk.IntVar() #check button variable
       
        p_frame.grid_columnconfigure(0, weight=1)

        self.task_individual_frame = tk.Frame(p_frame, background='skyblue')
        self.task_individual_frame.grid(column=0, row=profile_counter, sticky='ew')
        self.task_individual_frame.grid_columnconfigure(1, weight=1)
        
        
        self.task_cbtn = tk.Checkbutton(
            self.task_individual_frame, 
            text=f'Task {profile_counter} : ', 
            font=self.global_font,
            variable=task_check_var,
            bg='skyblue',
            relief='solid',
            border=2,
            command=lambda actual_id=profile_counter:self.finished_task(actual_id) # original command=lambda:self.finished_task(self.task_counter-1) 
            )
        #self.task_frame_dict = {}
        
        self.task_cbtn.grid(row=0, column=0, pady=10, padx=10, sticky='ew')

        self.task_entry = tk.Entry(self.task_individual_frame, font=self.global_font)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        #dictionary to store dinamicaly created widgets
        self.task_dict[profile_counter] = {
            'variable': task_check_var, 
            'entry': self.task_entry, 
            'frame':self.task_individual_frame,
            'check':self.task_cbtn
            }
        
        self.profiles_dict[profile]['task_dict'] = self.task_dict #assign the whole dictionary to actual profile

        self.task_save_btn = tk.Button(
            self.task_individual_frame, 
            text='SAVE', 
            font=('rubik',8,'normal'), 
            command=lambda:self.save_pressed(profile_counter) 
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
            command=lambda:self.cancel_pressed(profile_counter) ) 
        self.task_cancel_btn.grid(row=0, column=3, padx=5, pady=5)

        self.modify_check_button_status(profile_counter) #disable check button until the task is saved

        #self.task_counter += 1
            
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
    
    def modify_check_button_status(self,id):
        ch_button = self.task_dict[id]['check']
        if ch_button['state'] == tk.NORMAL:
            ch_button.config(state='disabled')
        else:
            ch_button.config(state='normal')
        
    def entry_to_label(self, id):
        task_frame = self.task_dict[int(id)]['frame']
        entry_info = self.task_dict[int(id)]['entry'].grid_info()
        text = self.task_dict[int(id)]['entry'].get()
        self.task_dict[int(id)]['entry'].destroy()
        self.converted_task_lbl = tk.Label(task_frame,text=text,font=self.global_font, bg='skyblue')
        self.converted_task_lbl.grid(column=entry_info['column'], row=entry_info['row'], sticky='W')
        self.task_dict[id]['label'] = self.converted_task_lbl

    def save_pressed(self,counter):
        if self.check_task_empty(counter) is True:
            pass
        else:
            self.forced_task_lenght(counter)
            self.entry_to_label(counter)
            self.task_save_btn.destroy()
            self.task_cancel_btn.destroy()
            self.modify_task_button_status() # enable new task button again
            self.modify_check_button_status(counter) #enable check button #check if something broke after changing id
    
    def cancel_pressed(self,id):
        self.task_dict[id]['frame'].destroy()
        self.modify_task_button_status()
        #self.task_counter-=1 # reduces the counter as it is always augmented on new task btn press

    def finished_task(self,id):#function to cross out the task when checked 
        check = self.task_dict[id]['variable']
        text = self.task_dict[id]['label']
        if check.get():
            text.config(font=('rubik', 8, 'italic overstrike'))
        else:
            text.config(font=('rubik', 12, 'bold'))

    def profile_gui(self):
        self.profile_root = tk.Tk()
        self.profile_root.title('New profile')
        self.profile_root.geometry('200x100')
        self.profile_entry = tk.Entry(self.profile_root)
        self.profile_entry.pack(side='top', padx=10, pady=10)
        create_profile_btn = tk.Button(self.profile_root, text='Create profile', command=self.profile_creation_btn)
        create_profile_btn.pack(side='left', padx=10, pady=10)
        cancel_profile_btn = tk.Button(self.profile_root, text='Cancel', command=self.profile_root.destroy)
        cancel_profile_btn.pack(side='right', padx=10, pady=10)
        #test
        test_btn = tk.Button(self.profile_root, text='test', command=lambda:messagebox.showinfo('dictionary', f'profile dictionary :[ {self.profiles_dict.items()} ]'))
        test_btn.pack(side='bottom', padx=10, pady=10)

    def profile_creation_btn(self):
        profile_name = self.profile_entry.get()
        if profile_name != '':
            actual_values = list(self.profile_cbx['values'])
            actual_values.append(profile_name)
            self.profile_cbx.config(values=actual_values)
            self.profiles_dict[f'{profile_name}'] = {f'{profile_name}_counter':0}
            self.profile_root.destroy()
        else:
            messagebox.showerror('Error',f'input a proper profile name ! : {profile_name}')

    def profile_frame(self, key):
        if self.active_frame != None:
            self.active_frame.pack_forget()
        
        if 'frame' not in self.profiles_dict[key]:
            self.profiles_dict[key].update({'frame':tk.Frame(self.body_frame, bg='lightblue')})
            self.profiles_dict[key]['frame'].pack(side='bottom', fill='both',expand=True)
        else: 
            #self.active_frame.pack_forget()
            self.profiles_dict[key]['frame'].pack(side='bottom', fill='both',expand=True)
        
    def profile_cb(self, *_):
        profile = self.profile_cbx.get()
        self.profile_frame(profile)
        print(self.profile_cbx.get())
        #self.check_profile()
        self.task_btn.config(state='normal')
        """self.profiles_dict[profile]['frame'].config(bg='yellow', width=100, height=100)#weird bg to test existence
        self.profiles_dict[profile]['frame'].pack(side='bottom', padx=10, pady=10)"""
        self.active_frame = self.profiles_dict[profile]['frame']

    def check_profile(self):
        if self.profile_cbx.get() != 'default':
            self.task_btn.config(state='normal')
        self.task_btn.config(state='disabled')   
        
        
if __name__ == "__main__": 
    root = tk.Tk()
    test = ToDoList(root)
    root.mainloop()