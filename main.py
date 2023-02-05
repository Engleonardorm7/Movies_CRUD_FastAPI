from fastapi import FastAPI, Body, Path, Query, Request,HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from middlewares.jwt_bearer import JWTBearer

from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler) #controlador de errores, se ejecuta cuando ocurre un error


Base.metadata.create_all(bind= engine)



class User(BaseModel):
    email:str
    password:str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating:float = Field(ge=1, le=10)
    category:str = Field(min_length=5, max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 9.8,
                "category" : "Acción"
            }
        }

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


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password=="admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

#Show movies

@app.get(
          '/movies', 
          tags=['movies'], 
          response_model=List[Movie], 
          status_code=200, 
          dependencies=[Depends(JWTBearer())]
          )
def get_movies() -> List[Movie]:
    db=Session()
    result=db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Show a movie

@app.get(
          '/movies/{id}',
            tags=['movies'],
              response_model=Movie
              )
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db=Session()
    result= db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404, content={"Message":"Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Show movies by category

@app.get(
          '/movies/',
            tags=['movies'], 
            response_model=List[Movie]
            )
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db=Session()
    result= db.query(MovieModel).filter(MovieModel.category==category).all()
    if not result:
         return JSONResponse(status_code=404, content={"Message":"Not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
    # data = [ item for item in movies if item['category'] == category ]
    # return JSONResponse(content=data)

#Create a Movie

@app.post(
          '/movies', 
          tags=['movies'],
            response_model=dict,
              status_code=201
              )
def create_movie(movie: Movie) -> dict:
    db=Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()#se hace actualizacion para que los datos de la tabla se guarden
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

# Update a movie    

@app.put(
          '/movies/{id}', 
          tags=['movies'], 
          response_model=dict, 
          status_code=200
          )
def update_movie(id: int, movie: Movie)-> dict:
    db=Session()
    result=db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404,content={"message":"Not found "})
    result.title=movie.title
    result.overview=movie.overview
    result.year=movie.year
    result.rating=movie.rating
    result.category=movie.category
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

# Delete a movie 

@app.delete(
        '/movies/{id}',
        tags=['movies'],
        response_model=dict,
        status_code=200
        )
def delete_movie(id: int)-> dict:
    db=Session()
    result=db.query(MovieModel).filter(MovieModel.id==id).first()
    if not result:
        return JSONResponse(status_code=404,content={"message":"Not found "})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})
        
