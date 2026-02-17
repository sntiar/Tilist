
# ToDoList Application (Python/Tkinter)

**DISCLAIMER:** This is purely a learning project. It was never intended as a production-ready application; rather, it is used specifically to explore Python, Tkinter, data flow, state management, and dynamically created widgets.

## 📋 About the Project
This application is designed to help users manage productivity through a goal-oriented profile system. Unlike traditional user accounts, these "profiles" represent different life categories or major goals.

### Planned Features:
*   **Task Creation**: Create tasks with the ability to strike them out upon completion.
*   **Profile Management**: Group tasks under specific profiles (e.g., "Work", "Personal Project", "Coding project A", etc.).
*   **Sub-Tasks**: Break down complex tasks into smaller, manageable steps.
*   **Data Persistence**: Implementation of a database to store and recover profiles, tasks, and sub-tasks across sessions.

### 🛠 Current Status: Developing Profile Contexts
I am currently tackling **State Management**. 
- [x] Successfully implemented dynamic profile creation and switching.
- [wip] Debugging **Task-to-Profile Parentage** (ensuring tasks stay with their respective profiles).
- [wip] Refactoring **Checkbutton logic** to handle unique task states across multiple frames.

Side Note : As i started working on the 'profiles', i had to refactor some functions, so there may be variables or lines of code that arent being used or outdated comments that are pending for a clean up.


Note on Development: This project was developed with the assistance of AI as a learning mentor. I utilized AI to help debug complex logic errors (such as dictionary state management and late-binding issues) and to refine the project's documentation. Every architectural decision and fix was manually implemented and tested to ensure a proper understanding of the underlying concepts.

