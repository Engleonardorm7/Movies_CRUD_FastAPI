from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers.user import user_router
from routers.movie import movie_router
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler



app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler) #controlador de errores, se ejecuta cuando ocurre un error
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind= engine)



movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')


