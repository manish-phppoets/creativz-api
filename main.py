import uvicorn

if _name_ == "_main_":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)