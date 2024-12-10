from abc import ABC, abstractmethod
from typing import List

from SchemasRepository import SchemasRepository
from model import Schema


class SchemaService:
    def __init__(self, repository: SchemasRepository, auth_service, solutions_service):
        self.repository = repository
        self.auth_service = auth_service
        self.solutions_service = solutions_service

    def get_all_schemas(self, user_token: str) -> List[Schema]:
        user_id = self.auth_service.get_user_id(user_token)
        return self.repository.get_schemas(user_id)

    def create_schema(self, user_token: str) -> Schema:
        user_id = self.auth_service.get_user_id(user_token)
        return self.repository.create_schema(user_id)

    def update_schema(self, schema: Schema, user_token: str) -> Schema:
        user_id = self.auth_service.get_user_id(user_token)
        if not self.repository.schema_belongs_to_user(schema.id, user_id):
            raise ValueError("Unauthorized to update this schema")
        self.repository.update_schema(schema)
        self.solutions_service.mark_solution_obsolete(schema.id)
        return schema

    def get_schema(self, schema_id: int, user_token: str) -> Schema:
        user_id = self.auth_service.get_user_id(user_token)
        if not self.repository.schema_belongs_to_user(schema_id, user_id):
            raise ValueError("Unauthorized to access this schema")
        return self.repository.get_schema(schema_id)
