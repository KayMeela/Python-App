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
