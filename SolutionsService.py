from abc import ABC, abstractmethod
import requests

SOLUTIONS_SERVICE_URL = "http://localhost:8003/"


class SolutionsService(ABC):
    @abstractmethod
    def mark_solution_obsolete(self, schema_id: int) -> None:
        pass


class StubSolutionsService(SolutionsService):
    def mark_solution_obsolete(self, schema_id: int) -> None:
        print(f"Marking solution for schema {schema_id} as obsolete")


class SolutionsServiceImpl(SolutionsService):
    def mark_solution_obsolete(self, schema_id: int) -> None:
        try:
            response = requests.put(f"{SOLUTIONS_SERVICE_URL}/mark_solution_obsolete-obsolete/{schema_id}")
            if response.status_code != 200:
                raise Exception(f"Error marking solution as obsolete: {response.json()}")
        except requests.RequestException as e:
            raise Exception(f"Error connecting to solutions service: {e}")
