# FastAPI To-Do List API

Una API REST sencilla y liviana para gestionar una lista de tareas (To-Do List), desarrollada con **FastAPI** y **Pydantic**. 

Este proyecto está diseñado principalmente como un entorno de práctica para experimentar con flujos de trabajo de **GitHub Projects**, gestión de *issues*, control de versiones y despliegue básico.

---

## 🚀 Requisitos previos

- **Python 3.8+**
- **pip** y **python3-venv**

---

## 🛠️ Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en tu entorno local (ejemplo para Ubuntu / Linux):

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/fastapi-todo.git](https://github.com/tu-usuario/fastapi-todo.git)
cd fastapi-todo

```

### 2. Crear y activar el entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt

```

---

## ▶️ Ejecutar la API

Con el entorno virtual activado, inicia el servidor de desarrollo con Uvicorn:

```bash
uvicorn main:app --reload

```

La API estará disponible en `http://127.0.0.1:8000`.

---

## 📖 Documentación Interactiva

FastAPI genera automáticamente documentación interactiva. Una vez ejecutando el servidor, abre en tu navegador:

* **Swagger UI:** [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs) (Recomendado para probar endpoints)
* **ReDoc:** [http://127.0.0.1:8000/redoc](https://www.google.com/search?q=http://127.0.0.1:8000/redoc)

---

## 📌 Endpoints disponibles

| Método | Endpoint | Descripción |
| --- | --- | --- |
| `GET` | `/todos` | Obtener todas las tareas |
| `GET` | `/todos/{id}` | Obtener una tarea por su ID |
| `POST` | `/todos` | Crear una nueva tarea |
| `PUT` | `/todos/{id}` | Actualizar una tarea existente |
| `DELETE` | `/todos/{id}` | Eliminar una tarea |

---

## 📁 Estructura del Proyecto

```text
fastapi-todo/
├── main.py           # Código fuente principal de la API
├── requirements.txt  # Lista de dependencias del proyecto
├── .gitignore        # Archivos ignorados por Git
└── README.md         # Documentación del proyecto

```

