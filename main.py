import os
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from db.connect_db import connect_db, serialize_mongo_data
from dotenv import load_dotenv
load_dotenv()

PORT=os.getenv("PORT")

app = FastAPI()

db = connect_db()
usuariosCollection = db["usuarios"]

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return JSONResponse(content={"message": "Hello World, desde FastApi"})

@app.get("/usuarios/")
async def get_usuarios():
    try:
        # Obtener los documentos de la colección 'usuarios'
        usuarios = list(usuariosCollection.find())
        
        # Serializar los documentos para convertir ObjectId y datetime a formatos estándar
        usuarios_serializados = [serialize_mongo_data(usuario) for usuario in usuarios]

        # Devolver los datos como respuesta en formato JSON válido
        return JSONResponse(content=usuarios_serializados, status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", PORT)) 
    uvicorn.run(app, host="0.0.0.0", port=port)