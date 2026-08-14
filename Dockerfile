# 1. Imagen base oficial y ligera (Slim basada en Debian)
FROM python:3.10-slim

# 2. Variables de entorno recomendadas para Python en contenedores
# - PYTHONDONTWRITEBYTECODE: Evita que Python genere archivos .pyc
# - PYTHONUNBUFFERED: Asegura que los logs de la API aparezcan en tiempo real en la consola
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. PRÁCTICA DE SEGURIDAD: Crear un usuario sin privilegios de root
RUN useradd -m -u 1000 appuser

# 5. OPTIMIZACIÓN DE CACHÉ: Copiar primero solo el requirements.txt
# Si no cambias tus dependencias, Docker usará la caché de esta capa al reconstruir
COPY requirements.txt .

# 6. Instalar dependencias sin guardar la caché del instalador de pip (reduce tamaño de imagen)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copiar el resto del código del proyecto asignándole la propiedad al usuario no-root
COPY --chown=appuser:appuser . .

# 8. Cambiar al usuario no privilegiado
USER appuser

# 9. Documentar el puerto que expondrá la aplicación
EXPOSE 8000

# 10. Comando para iniciar la API escuchando en todas las interfaces de red (0.0.0.0)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
