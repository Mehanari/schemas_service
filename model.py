class WorkStation:
    def __init__(self, name: str, demand: float, x: float, y: float):
        self.name = name
        self.demand = demand
        self.x = x
        self.y = y

    def set_position(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_position(self) -> tuple:
        return self.x, self.y

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_demand(self, demand: float):
        self.demand = demand

    def get_demand(self) -> float:
        return self.demand

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "demand": self.demand,
            "x": self.x,
            "y": self.y
        }

    @staticmethod
    def from_json(data: dict) -> 'WorkStation':
        return WorkStation(
            name=data["name"],
            demand=data["demand"],
            x=data["x"],
            y=data["y"]
        )

    def __eq__(self, other):
        if not isinstance(other, WorkStation):
            return False
        return (self.name == other.name and
                self.demand == other.demand and
                self.x == other.x and
                self.y == other.y)

    def __hash__(self):
        return hash((self.name, self.demand, self.x, self.y))


class TransportationCost:
    def __init__(self, from_station: WorkStation, to_station: WorkStation, cost: float):
        self.from_station = from_station
        self.to_station = to_station
        self.cost = cost

    def get_from(self) -> WorkStation:
        return self.from_station

    def get_to(self) -> WorkStation:
        return self.to_station

    def get_cost(self) -> float:
        return self.cost

    def set_cost(self, cost: float):
        self.cost = cost

    def to_json(self) -> dict:
        return {
            "from_station": self.from_station.to_json(),
            "to_station": self.to_station.to_json(),
            "cost": self.cost
        }

    @staticmethod
    def from_json(data: dict) -> 'TransportationCost':
        return TransportationCost(
            from_station=WorkStation.from_json(data["from_station"]),
            to_station=WorkStation.from_json(data["to_station"]),
            cost=data["cost"]
        )

    def __eq__(self, other):
        if not isinstance(other, TransportationCost):
            return False
        return (self.from_station == other.from_station and
                self.to_station == other.to_station and
                self.cost == other.cost)

    def __hash__(self):
        return hash((self.from_station, self.to_station, self.cost))


class AMRParameters:
    def __init__(self, quantity: int, capacity: float):
        self.quantity = quantity
        self.capacity = capacity

    def set_quantity(self, quantity: int):
        self.quantity = quantity

    def get_quantity(self) -> int:
        return self.quantity

    def set_capacity(self, capacity: float):
        self.capacity = capacity

    def get_capacity(self) -> float:
        return self.capacity

    def to_json(self) -> dict:
        return {
            "quantity": self.quantity,
            "capacity": self.capacity
        }

    @staticmethod
    def from_json(data: dict) -> 'AMRParameters':
        return AMRParameters(
            quantity=data["quantity"],
            capacity=data["capacity"]
        )


class Schema:
    def __init__(self, schema_id: int, user_id: int):
        self.user_id = user_id
        self.id = schema_id
        self.workstations = set()
        self.transportation_costs = set()
        self.amr_parameters = None

    def add_workstation(self, station: WorkStation):
        self.workstations.add(station)

    def remove_workstation(self, station: WorkStation):
        self.workstations.discard(station)

    def get_all_workstations(self) -> list:
        return list(self.workstations)

    def set_transportation_cost(self, cost: TransportationCost):
        self.transportation_costs.add(cost)

    def remove_transportation_cost(self, cost: TransportationCost):
        self.transportation_costs.discard(cost)

    def get_transportation_costs(self) -> list:
        return list(self.transportation_costs)

    def set_amr_parameters(self, parameters: AMRParameters):
        self.amr_parameters = parameters

    def get_amr_parameters(self) -> AMRParameters:
        return self.amr_parameters

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "workstations": [station.to_json() for station in self.workstations],
            "transportation_costs": [cost.to_json() for cost in self.transportation_costs],
            "amr_parameters": self.amr_parameters.to_json() if self.amr_parameters else None
        }

    @staticmethod
    def from_json(data: dict) -> 'Schema':
        schema = Schema(schema_id=data["id"], user_id=data["user_id"])
        schema.workstations = {WorkStation.from_json(ws) for ws in data["workstations"]}
        schema.transportation_costs = {
            TransportationCost.from_json(tc) for tc in data["transportation_costs"]
        }
        if data["amr_parameters"]:
            schema.amr_parameters = AMRParameters.from_json(data["amr_parameters"])
        return schema
