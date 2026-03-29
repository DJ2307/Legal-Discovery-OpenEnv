from dataclasses import dataclass
from openenv.core.env_server import Action as BaseAction, Observation as BaseObservation

@dataclass
class Action(BaseAction):
    action_type: str

@dataclass
class Observation(BaseObservation):
    state: str
  
