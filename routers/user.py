from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from fastapi import APIRouter
from schemas.user import User

user_router=APIRouter()


@user_router.post('/login', tags=['auth'])
def login(user: User):
    """
    Login endpoint for user authentication

    Parameters:
        user: A User object with the email and password of the user to authenticate

    Returns:
        JSONResponse: A JSON response with a 200 status code and the JWT token if authentication is successful,
                      or a 401 status code with a message if authentication fails

    Raises:
        Exception: If an error occurs during the authentication process
    """
    if user.email == "admin@gmail.com" and user.password=="admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
