from typing import Optional

import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import FastAPI, HTTPException, Request, Header
from AuthenticationService import StubAuthenticationService, AuthenticationServiceImpl
from SchemasRepository import StubSchemaRepository, FirebaseSchemasRepository
from SchemasService import SchemaService
from SolutionsService import StubSolutionsService, SolutionsServiceImpl
from model import Schema

# Initialize Firebase Admin SDK
# Use the service account key you downloaded to initialize the SDK
cred = credentials.Certificate("amr-routes-optimization-firebase-adminsdk-hpd3u-eaed4b8e2a.json")
firebase_admin.initialize_app(cred)

repository = FirebaseSchemasRepository()
auth_service = AuthenticationServiceImpl()
solutions_service = SolutionsServiceImpl()
schema_service = SchemaService(repository, auth_service, solutions_service)
app = FastAPI()


@app.post("/schemas/")
async def create_schema(authorization: Optional[str] = Header(None)):
    try:
        user_token = authorization.split(" ")[1]
        if not user_token:
            raise ValueError("User token is required")
        created_schema = schema_service.create_schema(user_token)
        return created_schema
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/schemas/")
async def get_all_schemas(authorization: Optional[str] = Header(None)):
    try:
        user_token = authorization.split(" ")[1]
        schemas = schema_service.get_all_schemas(user_token)
        return schemas
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/schemas/")
async def update_schema(schema: Schema, authorization: Optional[str] = Header(None)):
    try:
        user_token = authorization.split(" ")[1]
        if not user_token:
            raise ValueError("User token is required")
        updated_schema = schema_service.update_schema(schema, user_token)
        return updated_schema
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/schemas/{schema_id}")
async def get_schema(schema_id: int, authorization: Optional[str] = Header(None)):
    try:
        user_token = authorization.split(" ")[1]
        schema = schema_service.get_schema(schema_id, user_token)
        return schema
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8002)
