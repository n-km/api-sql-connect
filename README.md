# api-sql-connect
FastAPI connected to SQLite

### Database
<!-- Currently, the database is filled with some entrys, so if you want to have a new clean database, delete the data.db file. -->
The file ```data.db``` is a fresh new generated database for the project. If you want to be safe, just delete the file and run the API.
The file will be created automatically.

### Run the FastAPI
```powershell
python -m uvicorn main:app --reload --port 19999
```