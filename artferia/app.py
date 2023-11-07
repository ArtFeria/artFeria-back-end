from fastapi import FastAPI

from routers import auth, events, users

app = FastAPI()

app.include_router(users.router)
app.include_router(events.router)
app.include_router(auth.router)


@app.get('/')
def read_root():
    return {'message': 'hello world!'}
