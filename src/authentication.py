from lib2to3.pytree import Node
from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from jose import JWTError, jwt

from src.configuration.database import SECRET_KEY,ALGORITHM,database

router = APIRouter()

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generateHashPassword(password):
    return pwdContext.hash(password)

async def authorized(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):

    serverResponse = { 'username' :'' ,'userID': '' }

    credentialsException = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail  = "Could not validate credentials :(",
        headers = {"WWW-Authenticate": ""},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        userID   : str = payload.get("key")

        if username is None or userID is None:
            raise credentialsException

        serverResponse["username"] = username
        serverResponse["userID"]   = userID
   
    except JWTError:
        raise credentialsException  

    return serverResponse

@router.post("/login",)
async def login(formData: OAuth2PasswordRequestForm = Depends()):

    serverResponse = { 'status' : '', 'message' : '' }

    credentialsException = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": ""},
    )

    try:

        query = "SELECT * FROM users WHERE username = '" + formData.username + "'"
        
        databaseResponse = await database.fetch_one(query)

        if databaseResponse == None:
            raise credentialsException

        if not pwdContext.verify(formData.password, databaseResponse['password']):
            raise credentialsException

        expire = datetime.utcnow() + timedelta(minutes = 30)
        encodeData = { "sub" : formData.username, "exp" : expire, "key" : databaseResponse['id']}
 
        serverResponse["accessToken"] = jwt.encode(encodeData,SECRET_KEY,algorithm = ALGORITHM)
        serverResponse["response"]   = databaseResponse['username']
        serverResponse["status"] = 'success'

    except HTTPException:
        raise credentialsException

    except Exception as error:
        serverResponse["status"]  = 'error'
        serverResponse["message"] = str(error)
       
    return serverResponse

@router.post('/signup')
async def signup(request: Request):

    serverResponse = { 'status' : '', 'message' : '' }

    try:

        data = await request.form()

        username = data['username']
        email    = data['email']
        password = data['password']

        # query = "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)"
        # arguments = (str(username),str(email),generateHashPassword(str(password)))

        # databaseResponse = await database.execute(query,arguments)

        serverResponse['response']    = 'databaseResponse'
        serverResponse["status"]  = 'success'
        serverResponse["message"] = 'account created successfully'

    except KeyError as error:
        serverResponse["error"]   = str(error) + " is required"
        serverResponse["status"]  = 'error'
        serverResponse["message"] = 'Internal server error'
        
    except Exception as error:
        print(error)

        serverResponse["error"]   =  str(error)
        serverResponse["status"]  = 'error'
        serverResponse["message"] = 'Internal server error'
    
    return serverResponse
