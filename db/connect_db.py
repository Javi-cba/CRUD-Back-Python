from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# URI de conexión
MONGO_URI = os.getenv("MONGO_URI")

def connect_db():
    try:
        # conectamos al cliente de MongoDB
        client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
        
        # mi base de datos
        db = client["test"]  
        print("Conexión exitosa a la base de datos.")
        
        collections = db.list_collection_names()
        print(f"Colecciones disponibles: {collections}")
        
        return db
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        raise

def serialize_mongo_data(data):
    """Función para convertir los objetos MongoDB a un formato estándar (JSON válido)."""
    if isinstance(data, ObjectId):
        return str(data)
    elif isinstance(data, datetime.datetime):
        return data.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(data, dict):
        return {key: serialize_mongo_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [serialize_mongo_data(item) for item in data]
    return data
