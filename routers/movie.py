from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from typing import List
from middlewares.jwt_bearer import JWTBearer
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder

from fastapi import APIRouter
from services.movie import MovieService
from schemas.movie import Movie


movie_router=APIRouter()

#Show movies   
@movie_router.get(
          '/movies', 
          tags=['movies'], 
          response_model=List[Movie], 
          status_code=200, 
          dependencies=[Depends(JWTBearer())]
          )
def get_movies() -> List[Movie]:
    db=Session()
    result=MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Show a movie

@movie_router.get(
          '/movies/{id}',
            tags=['movies'],
              response_model=Movie
              )
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db=Session()
    result= MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"Message":"Not found"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Show movies by category

@movie_router.get(
          '/movies/',
            tags=['movies'], 
            response_model=List[Movie]
            )
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db=Session()
    result= MovieService(db).get_movie_by_category(category)
    if not result:
         return JSONResponse(status_code=404, content={"Message":"Not found"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))
    # data = [ item for item in movies if item['category'] == category ]
    # return JSONResponse(content=data)

#Create a Movie

@movie_router.post(
          '/movies', 
          tags=['movies'],
            response_model=dict,
              status_code=201
              )
def create_movie(movie: Movie) -> dict:
    db=Session()
    MovieService(db).create_movie(movie)

    # new_movie = MovieModel(**movie.dict())
    # db.add(new_movie)
    # db.commit()#se hace actualizacion para que los datos de la tabla se guarden
    return JSONResponse(status_code=201, content={"message": "Se ha registrado la película"})

# Update a movie    

@movie_router.put(
          '/movies/{id}', 
          tags=['movies'], 
          response_model=dict, 
          status_code=200
          )
def update_movie(id: int, movie: Movie)-> dict:
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={"message":"Not found "})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado la película"})

# Delete a movie 

@movie_router.delete(
        '/movies/{id}',
        tags=['movies'],
        response_model=dict,
        status_code=200
        )
def delete_movie(id: int)-> dict:
    db=Session()
    result=MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404,content={"message":"Not found "})
    MovieService(db).delete_movie(id)
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})