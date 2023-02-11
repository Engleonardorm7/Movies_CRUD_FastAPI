
## Movies API

This project is a REST API made with FastAPI.

### Features
Features included:

- Data validation.
- CRUD of Movies
- Data persistance with JSON files (JSON files as database)


## Requirements:
- Python >= 3.10

## Installing
1. Clone or download de repository:
    ```
    $ git@github.com:Engleonardorm7/Movies_CRUD_FastAPI.git
    ```

2. Open the console inside the project directory and create a virtual environment.
    ```bash
    $ python -m venv venv
    $ source venv/Scripts/activate
    ```

3. Install the app
    ```bash
    (venv) $ pip install -r requirements.txt
    ```

## Run it locally
```
(venv) $ uvicorn main:app --reload
```

## Basic Usage
Once you are running the server open the [Swagger UI App](http://127.0.0.1:8000/docs#/) to checkout the API documentation.

## Author
Leonardo Rodriguez - [Github Profile](https://github.com/Engleonardorm7)

## Additional notes
The code is a program that implements the basic concepts of FastAPI to log into the application, create movies, search for movies, delete or modify movie content.
