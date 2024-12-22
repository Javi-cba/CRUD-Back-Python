from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# URI de conexión
MONGO_URI = os.getenv("MONGO_URI")

# Variable global para el cliente
client = None

def connect_db():
    global client
    if client is None:
        try:
            # Crear una conexión global al cliente de MongoDB
            client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
            client.admin.command('ping')  # Comprobar conexión
            print("Conexión exitosa a MongoDB")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")
            raise
    # Retornar la base de datos específica
    return client["test"]

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
