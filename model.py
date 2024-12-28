from typing import Optional, List, Set
from pydantic import BaseModel


# --------------------------- WorkStation ---------------------------

class WorkStation(BaseModel):
    name: str
    demand: int
    depot_distance: int
    x: int
    y: int

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_demand(self, demand: int):
        self.demand = demand

    def get_demand(self) -> int:
        return self.demand

    def set_depot_distance(self, depo_distance: int):
        self.depot_distance = depo_distance

    def get_depot_distance(self) -> int:
        return self.depot_distance

    def __eq__(self, other):
        if not isinstance(other, WorkStation):
            return False
        return (self.name == other.name and
                self.demand == other.demand and
                self.x == other.x and
                self.y == other.y)

    def __hash__(self):
        return hash((self.name, self.demand, self.x, self.y))


# --------------------------- TransportationCost ---------------------------

class TransportationCost(BaseModel):
    from_station: WorkStation
    to_station: WorkStation
    cost: int

    def get_from(self) -> WorkStation:
        return self.from_station

    def get_to(self) -> WorkStation:
        return self.to_station

    def get_cost(self) -> int:
        return self.cost

    def set_cost(self, cost: int):
        self.cost = cost

    def __eq__(self, other):
        if not isinstance(other, TransportationCost):
            return False
        return (self.from_station == other.from_station and
                self.to_station == other.to_station and
                self.cost == other.cost)

    def __hash__(self):
        return hash((self.from_station, self.to_station, self.cost))


# --------------------------- AMRParameters ---------------------------

class AMRParameters(BaseModel):
    quantity: int
    capacity: int

    def set_quantity(self, quantity: int):
        self.quantity = quantity

    def get_quantity(self) -> int:
        return self.quantity

    def set_capacity(self, capacity: int):
        self.capacity = capacity

    def get_capacity(self) -> int:
        return self.capacity


# --------------------------- Schema ---------------------------

class Schema(BaseModel):
    user_id: int
    id: int
    workstations: Set[WorkStation] = set()
    transportation_costs: Set[TransportationCost] = set()
    amr_parameters: AMRParameters = AMRParameters(quantity=0, capacity=0)

    def add_workstation(self, station: WorkStation):
        self.workstations.add(station)

    def remove_workstation(self, station: WorkStation):
        self.workstations.discard(station)

    def get_all_workstations(self) -> List[WorkStation]:
        return list(self.workstations)

    def set_transportation_cost(self, cost: TransportationCost):
        self.transportation_costs.add(cost)

    def remove_transportation_cost(self, cost: TransportationCost):
        self.transportation_costs.discard(cost)

    def get_transportation_costs(self) -> List[TransportationCost]:
        return list(self.transportation_costs)

    def set_amr_parameters(self, parameters: AMRParameters):
        self.amr_parameters = parameters

    def get_amr_parameters(self) -> Optional[AMRParameters]:
        return self.amr_parameters
