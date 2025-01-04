run:
	echo "Ejecutando el backend con uvicorn..."
    uvicorn main:app --host 0.0.0.0 --port 8081
