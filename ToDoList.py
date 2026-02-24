import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from task import Task
from profile import Profile
import utils
from gui_manager import GuiManager 

class ToDoList:
    def __init__(self,root):
        self.root = root
        self.root.title('To Do List')
        self.root.geometry('650x400')
        self.root.update_idletasks()
        self.root.minsize(self.root.winfo_width(),self.root.winfo_height())
        self.global_font = ('rubik', 11, 'bold')
        self.active_frame = None

        self.gum = GuiManager()

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
        self.gum.register(self.profile_btn,{'NORMAL'},False)

        self.task_btn= tk.Button(
            self.top_form, 
            text='NEW TASK', 
            font=top_font, 
            command=lambda: self.task_creation(self.profiles_dict[self.profile_cbx.get()]))
        self.task_btn.grid(column=2, row=2, padx=10, pady=20)
        self.gum.register(self.task_btn,{'NORMAL'},False)

        self.save_btn= tk.Button(self.top_form, text='SAVE', font=top_font)
        self.save_btn.grid(column=3, row=2, padx=10, pady=20)
        self.gum.register(self.save_btn,{'NORMAL'},False)

        self.clear_btn= tk.Button(self.top_form, text='CLEAR', font=top_font)
        self.clear_btn.grid(column=4, row=2, padx=10, pady=20)
        self.gum.register(self.clear_btn,{'NORMAL'},False)

        self.profile_cbx = ttk.Combobox(self.top_form, font=top_font)
        self.profile_cbx.config(width=20, justify='center', state='readonly')
        self.profile_cbx.config(values=['default'])
        self.profile_cbx.current(0)
        self.profile_cbx.bind("<<ComboboxSelected>>",self.profile_cb)
        self.profile_cbx.grid(column=3, row=3, padx=10, pady=20, columnspan= 2)
        self.gum.register(self.profile_cbx,{'NORMAL'},True)

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
        new_task.subtask_id = 0
        _,id = profile.add_task(new_task)
        self.active_frame = profile.p_frame
        self.task_gui(new_task, id, profile)


    def task_gui(self, new_task: Task, id: int, profile: Profile):
        self.gum.set_active_mode('NEW_TASK')

        p_frame = profile.p_frame
        p_frame.pack(side='right', fill='both', expand=True) #reposition to implement the subtask panel

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
        self.gum.register(new_task.task_cbtn,{'NORMAL'},False)
        
        new_task.task_entry = tk.Entry(new_task.task_individual_frame, font=self.global_font)
        new_task.task_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.gum.register(new_task.task_entry,{'NEW_TASK'},False)
        
        vc = new_task.task_entry.register(lambda p:utils.entry_lenght_limit(100, p)),'%P' #replaced forced_task_entry function
        new_task.task_entry.config(validate='key', validatecommand=vc)

        new_task.task_cancel_btn = tk.Button(
            new_task.task_individual_frame, 
            text='CANCEL', 
            font=('rubik',8,'normal'), 
            command=lambda:self.cancel_pressed(new_task,0) ) # 0 is the flag to recognize the function is called from new task
        new_task.task_cancel_btn.grid(row=0, column=3, padx=5, pady=5)
        self.gum.register(new_task.task_cancel_btn,{'NEW_TASK'},False)

        new_task.subtask_frame = self.sub_task_frame()
        #new_task.subtask.subtask_frame.pack(side='right', fill='both', expand=True) #reposition to implement the subtask panel
        new_task.subtask_frame.grid_columnconfigure(0, weight=1)

        new_task.sub_task_panel_btn = tk.Button( ##subtask test
            new_task.task_individual_frame, 
            text='+', 
            font=('rubik',8,'bold'),
            state='disabled', 
            command=lambda p=new_task.subtask_frame:self.sub_task_panel(p)) 
        new_task.sub_task_panel_btn.grid(row=0, column=5, padx=5, pady=5)
        self.gum.register(new_task.sub_task_panel_btn,{'NORMAL','NEW_TASK'},False)

        new_task.sub_task_add_btn = tk.Button( ##subtask test
            new_task.task_individual_frame, 
            text='Add Subtask', 
            font=('rubik',8,'bold'),
            state='disabled', 
            command=lambda t=new_task :self.subtask_creation(t)) 
        new_task.sub_task_add_btn.grid(row=0, column=4, padx=5, pady=5)
        self.gum.register(new_task.sub_task_add_btn,{'NORMAL'},False)

        new_task.task_save_btn = tk.Button(
            new_task.task_individual_frame, 
            text='SAVE', 
            font=('rubik',8,'normal'), 
            command=lambda:self.save_pressed(new_task) 
            )
        new_task.task_save_btn.grid(row=0, column=2, padx=5, pady=5)
        self.gum.register(new_task.task_save_btn,{'NEW_TASK'},False)

    def entry_to_label(self, task_object: Task):
        
        task_frame = task_object.task_individual_frame
        entry_info = task_object.task_entry.grid_info()
        text = task_object.task_entry.get()
        task_object.content = text 
        self.gum.remove_destroyed(task_object.task_entry)
        task_object.task_entry.destroy()
        task_object.converted_task_lbl = tk.Label(task_frame,text=text,font=self.global_font, bg='skyblue')
        task_object.converted_task_lbl.grid(column=entry_info['column'], row=entry_info['row'], sticky='W')
        
    def save_pressed(self,task_object: Task):
        task_text = task_object.task_entry.get()
        if utils.task_empty(task_text):
            messagebox.showerror('Error', 'Input a valid task content.')
        else:
            self.gum.set_active_mode('NORMAL')
            self.entry_to_label(task_object)
            self.gum.remove_destroyed(task_object.task_save_btn)
            task_object.task_save_btn.destroy()
            self.gum.remove_destroyed(task_object.task_cancel_btn)
            task_object.task_cancel_btn.destroy()
    
    def cancel_pressed(self,task_object: Task,flag): #flag = 0 task, flag = 1 subtask
        if flag == 0:
            self.gum.set_active_mode('NORMAL')
            self.task_canceled_destruction(task_object)
            task_object.task_individual_frame.destroy()
            task_object.profile.task_list.remove(task_object)
        elif flag == 1:
            self.gum.set_active_mode('NORMAL')
            self.task_canceled_destruction(task_object.subtask)
            task_object.subtask.task_individual_frame.destroy()
            #task_object.subtask_list.remove(task_object.subtask)
            task_object.subtask_id -= 1

    def task_canceled_destruction(self,task_object: Task):
        child_widgets = task_object.task_individual_frame.winfo_children()
        for i in child_widgets:
            self.gum.remove_destroyed(i)

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
            self.active_frame=profile.p_frame

    def subpanel_mapping(self, sub_frame):
       # if not hasattr(self,'sub_frame'):return
        if sub_frame.winfo_ismapped():
            sub_frame.pack_forget()
       
    #start sub tasks # ts

    def sub_task_frame(self):
        sub_frame = tk.Frame(self.body_frame, bg="#afe9f3")   
        return sub_frame  

    def show_hide_sub(self,sub_frame):
        if sub_frame.winfo_ismapped():
           sub_frame.pack_forget()
        else:
           sub_frame.config(height=100, width=300)
           sub_frame.pack(side='left', fill='both' )

    def sub_task_panel(self, sub_frame):
        if sub_frame.winfo_exists():
            self.show_hide_sub(sub_frame)
        else:
            self.show_hide_sub(self.sub_task_frame())

    def add_subtask(self, task,subtask):
        task.add_subtask(subtask)

    def subtask_creation(self, task_obj):
        task = task_obj
        frame = task_obj.subtask_frame
        self.subtask_gui(task,task.subtask_id,frame)
        task.subtask_id += 1

    def subtask_gui(self, task, id, sub_frame):
        self.gum.set_active_mode('NEW_TASK')

        task.subtask = Task("")

        task.subtask.task_check_var = tk.IntVar() #check button variable
       
        task.subtask.task_individual_frame = tk.Frame(sub_frame, background='skyblue')
        task.subtask.task_individual_frame.grid(column=0, row=id, sticky='ew')
        task.subtask.task_individual_frame.grid_columnconfigure(1, weight=1)

        task.subtask.task_cbtn = tk.Checkbutton(
            task.subtask.task_individual_frame, 
            text=f'Task {id} : ', 
            font=self.global_font,
            variable=task.subtask.task_check_var,
            bg='skyblue',
            relief='solid',
            border=2,
            command=lambda t=task.subtask:self.finished_task(t) 
            )
        task.subtask.task_cbtn.grid(row=0, column=0, pady=10, padx=10, sticky='ew')
        self.gum.register(task.subtask.task_cbtn,{'NORMAL'},False)
        
        task.subtask.task_entry = tk.Entry(task.subtask.task_individual_frame, font=self.global_font)
        task.subtask.task_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.gum.register(task.subtask.task_entry,{'NEW_TASK'},False)
        
        vc = task.subtask.task_entry.register(lambda p:utils.entry_lenght_limit(100, p)),'%P' #replaced forced_task_entry function
        task.subtask.task_entry.config(validate='key', validatecommand=vc)

        task.subtask.task_cancel_btn = tk.Button(
            task.subtask.task_individual_frame, 
            text='CANCEL', 
            font=('rubik',8,'normal'), 
            command=lambda:self.cancel_pressed(task,1) ) # 1 is the flag to recognize the function is called from new task
        task.subtask.task_cancel_btn.grid(row=0, column=3, padx=5, pady=5)
        self.gum.register(task.subtask.task_cancel_btn,{'NEW_TASK'},False)

        task.subtask.task_save_btn = tk.Button(
            task.subtask.task_individual_frame, 
            text='SAVE', 
            font=('rubik',8,'normal'), 
            command=lambda:self.save_pressed(task.subtask) 
            )
        task.subtask.task_save_btn.grid(row=0, column=2, padx=5, pady=5)
        self.gum.register(task.subtask.task_save_btn,{'NEW_TASK'},False)
        

        
if __name__ == "__main__": 
    root = tk.Tk()
    test = ToDoList(root)
    
    root.mainloop()