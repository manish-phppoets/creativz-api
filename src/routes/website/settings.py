from fastapi import Depends, HTTPException, status, APIRouter, Request
from src.configuration.database import SECRET_KEY,ALGORITHM,database
router = APIRouter()


#Get website settings
@router.get('/')
async def index():
	
	serverResponse = { 'status' : '', 'message': '','response' : '' }
	
	credentialsException = HTTPException(
		status_code= status.HTTP_401_UNAUTHORIZED,
		detail="Incorrect username or password",
		headers={"WWW-Authenticate": ""},
	)
	
	try:
		query = "SELECT * FROM settings"
		dbResponse = await database.fetch_one(query)
		serverResponse["status"] = 'success' #// error, fail
		serverResponse["message"]   = 'Settings found successfully'
		serverResponse["response"]   = dbResponse

	except HTTPException:
		raise credentialsException

	except Exception as error:
		serverResponse["status"]  = 'error'
		serverResponse["message"]   = str(error)

	return serverResponse


#Get website menus
@router.get('/menus')
async def menus():
	
	serverResponse = { 'status' : '', 'message': '','response' : '' }
	
	credentialsException = HTTPException(
		status_code= status.HTTP_401_UNAUTHORIZED,
		detail="Incorrect username or password",
		headers={"WWW-Authenticate": ""},
	)
	
	try:
		query = "SELECT * FROM menus WHERE section_show= '0'"
		dbResponse = await database.fetch_all(query)
		serverResponse["status"] = 'success' #// error, fail
		serverResponse["message"]   = 'menu found successfully'
		serverResponse["response"]   = dbResponse

	except HTTPException:
		raise credentialsException

	except Exception as error:
		serverResponse["status"]  = 'error'
		serverResponse["message"]   = str(error)

	return serverResponse


#Get website home screens content
@router.get('/home-screens')
async def home_screens():
	
	serverResponse = { 'status' : '', 'message': '','response' : '' }
	
	credentialsException = HTTPException(
		status_code= status.HTTP_401_UNAUTHORIZED,
		detail="Incorrect username or password",
		headers={"WWW-Authenticate": ""},
	)
	
	try:
		query = "SELECT * FROM home_screens WHERE section_show = '0' ORDER BY order_no ASC"
		dbResponse = []
		dbResponse = await database.fetch_all(query)
		
		i = 0
		for row in dbResponse:
			if row.table_name != None:
				banner_query = "SELECT * FROM "+row.table_name+" WHERE is_status = '0' ORDER BY order_no ASC"
				child = await database.fetch_all(banner_query)
				dbResponse[i] = dict(row)
				dbResponse[i][row.layout] = child
			i += 1

		serverResponse["status"] = 'success' #// error, fail
		serverResponse["message"]   = 'Home screen layout found successfully'
		serverResponse["response"]   = dbResponse

	except HTTPException:
		raise credentialsException

	except Exception as error:
		serverResponse["status"]  = 'error'
		serverResponse["message"]   = str(error)

	return serverResponse