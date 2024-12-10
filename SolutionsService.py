from abc import ABC, abstractmethod


class SolutionsService(ABC):
    @abstractmethod
    def mark_solution_obsolete(self, schema_id: int) -> None:
        pass


class StubSolutionsService(SolutionsService):
    def mark_solution_obsolete(self, schema_id: int) -> None:
        print(f"Marking solution for schema {schema_id} as obsolete")
