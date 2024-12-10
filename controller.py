from fastapi import FastAPI, HTTPException, Request
from AuthenticationService import StubAuthenticationService
from SchemasRepository import StubSchemaRepository
from SchemasService import SchemaService
from SolutionsService import StubSolutionsService
from model import Schema

repository = StubSchemaRepository()
auth_service = StubAuthenticationService()
solutions_service = StubSolutionsService()
schema_service = SchemaService(repository, auth_service, solutions_service)
app = FastAPI()


@app.post("/schemas/")
async def create_schema(request: Request):
    try:
        body = await request.json()
        user_token = body.get("user_token")
        if not user_token:
            raise ValueError("User token is required")
        created_schema = schema_service.create_schema(user_token)
        return created_schema.to_json()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/schemas/")
async def get_all_schemas(user_token: str):
    try:
        schemas = schema_service.get_all_schemas(user_token)
        return [schema.to_json() for schema in schemas]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/schemas/{schema_id}")
async def update_schema(schema_id: int, request: Request):
    try:
        body = await request.json()
        schema = Schema.from_json(body)
        schema.id = schema_id
        user_token = body.get("user_token")
        if not user_token:
            raise ValueError("User token is required")
        updated_schema = schema_service.update_schema(schema, user_token)
        return updated_schema.to_json()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/schemas/{schema_id}")
async def get_schema(schema_id: int, user_token: str):
    try:
        schema = schema_service.get_schema(schema_id, user_token)
        return schema.to_json()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))