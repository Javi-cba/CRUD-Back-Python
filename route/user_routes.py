from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
from bson import ObjectId 
from db.connect_db import serialize_mongo_data, connect_db

db = connect_db()
usuariosCollection = db["users"]

router = APIRouter()

@router.get("/get")
async def get_usuarios():
    try:
        usuarios = list(usuariosCollection.find())
        
        usuarios_serializados = [serialize_mongo_data(usuario) for usuario in usuarios]

        return JSONResponse(content=usuarios_serializados, status_code=status.HTTP_200_OK)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/post")
async def post_usuarios(request: Request):
    try:
        data= await request.json()

        if not data:
            return JSONResponse(content={"error": "No se ha proporcionado el contenido del usuario"}, status_code=status.HTTP_400_BAD_REQUEST)

        usuariosCollection.insert_one(data)
        return JSONResponse(content={"message": "Usuario creado correctamente"}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put("/put")
async def put_usuarios(req: Request):
    try:
        data=await req.json()
        id = req.query_params.get("id") 
        if not id:
            return JSONResponse(content={"error": "No se ha proporcionado un ID"}, status_code=status.HTTP_400_BAD_REQUEST)
        if not data:
            return JSONResponse(content={"error": "No se ha proporcionado el contenido del usuario"}, status_code=status.HTTP_400_BAD_REQUEST)

        object_id = ObjectId(id)
        usuariosCollection.update_one({"_id": object_id}, {"$set": data})
        return JSONResponse(content={"message": "Usuario actualizado correctamente"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error":str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/delete")
async def delete_usuarios(req:Request):
    id = req.query_params.get("id")
    object_id = ObjectId(id)
 
    try:
        if not id:
            return JSONResponse(content={"error": "No se ha proporcionado un ID"}, status_code=status.HTTP_400_BAD_REQUEST)
        usuariosCollection.delete_one({"_id":object_id})
        return JSONResponse(content={"message": "Usuario actualizado correctamente"}, status_code=status.HTTP_200_OK)
    except Exception as e:
            return JSONResponse(content={"error":str(e)},status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)