import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from src.main import app, db_todos, TodoItem, get_default_due_date

client = TestClient(app)

# Fixture para reiniciar la base de datos en memoria antes de cada test
@pytest.fixture(autouse=True)
def reset_db():
    db_todos.clear()
    due_date_default = get_default_due_date()
    db_todos.extend([
        TodoItem(
            id=1, 
            title="Configurar GitHub Projects", 
            description="Crear el tablero y definir columnas", 
            completed=False,
            due_date=due_date_default
        ),
        TodoItem(
            id=2, 
            title="Probar endpoints de FastAPI", 
            description="Hacer peticiones GET y POST", 
            completed=False,
            due_date=due_date_default
        )
    ])


# -------------------------------------------------------------------
# Pruebas para GET /todos
# -------------------------------------------------------------------
def test_get_all_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert "due_date" in data[0]
    assert data[0]["due_date"] == get_default_due_date()


# -------------------------------------------------------------------
# Pruebas para GET /todos/{todo_id}
# -------------------------------------------------------------------
def test_get_todo_by_id_success():
    response = client.get("/todos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["due_date"] == get_default_due_date()

def test_get_todo_by_id_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


# -------------------------------------------------------------------
# Pruebas para POST /todos (Creación con fecha válida e inválida)
# -------------------------------------------------------------------
def test_create_todo_success():
    new_todo = {
        "title": "Aprender Pytest",
        "description": "Escribir pruebas unitarias",
        "completed": False,
        "due_date": "20/12/2026"
    }
    response = client.post("/todos", json=new_todo)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 3
    assert data["due_date"] == "20/12/2026"
    assert len(db_todos) == 3

# NUEVO TEST CASE: Validación de formato DD/MM/YYYY inválido
def test_create_todo_invalid_due_date_format():
    invalid_todo = {
        "title": "Tarea con fecha invalida",
        "description": "Usando formato YYYY-MM-DD en vez de DD/MM/YYYY",
        "completed": False,
        "due_date": "2026-12-20"  # Formato incorrecto
    }
    response = client.post("/todos", json=invalid_todo)
    # FastAPI/Pydantic devuelven HTTP 422 cuando la validación falla
    assert response.status_code == 422


# -------------------------------------------------------------------
# Pruebas para PUT /todos/{todo_id}
# -------------------------------------------------------------------
def test_update_todo_success():
    updated_payload = {
        "title": "Configurar GitHub Projects ACTUALIZADO",
        "description": "Nueva descripción",
        "completed": True,
        "due_date": "31/12/2026"
    }
    response = client.put("/todos/1", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["due_date"] == "31/12/2026"
    assert data["completed"] is True


# -------------------------------------------------------------------
# Pruebas para DELETE /todos/{todo_id}
# -------------------------------------------------------------------
def test_delete_todo_success():
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Tarea 1 eliminada correctamente"
    assert len(db_todos) == 1

