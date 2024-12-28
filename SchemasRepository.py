from abc import ABC, abstractmethod
from typing import List
from model import Schema
from firebase_admin import firestore


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

    def create_schema(self, user_id: int) -> Schema:
        schema = Schema(user_id=user_id, id=len(self.schemas) + 1)
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


class FirebaseSchemasRepository(SchemasRepository):
    def __init__(self):
        self.db = firestore.client()
        self.collection_name = "schemas"
        self.counter_doc = "counters/schemas"

    def _get_next_id(self) -> int:
        """Fetch and increment the next available ID atomically."""
        counter_ref = self.db.document(self.counter_doc)
        transaction = self.db.transaction()

        @firestore.transactional
        def increment_counter(trans, cont_ref):
            snapshot = cont_ref.get(transaction=trans)
            if snapshot.exists:
                next_id = snapshot.get("next_id")
                trans.update(cont_ref, {"next_id": next_id + 1})
            else:
                next_id = 1
                trans.set(cont_ref, {"next_id": next_id + 1})
            return next_id

        return increment_counter(transaction, counter_ref)

    def get_schemas(self, user_id: int) -> List[Schema]:
        docs = self.db.collection(self.collection_name).where("user_id", "==", user_id).stream()
        return [Schema(**doc.to_dict()) for doc in docs]

    def create_schema(self, user_id: int) -> Schema:
        schema_id = self._get_next_id()
        schema = Schema(user_id=user_id, id=schema_id, workstations=set(), transportation_costs=set())
        self.db.collection(self.collection_name).document(str(schema_id)).set(schema.dict())
        return schema

    def update_schema(self, schema: Schema) -> Schema:
        if not schema.id:
            raise ValueError("Schema ID is required for updates")
        doc_ref = self.db.collection(self.collection_name).document(str(schema.id))
        doc_ref.set(schema.dict())
        return schema

    def schema_belongs_to_user(self, schema_id: int, user_id: int) -> bool:
        doc = self.db.collection(self.collection_name).document(str(schema_id)).get()
        if not doc.exists:
            return False
        return doc.to_dict()["user_id"] == user_id

    def get_schema(self, schema_id: int) -> Schema:
        doc = self.db.collection(self.collection_name).document(str(schema_id)).get()
        if not doc.exists:
            raise ValueError("Schema not found")
        return Schema(**doc.to_dict())
