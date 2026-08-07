from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Simple To-Do API")

# Esquema para representarlo en las peticiones y respuestas
class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

# Base de datos temporal en memoria
db_todos: List[TodoItem] = [
    TodoItem(id=1, title="Configurar GitHub Projects", description="Crear el tablero y definir columnas", completed=False),
    TodoItem(id=2, title="Probar endpoints de FastAPI", description="Hacer peticiones GET y POST", completed=False)
]

# 1. Obtener todas las tareas
@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return db_todos

# 2. Obtener una tarea por ID
@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    for todo in db_todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# 3. Crear una nueva tarea
@app.post("/todos", response_model=TodoItem, status_code=201)
def create_todo(todo: TodoItem):
    todo.id = len(db_todos) + 1 if db_todos else 1
    db_todos.append(todo)
    return todo

# 4. Actualizar el estado o contenido de una tarea
@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    for index, todo in enumerate(db_todos):
        if todo.id == todo_id:
            updated_todo.id = todo_id
            db_todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# 5. Eliminar una tarea
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(db_todos):
        if todo.id == todo_id:
            db_todos.pop(index)
            return {"message": f"Tarea {todo_id} eliminada correctamente"}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


