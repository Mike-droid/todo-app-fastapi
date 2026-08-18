from fastapi import FastAPI
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, field_validator

# --- Importaciones de OpenTelemetry ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# 1. Configurar el proveedor de trazas y el exportador
provider = TracerProvider()
# ConsoleSpanExporter imprime las trazas directamente en la consola (ideal para desarrollo)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Establecer el proveedor global de trazas
trace.set_tracer_provider(provider)

app = FastAPI(title="Simple To-Do API con OpenTelemetry")

# 2. Instrumentar automáticamente la aplicación FastAPI
FastAPIInstrumentor.instrument_app(app)

# Función para obtener la fecha de hoy + 5 días en formato DD/MM/YYYY
def get_default_due_date() -> str:
    return (datetime.now() + timedelta(days=5)).strftime("%d/%m/%Y")

# Esquema actualizado para representarlo en las peticiones y respuestas
class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    due_date: str  # Formato esperado: DD/MM/YYYY

    @field_validator('due_date')
    @classmethod
    def validate_due_date_format(cls, value: str) -> str:
        try:
            datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError("El campo 'due_date' debe tener el formato DD/MM/YYYY (ej. 25/12/2026)")
        return value

# Base de datos temporal en memoria con el nuevo campo due_date
db_todos: List[TodoItem] = [
    TodoItem(
        id=1, 
        title="Configurar GitHub Projects", 
        description="Crear el tablero y definir columnas", 
        completed=False,
        due_date=get_default_due_date()
    ),
    TodoItem(
        id=2, 
        title="Probar endpoints de FastAPI", 
        description="Hacer peticiones GET y POST", 
        completed=False,
        due_date=get_default_due_date()
    )
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

