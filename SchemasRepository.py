from abc import ABC, abstractmethod
from typing import List
from model import Schema


class SchemasRepository(ABC):
    @abstractmethod
    def get_schemas(self, user_id: int) -> List[Schema]:
        pass

    @abstractmethod
    def create_schema(self, user_id: int) -> Schema:
        pass

    @abstractmethod
    def update_schema(self, schema: Schema) -> Schema:
        pass

    @abstractmethod
    def schema_belongs_to_user(self, schema_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def get_schema(self, schema_id: int) -> Schema:
        pass


class StubSchemaRepository(SchemasRepository):
    def __init__(self):
        self.schemas = {}

    def get_schemas(self, user_id: int) -> List[Schema]:
        return [schema for schema in self.schemas.values() if schema.user_id == user_id]

    def create_schema(self, schema: Schema) -> Schema:
        self.schemas[schema.id] = schema
        return schema

    def update_schema(self, schema: Schema) -> Schema:
        if schema.id not in self.schemas:
            raise ValueError("Schema not found")
        self.schemas[schema.id] = schema
        return schema

    def schema_belongs_to_user(self, schema_id: int, user_id: int) -> bool:
        schema = self.schemas.get(schema_id)
        return schema is not None and schema.user_id == user_id

    def get_schema(self, schema_id: int) -> Schema:
        if schema_id not in self.schemas:
            raise ValueError("Schema not found")
        return self.schemas[schema_id]
