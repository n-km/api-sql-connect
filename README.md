# api-sql-connect
FastAPI connected to SQLite

### Project
This is a simplified FastAPI setup connected to SQLite.
It has a basic `register` + `login` flow, and you can list users.

The schema is simple: store `email` (unique) and `password` in the sqlite database.
For testing purposes, the password is saved as-is.

### Endpoints
- `POST /register` => create a new user in the database.
  Body: `{"email":"example@mail.com","password":"yourpassword"}`
- `POST /login` => check if email+password exists.
  Body: `{"email":"example@mail.com","password":"yourpassword"}`
- `GET /users` => returns all users (`id` + `email`).

### CORS
The API has CORS enabled for all origins, so a frontend can call it directly.

### Database
<!-- Currently, the database is filled with some entrys, so if you want to have a new clean database, delete the data.db file. -->
The file ```data.db``` is a fresh new generated database for the project. If you want to be safe, just delete the file and run the API.
The file will be created automatically.

### Run the FastAPI
```powershell
python -m uvicorn main:app --reload --port 19999
```