#!/usr/bin/env python3
"""
Simple CLI Todo Application
Supports add, list, and remove operations with local JSON storage.
"""

import argparse
import json
import os
import sys

TODO_FILE = 'todos.json'

def load_todos():
    """Load todos from JSON file."""
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_todos(todos):
    """Save todos to JSON file."""
    try:
        with open(TODO_FILE, 'w') as f:
            json.dump(todos, f, indent=2)
    except IOError as e:
        print(f"Error saving todos: {e}", file=sys.stderr)
        sys.exit(1)

def add_todo(task):
    """Add a new todo task."""
    todos = load_todos()
    todo = {
        'id': len(todos) + 1,
        'task': task,
        'completed': False
    }
    todos.append(todo)
    save_todos(todos)
    print(f"Added: {task}")

def list_todos():
    """List all todo tasks."""
    todos = load_todos()
    if not todos:
        print("No todos found.")
        return
    
    print("\nTodo List:")
    print("-" * 40)
    for i, todo in enumerate(todos, 1):
        status = "✓" if todo.get('completed', False) else "○"
        print(f"{i}. {status} {todo['task']}")
    print()

def remove_todo(index):
    """Remove a todo task by index."""
    todos = load_todos()
    if not todos:
        print("No todos to remove.")
        return
    
    if index < 1 or index > len(todos):
        print(f"Invalid index. Please choose between 1 and {len(todos)}.")
        return
    
    removed_todo = todos.pop(index - 1)
    save_todos(todos)
    print(f"Removed: {removed_todo['task']}")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description='Simple CLI Todo Application')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new todo')
    add_parser.add_argument('task', help='Task description')
    
    # List command
    subparsers.add_parser('list', help='List all todos')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove a todo by index')
    remove_parser.add_argument('index', type=int, help='Index of todo to remove')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_todo(args.task)
    elif args.command == 'list':
        list_todos()
    elif args.command == 'remove':
        remove_todo(args.index)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
