from typing import List, Optional
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Inicializaremos una variable donde tendrá todas las características de una API REST
app = FastAPI()

# Definimos el modelo
class Curso(BaseModel):
    id : Optional[str] = None
    nombre : str
    descripcion: Optional[str] = None
    nivel: str
    duracion: int

# Simularemos una base de datos
cursos_db = []

# Read (lectura) Get all: Leer todos los recursos que tenemos en la base de datos
@app.get("/cursos/", response_model = List[Curso])
def obtener_cursos():
    return cursos_db

# Create (crear) Post: agregamos un nuevo recurso a nuestra base de datos
@app.post("/cursos/", response_model = Curso)
def crear_usuario(curso:Curso):
    curso.id = str (uuid.uuid4()) # Usamos UUID para generar un ID único e irrepetible
    cursos_db.append(curso)
    return curso

# Create (lectura) GET (Individual): Se usará para leer el curso que coincida
@app.get("/cursos/{curso_id}", response_model=Curso)
def obtener_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado") # Raise lo que hace es cortar la ejecución
    return curso

# Update (Actualizar/Modificar) PUT: Modificará los recursos que coincidan con el ID que mandemos
@app.put("/cursos/{curso_id}", response_model=Curso)
def actualizar_curso(curso_id:str, curso_actualizado:Curso):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None)
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    curso_actualizado.id = curso_id
    index = cursos_db.index(curso) # Buscamos el índice excato donde está el curso en nuestra línea (DB)
    cursos_db[index] = curso_actualizado
    return curso_actualizado

# Delete (Borrar) DELETE: Eliminaremos un recurso que coincida con el ID que mandamos
@app.delete("/cursos/{curso_id}", response_model=Curso)
def eliminar_curso(curso_id:str):
    curso = next((curso for curso in cursos_db if curso.id == curso_id), None) # Con next tomamos la primera coincidencia del array
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    cursos_db.remove(curso)
    return curso
