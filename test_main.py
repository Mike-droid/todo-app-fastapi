import pytest
from fastapi.testclient import TestClient
from main import app, db_todos, TodoItem

client = TestClient(app)

# Fixture para reiniciar la base de datos en memoria antes de cada test
@pytest.fixture(autouse=True)
def reset_db():
    db_todos.clear()
    db_todos.extend([
        TodoItem(id=1, title="Configurar GitHub Projects", description="Crear el tablero y definir columnas", completed=False),
        TodoItem(id=2, title="Probar endpoints de FastAPI", description="Hacer peticiones GET y POST", completed=False)
    ])


# -------------------------------------------------------------------
# Pruebas para GET /todos
# -------------------------------------------------------------------
def test_get_all_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Configurar GitHub Projects"


# -------------------------------------------------------------------
# Pruebas para GET /todos/{todo_id}
# -------------------------------------------------------------------
def test_get_todo_by_id_success():
    response = client.get("/todos/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Configurar GitHub Projects"

def test_get_todo_by_id_not_found():
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


# -------------------------------------------------------------------
# Pruebas para POST /todos
# -------------------------------------------------------------------
def test_create_todo():
    new_todo = {
        "title": "Aprender Pytest",
        "description": "Escribir pruebas unitarias",
        "completed": False
    }
    response = client.post("/todos", json=new_todo)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 3
    assert data["title"] == "Aprender Pytest"
    
    # Verificamos que realmente se agregó a la "base de datos"
    assert len(db_todos) == 3


# -------------------------------------------------------------------
# Pruebas para PUT /todos/{todo_id}
# -------------------------------------------------------------------
def test_update_todo_success():
    updated_payload = {
        "title": "Configurar GitHub Projects ACTUALIZADO",
        "description": "Nueva descripción",
        "completed": True
    }
    response = client.put("/todos/1", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Configurar GitHub Projects ACTUALIZADO"
    assert data["completed"] is True

def test_update_todo_not_found():
    updated_payload = {
        "title": "Inexistente",
        "completed": True
    }
    response = client.put("/todos/999", json=updated_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


# -------------------------------------------------------------------
# Pruebas para DELETE /todos/{todo_id}
# -------------------------------------------------------------------
def test_delete_todo_success():
    response = client.delete("/todos/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Tarea 1 eliminada correctamente"
    
    # Verificamos que el elemento fue eliminado
    assert len(db_todos) == 1
    assert db_todos[0].id == 2

def test_delete_todo_not_found():
    response = client.delete("/todos/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tarea no encontrada"


