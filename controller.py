from fastapi import FastAPI, HTTPException, Request
from AuthenticationService import StubAuthenticationService, AuthenticationServiceImpl
from SchemasRepository import StubSchemaRepository
from SchemasService import SchemaService
from SolutionsService import StubSolutionsService
from model import Schema

repository = StubSchemaRepository()
auth_service = AuthenticationServiceImpl()
solutions_service = StubSolutionsService()
schema_service = SchemaService(repository, auth_service, solutions_service)
app = FastAPI()


@app.post("/schemas/")
async def create_schema(user_token: str):
    try:
        if not user_token:
            raise ValueError("User token is required")
        created_schema = schema_service.create_schema(user_token)
        return created_schema
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/schemas/")
async def get_all_schemas(user_token: str):
    try:
        schemas = schema_service.get_all_schemas(user_token)
        return schemas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/schemas/{schema_id}")
async def update_schema(schema: Schema, user_token: str):
    try:
        if not user_token:
            raise ValueError("User token is required")
        updated_schema = schema_service.update_schema(schema, user_token)
        return updated_schema
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/schemas/{schema_id}")
async def get_schema(schema_id: int, user_token: str):
    try:
        schema = schema_service.get_schema(schema_id, user_token)
        return schema
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8002)
