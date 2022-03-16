"""

"""
from dataclasses import dataclass
from enum import Enum



@dataclass
class SwitchState:
    path_length: float
    voltages: tuple[float, float]

@dataclass
class SwitchStage:
    state_up: SwitchState
    state_dn: SwitchState


stage = SwitchStage(state_up=SwitchState(path_length=100, voltages=(2.3, 0.5)),
                    state_dn=SwitchState(path_length=0,   voltages=(2.3, 0.5)))

