from flask import Flask, render_template, request, redirect
import re
import pickle
import os

app = Flask(__name__)

TODO_FILE = 'todo.pkl'
todo_list = []

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'rb') as f:
            return pickle.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, 'wb') as f:
        pickle.dump(todos, f)

todo_list = load_todos()

def is_valid_email(email):
    """A simple regex for basic email validation."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

@app.route('/')
def index():
    return render_template('index.html', todos=todo_list)

@app.route('/submit', methods=['POST'])
def submit():
    if 'save' in request.form:
        save_todos(todo_list)
        return redirect('/')
    else:
        task = request.form['task']
        email = request.form['email']
        priority = request.form['priority']

        error = None
        if not task:
            error = 'Task description cannot be empty.'
        elif not is_valid_email(email):
            error = 'Invalid email address.'
        elif priority not in ['Low', 'Medium', 'High']:
            error = 'Invalid priority level.'

        if error:
            return redirect('/') # Could add error message with flash
        else:
            todo_list.append({'task': task, 'email': email, 'priority': priority})
            return redirect('/')

@app.route('/clear', methods=['POST'])
def clear():
    global todo_list
    todo_list = []
    return redirect('/')

@app.route('/delete/<int:index>', methods=['POST'])
def delete_todo(index):
    global todo_list
    if 0 <= index < len(todo_list):
        del todo_list[index]
        save_todos(todo_list) # Save the list after deletion
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)