SECRET_KEY  = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM   = "HS256"

import databases
import sqlalchemy

DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/creativz"


database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

async def databaseStartup():
    try:
        await database.connect()
        print("Database connected successfully!")
    except Exception as error:
        error   =  str(error)
        print(error)

async def databaseShutdown():
    await database.disconnect()
    print("Database disconnected successfully!")