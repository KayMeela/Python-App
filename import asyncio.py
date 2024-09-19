import asyncio
from datetime import datetime

class TodoItem:
    def __init__(self, id, description, created_on=None):
        self.id = id
        self.description = description
        self.created_on = created_on or datetime.now()
        self.completed_on = None

class TodoApp:
    def __init__(self):
        self._todos = {}
        self._next_id = 1

    @classmethod
    def new(cls):
        return cls()

    async def create(self, description):
        new_id = self._next_id
        self._next_id += 1
        todo_item = TodoItem(new_id, description)
        self._todos[new_id] = todo_item
        return todo_item

    async def update(self, todo_id, description=None, completed=None):
        if todo_id not in self._todos:
            raise ValueError(f"Todo item with ID {todo_id} not found")

        todo_item = self._todos[todo_id]
        if description is not None:
            todo_item.description = description
        if completed is not None:
            todo_item.completed_on = datetime.now() if completed else None

    async def delete(self, todo_id):
        if todo_id not in self._todos:
            raise ValueError(f"Todo item with ID {todo_id} not found")

        del self._todos[todo_id]

    async def complete(self, todo_id):
        await self.update(todo_id, completed=True)

    async def filter(self, criteria):
        if criteria == "completed":
            return [item for item in self._todos.values() if item.completed_on is not None]
        elif criteria == "todo":
            return [item for item in self._todos.values() if item.completed_on is None]
        elif isinstance(criteria, str):
            # Partial text search
            return [item for item in self._todos.values() if criteria.lower() in item.description.lower()]
        else:
            raise ValueError(f"Invalid filter criteria: {criteria}")

# Example usage (assuming async/await is supported)
async def main():
    app = TodoApp.new()
    await app.create("Buy groceries")
    await app.create("Clean the house")
    await app.complete(1)

    todos = await app.filter("todo")
    for todo in todos:
        print(f"Task: {todo.description}")

if __name__ == "__main__":
    asyncio.run(main())



    import pytest
from src.todo_app import TodoApp, TodoItem

pytestmark = pytest.mark.asyncio

async def test_create_todo():
    app = TodoApp.new()
    todo = await app.create("Buy milk")
    assert isinstance(todo, TodoItem)
    assert todo.id > 0
    assert todo.description == "Buy milk"

async def test_update_todo():
    app = TodoApp.new()
    todo = await app.create("Write report")
    await app.update(todo.id, description="Finish report")

    updated_todo = await app.filter(todo.id)
    assert len(updated_todo) == 1
    assert updated_todo[0].description == "Finish report"

async def test_delete_todo():
    app = TodoApp.new()
    await app.create