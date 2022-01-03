from fastapi import FastAPI

from routers.sign.api import router as sign_router


app = FastAPI()
app.include_router(sign_router)


@app.get('/')
def root():
    return 'Root message'
