from fastapi import FastAPI
#from api.router import routers
import uvicorn
from api.auth.endpoints import auth_routers
app = FastAPI(root_path="/api/v1")

#for router in routers:
#    app.include_router(router)

app.include_router(auth_routers)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=True,
        port=8000

    )

