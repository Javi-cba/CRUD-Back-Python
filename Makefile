run:
	echo "Ejecutando el backend con uvicorn..."
    uvicorn main:app --host 0.0.0.0 --port $PORT
