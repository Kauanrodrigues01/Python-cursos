import datetime
import os
import pickle
import sys

# Definindo a classe Task para gerenciar as tarefas
class Task:
    def __init__(self, title, description, due_date):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = False

    def __str__(self):
        status = 'Done' if self.completed else 'Pending'
        return f"{self.title} (Due: {self.due_date}) - {status}\n{self.description}"

# Função para carregar tarefas de um arquivo
def load_tasks(file_name='tasks.pkl'):
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            return pickle.load(f)
    return []

# Função para salvar tarefas em um arquivo
def save_tasks(tasks, file_name='tasks.pkl'):
    with open(file_name, 'wb') as f:
        pickle.dump(tasks, f)

# Função para adicionar uma nova tarefa
def add_task(tasks):
    title = input("Title: ")
    description = input("Description: ")
    due_date = input("Due Date (YYYY-MM-DD): ")
    try:
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Task not added.")
        return
    task = Task(title, description, due_date)
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully.")

# Função para exibir todas as tarefas
def view_tasks(tasks):
    if not tasks:
        print("No tasks available.")
        return
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

# Função para atualizar uma tarefa existente
def update_task(tasks):
    if not tasks:
        print("No tasks available to update.")
        return
    view_tasks(tasks)
    try:
        task_number = int(input("Enter task number to update: "))
        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number.")
            return
    except ValueError:
        print("Invalid input.")
        return
    task = tasks[task_number - 1]
    print(f"Updating task: {task}")
    task.title = input(f"New title (leave blank to keep '{task.title}'): ") or task.title
    task.description = input(f"New description (leave blank to keep current): ") or task.description
    due_date = input(f"New due date (YYYY-MM-DD, leave blank to keep '{task.due_date}'): ")
    if due_date:
        try:
            task.due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Date not changed.")
    save_tasks(tasks)
    print("Task updated successfully.")

# Função para excluir uma tarefa
def delete_task(tasks):
    if not tasks:
        print("No tasks available to delete.")
        return
    view_tasks(tasks)
    try:
        task_number = int(input("Enter task number to delete: "))
        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number.")
            return
    except ValueError:
        print("Invalid input.")
        return
    task = tasks.pop(task_number - 1)
    save_tasks(tasks)
    print(f"Task '{task.title}' deleted successfully.")

# Função para marcar uma tarefa como concluída
def mark_task_completed(tasks):
    if not tasks:
        print("No tasks available to mark as completed.")
        return
    view_tasks(tasks)
    try:
        task_number = int(input("Enter task number to mark as completed: "))
        if task_number < 1 or task_number > len(tasks):
            print("Invalid task number.")
            return
    except ValueError:
        print("Invalid input.")
        return
    tasks[task_number - 1].completed = True
    save_tasks(tasks)
    print("Task marked as completed.")

# Função para limpar tarefas concluídas
def clear_completed_tasks(tasks):
    completed_tasks = [task for task in tasks if task.completed]
    if not completed_tasks:
        print("No completed tasks to clear.")
        return
    print("Completed Tasks:")
    view_tasks(completed_tasks)
    confirmation = input("Are you sure you want to clear all completed tasks? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        tasks[:] = [task for task in tasks if not task.completed]
        save_tasks(tasks)
        print("Completed tasks cleared successfully.")
    else:
        print("Operation canceled.")

# Função para buscar tarefas por palavra-chave
def search_tasks(tasks):
    keyword = input("Enter keyword to search for in tasks: ").lower()
    found_tasks = [task for task in tasks if keyword in task.title.lower() or keyword in task.description.lower()]
    if not found_tasks:
        print("No tasks found matching the keyword.")
    else:
        print(f"Found {len(found_tasks)} task(s) matching the keyword:")
        view_tasks(found_tasks)

# Função para exibir estatísticas das tarefas
def show_task_stats(tasks):
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.completed)
    pending_tasks = total_tasks - completed_tasks
    print(f"Total Tasks: {total_tasks}")
    print(f"Completed Tasks: {completed_tasks}")
    print(f"Pending Tasks: {pending_tasks}")

# Função para salvar e sair do programa
def save_and_exit(tasks):
    save_tasks(tasks)
    print("Tasks saved successfully.")
    sys.exit()

# Função para exibir o menu
def display_menu():
    print("\nTask Manager")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Task as Completed")
    print("6. Clear Completed Tasks")
    print("7. Search Tasks")
    print("8. Show Task Statistics")
    print("9. Save and Exit")

# Função principal para gerenciar o fluxo do programa
def main():
    tasks = load_tasks()
    while True:
        display_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            update_task(tasks)
        elif choice == '4':
            delete_task(tasks)
        elif choice == '5':
            mark_task_completed(tasks)
        elif choice == '6':
            clear_completed_tasks(tasks)
        elif choice == '7':
            search_tasks(tasks)
        elif choice == '8':
            show_task_stats(tasks)
        elif choice == '9':
            save_and_exit(tasks)
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()