import os
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from route.user_routes import router as user_router  
from dotenv import load_dotenv
load_dotenv()

PORT=os.getenv("PORT")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return JSONResponse(content={"message": "Hello World, desde FastApi"})

app.include_router(user_router, prefix="/user")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", PORT)) 
    uvicorn.run(app, host="0.0.0.0", port=port)