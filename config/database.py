import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name="../database.sqlite"
base_dir=os.path.dirname(os.path.realpath(__file__))#Leer di reccion actual del archivo database

database_url=f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}" #sqlite:/// es la forma en la que se conecta a una base de datos, se usa el metodo join para unir las urls

engine = create_engine(database_url, echo=True)
"""representa el motor de la base de datos, con el comando “echo=True” para que al momento de realizar la base de datos,
me muestre por consola lo que esta realizando, que seria el codigo"""

Session = sessionmaker(bind=engine)
#Se crea sesion para conectarse a la base de datos, se enlaza con el comando “bind” y se iguala a engine
Base = declarative_base()
#Sirve para manipular todas las tablas de la base de datos

