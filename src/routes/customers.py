from fastapi import APIRouter, Depends
router = APIRouter()

@router.get('/view')
async def view():
	return 'welcome to customers list'