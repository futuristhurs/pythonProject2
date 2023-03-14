import sqlite3
import tkinter as tk

def create_table():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, completed INTEGER)")
    conn.commit()
    conn.close()

def add_task():
    task = entry_task.get()
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task, 0))
    conn.commit()
    conn.close()
    entry_task.delete(0, tk.END)

def mark_complete():
    task_id = listbox_tasks.get(tk.ACTIVE)[0]
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    view_incomplete_tasks()

def get_incomplete_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE completed = 0")
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_completed_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE completed = 1")
    tasks = c.fetchall()
    conn.close()
    return tasks

def delete_completed_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE completed = 1")
    conn.commit()
    conn.close()
    view_completed_tasks()

def view_incomplete_tasks():
    tasks = get_incomplete_tasks()
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        listbox_tasks.insert(tk.END, (task[0], task[1]))

def view_completed_tasks():
    tasks = get_completed_tasks()
    listbox_tasks.delete(0, tk.END)
    for task in tasks:
        listbox_tasks.insert(tk.END, (task[0], task[1]))

# Create GUI
root = tk.Tk()
root.title("To-Do List App")

# Create input field and "Add" button
frame_input = tk.Frame(root)
frame_input.pack(side=tk.TOP, padx=10, pady=10)
label_task = tk.Label(frame_input, text="Task:")
label_task.pack(side=tk.LEFT)
entry_task = tk.Entry(frame_input, width=50)
entry_task.pack(side=tk.LEFT)
button_add = tk.Button(frame_input, text="Add", command=add_task)
button_add.pack(side=tk.LEFT, padx=10)

# Create listbox and buttons for completed/incomplete tasks
frame_tasks = tk.Frame(root)
frame_tasks.pack(side=tk.TOP, padx=10, pady=10)
label_tasks = tk.Label(frame_tasks, text="Tasks:")
label_tasks.pack(side=tk.TOP)
listbox_tasks = tk.Listbox(frame_tasks, width=50)
listbox_tasks.pack(side=tk.TOP, padx=10, pady=10)
button_mark_complete = tk.Button(frame_tasks, text="Mark Complete", command=mark_complete)
button_mark_complete.pack(side=tk.LEFT, padx=10)
button_view_incomplete = tk.Button(frame_tasks, text="View Incomplete", command=view_incomplete_tasks)
button_view_incomplete.pack(side=tk.LEFT, padx=10)
button_view_completed = tk.Button(frame_tasks, text="View Completed", command=view_completed_tasks)
button_view_completed
button_view_completed.pack(side=tk.LEFT, padx=10)
button_delete_completed = tk.Button(frame_tasks, text="Delete Completed", command=delete_completed_tasks)
button_delete_completed.pack(side=tk.LEFT, padx=10)

#Create "Quit" button
button_quit = tk.Button(root, text="Quit", command=root.destroy)
button_quit.pack(side=tk.BOTTOM, pady=10)

#Create database table (if it doesn't exist already)
create_table()

#Load incomplete tasks into listbox by default
view_incomplete_tasks()

#Start the main event loop
root.mainloop()