import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from task import Task
from profile import Profile
import utils


class ToDoList:
    def __init__(self,root):
        self.root = root
        self.root.title('To Do List')
        self.root.geometry('650x400')
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(),self.root.winfo_height())
        self.global_font = ('rubik', 11, 'bold')
        self.active_frame = None

        self.top_ui_setup()
        self.body_ui_setup()

        self.profiles_dict = {} 

        self.default_profile()
    
    def top_ui_setup(self):
        top_font = self.global_font

        self.top_form = tk.Frame(self.root, background='steelblue', height=50)
        self.top_form.pack(side='top', fill='x')

        self.profile_btn= tk.Button(self.top_form, text='NEW POFILE', font=top_font, command=self.profile_gui)
        self.profile_btn.grid(column=1, row=2, padx=10, pady=20)

        self.task_btn= tk.Button(
            self.top_form, 
            text='NEW TASK', 
            font=top_font, 
            command=lambda: self.task_creation(self.profiles_dict[self.profile_cbx.get()]))
        self.task_btn.grid(column=2, row=2, padx=10, pady=20)

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

        tittle_frame = tk.Frame(self.body_frame, background='lightblue') #aux frame to keep the tittle label in place
        tittle_frame.pack(side='top', fill='x')
        tittle_frame.grid_columnconfigure(0, weight=1)   # allowing the label resizing by changing the father container
        
        task_lbl = tk.Label(tittle_frame, text='TASKS : ', font=('rubik', 20, 'bold'), bg='skyblue')
        task_lbl.config(relief='solid', border=2)# border
        task_lbl.grid(column=0, row=0, padx=5, pady=5, sticky='ew') #ew = east to west (expand with the window resizing)

    def task_creation(self, profile: Profile):
        new_task = Task('')
        _,id = profile.add_task(new_task)
        self.active_frame = profile.p_frame
        self.task_gui(new_task, id, profile)

    def task_gui(self, new_task: Task, id: int, profile: Profile):

        p_frame = profile.p_frame
        p_frame.pack(side='right', fill='both') #reposition to implement the subtask panel

        self.modify_task_button_status() #disable new task btn until save is pressed
        self.modify_profile_cbx_status() #disable profile cbx

        new_task.task_check_var = tk.IntVar() #check button variable
       
        p_frame.grid_columnconfigure(0, weight=1)

        new_task.task_individual_frame = tk.Frame(p_frame, background='skyblue')
        new_task.task_individual_frame.grid(column=0, row=id, sticky='ew')
        new_task.task_individual_frame.grid_columnconfigure(1, weight=1)

        new_task.task_cbtn = tk.Checkbutton(
            new_task.task_individual_frame, 
            text=f'Task {id} : ', 
            font=self.global_font,
            variable=new_task.task_check_var,
            bg='skyblue',
            relief='solid',
            border=2,
            command=lambda t=new_task:self.finished_task(t) 
            )
        
        new_task.task_cbtn.grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        
        new_task.task_entry = tk.Entry(new_task.task_individual_frame, font=self.global_font)
        new_task.task_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        vc = new_task.task_entry.register(lambda p:utils.entry_lenght_limit(100, p)),'%P' #replaced forced_task_entry function
        new_task.task_entry.config(validate='key', validatecommand=vc)

        new_task.task_cancel_btn = tk.Button(
            new_task.task_individual_frame, 
            text='CANCEL', 
            font=('rubik',8,'normal'), 
            command=lambda:self.cancel_pressed(new_task) ) 
        new_task.task_cancel_btn.grid(row=0, column=3, padx=5, pady=5)

        new_task.sub_task_add_btn = tk.Button( ##subtask test
            new_task.task_individual_frame, 
            text='+', 
            font=('rubik',8,'bold'),
            state='disabled', 
            command=self.sub_task_panel) 
        new_task.sub_task_add_btn.grid(row=0, column=4, padx=5, pady=5)

        new_task.task_save_btn = tk.Button(
            new_task.task_individual_frame, 
            text='SAVE', 
            font=('rubik',8,'normal'), 
            command=lambda:self.save_pressed(new_task) 
            )
        new_task.task_save_btn.grid(row=0, column=2, padx=5, pady=5)

        self.modify_check_button_status(new_task) #disable check button until the task is saved


    def modify_task_button_status(self):
        if self.task_btn['state'] == tk.NORMAL:
            self.task_btn.config(state='disabled')
        else:
            self.task_btn.config(state='normal')
    
    def modify_check_button_status(self,task_object: Task):
        ch_button = task_object.task_cbtn
        if ch_button['state'] == tk.NORMAL:
            ch_button.config(state='disabled')
        else:
            ch_button.config(state='normal')
        
    def entry_to_label(self, task_object: Task):
        
        task_frame = task_object.task_individual_frame
        entry_info = task_object.task_entry.grid_info()
        text = task_object.task_entry.get()
        task_object.content = text
        task_object.task_entry.destroy()
        task_object.converted_task_lbl = tk.Label(task_frame,text=text,font=self.global_font, bg='skyblue')
        task_object.converted_task_lbl.grid(column=entry_info['column'], row=entry_info['row'], sticky='W')
        
    def save_pressed(self,task_object: Task):
        task_text = task_object.task_entry.get()
        if utils.task_empty(task_text):
            messagebox.showerror('Error', 'Input a valid task content.')
        else:
            self.entry_to_label(task_object)
            task_object.task_save_btn.destroy()
            task_object.task_cancel_btn.destroy()
            self.modify_task_button_status() # enable new task button again
            self.modify_check_button_status(task_object) #enable check button 
            self.modify_profile_cbx_status() #enable profile cbx
            task_object.sub_task_add_btn.config(state='normal')#make a function
    
    def cancel_pressed(self,task_object: Task):
        task_object.task_individual_frame.destroy()
        task_object.profile.task_list.remove(task_object)
        print (task_object.profile.task_list) #test
        self.modify_task_button_status()
        self.modify_profile_cbx_status() #enable profile cbx
       
    def finished_task(self,task_object: Task):#function to cross out the task when checked 
        check = task_object.task_check_var
        text = task_object.converted_task_lbl
        
        if check.get():
            text.config(font=('rubik', 8, 'italic overstrike'))
            task_object.is_completed = True
        else:
            text.config(font=('rubik', 12, 'bold'))
            task_object.is_completed = False

    #start profiles

    def modify_profile_cbx_status(self):#ttk widget
        cbx_state = str(self.profile_cbx.cget('state'))
        if cbx_state == tk.DISABLED :
            self.profile_cbx.config(state='readonly')
        else:
            self.profile_cbx.config(state='disabled')

    def profile_gui(self):
        self.profile_sub = tk.Toplevel(self.root)
        self.profile_sub.title('New profile')
        self.profile_sub.geometry('400x100')
        self.profile_sub.resizable(False,False)
        self.profile_sub.transient(self.root)
        self.profile_sub.grab_set()
        self.profile_sub.focus_set()
        self.profile_entry = tk.Entry(self.profile_sub)
        self.profile_entry.pack(side='top', padx=10, pady=10, fill='both')
        create_profile_btn = tk.Button(self.profile_sub, text='Create profile', command=self.profile_creation_btn)
        create_profile_btn.pack(side='left', padx=10, pady=10)
        cancel_profile_btn = tk.Button(self.profile_sub, text='Cancel', command=self.profile_sub.destroy)
        cancel_profile_btn.pack(side='left', padx=10, pady=10)
       
    def profile_creation_btn(self):
        
        profile_name = self.profile_entry.get()
        
        if profile_name != '':
            profile_object = Profile(profile_name) #object creation
            actual_values = list(self.profile_cbx['values'])
            actual_values.append(profile_name)
            self.profile_cbx.config(values=actual_values) #update profile combobox values
            self.profiles_dict[profile_name] = profile_object #dictionary of profile objects
            self.profile_sub.destroy()
        else:
            messagebox.showerror('Error',f'input a proper profile name ! : {profile_name}')

    def profile_frame(self, profile_object: Profile):
        if self.active_frame != None:
            self.active_frame.pack_forget()

        if hasattr(profile_object,'p_frame'):
            profile_object.p_frame.pack(side='right', fill='both', expand=True)
        else:
            profile_object.p_frame = tk.Frame(self.body_frame, bg='lightblue')
            profile_object.p_frame.pack(side='right', fill='both', expand=True)
        
    def profile_cb(self, *_): 
        profile_object = self.profiles_dict[self.profile_cbx.get()]
        self.profile_frame(profile_object)
        self.task_btn.config(state='normal')
        self.active_frame = profile_object.p_frame
        self.subpanel_mapping()

    def default_profile(self):
         if 'default' not in self.profiles_dict:
             self.profiles_dict['default'] = Profile('default')

         profile = self.profiles_dict['default']
         if hasattr(profile,'p_frame') == False:
            profile.p_frame = tk.Frame(self.body_frame, bg='lightblue')
            profile.p_frame.pack(side='right', fill='both', expand=True)

    def subpanel_mapping(self):
        if self.sub_frame.winfo_ismapped():
            self.sub_frame.pack_forget()
       
    #start sub tasks

    def sub_task_frame(self):
        self.sub_frame = tk.Frame(self.body_frame, bg="#afe9f3")       

    def show_hide_sub(self):
        if self.sub_frame.winfo_ismapped():
           self.sub_frame.pack_forget()
        else:
           self.sub_frame.config(height=100, width=300)
           self.sub_frame.pack(side='left', fill='both' )

    def sub_task_panel(self):
        if hasattr(self,'sub_frame') and self.sub_frame.winfo_exists():
            self.show_hide_sub()
        else:
            self.sub_task_frame()
            self.show_hide_sub()
        

        
if __name__ == "__main__": 
    root = tk.Tk()
    test = ToDoList(root)
    
    root.mainloop()