import dataclasses

@dataclasses.dataclass 
class CounterParty:
    name: str
    id: str
    limits_per_currency: dict
    
    