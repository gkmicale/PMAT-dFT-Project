import csv
import itertools
from typing import Iterable

import numpy as np
import time
from switching_stage import SwitchStage, SwitchState

ΔL = 20.  # noqa

# Create the stages:
stage1 = SwitchStage(state_up=SwitchState(path_length=2 * ΔL, voltages=(2.3, 0.5)),
                     state_dn=SwitchState(path_length=0 * ΔL, voltages=(2.3, 0.5)))

stage2 = SwitchStage(state_up=SwitchState(path_length=8 * ΔL, voltages=(2.3, 0.5)),
                     state_dn=SwitchState(path_length=0 * ΔL, voltages=(2.3, 0.5)))

stage3 = SwitchStage(state_up=SwitchState(path_length=32 * ΔL, voltages=(2.3, 0.5)),
                     state_dn=SwitchState(path_length=0 * ΔL, voltages=(2.3, 0.5)))

stage4 = SwitchStage(state_up=SwitchState(path_length=128 * ΔL, voltages=(2.3, 0.5)),
                     state_dn=SwitchState(path_length=0 * ΔL, voltages=(2.3, 0.5)))

stage5 = SwitchStage(state_up=SwitchState(path_length=512 * ΔL, voltages=(-2.35, -0.5)),
                     state_dn=SwitchState(path_length=0 * ΔL, voltages=(-0.5, -2.35)))

stage6 = SwitchStage(state_up=SwitchState(path_length=6 * ΔL, voltages=(2.3, 0.5)),
                     state_dn=SwitchState(path_length=2 * ΔL, voltages=(2.3, 0.5)))

stage7 = SwitchStage(state_up=SwitchState(path_length=24 * ΔL, voltages=(2.3, 0.5)),
                     state_dn=SwitchState(path_length=8 * ΔL, voltages=(2.3, 0.5)))

stage8 = SwitchStage(state_up=SwitchState(path_length=96 * ΔL, voltages=(2.3, 0.5)),
                     state_dn=SwitchState(path_length=32 * ΔL, voltages=(2.3, 0.5)))

stage9 = SwitchStage(state_up=SwitchState(path_length=128 * ΔL, voltages=(2.3, 0.5)),
                     state_dn=SwitchState(path_length=384 * ΔL, voltages=(2.3, 0.5)))

stage10 = SwitchStage(state_up=SwitchState(path_length=512 * ΔL, voltages=(2.3, 0.5)),
                      state_dn=SwitchState(path_length=1536 * ΔL, voltages=(2.3, 0.5)))

arm_up = [stage1, stage2]#, stage3, stage4, stage5]
arm_dn = [stage6, stage7]#, stage8, stage9, stage10]

State = tuple[int, ...]


def find_OPL(stages: list[SwitchStage, ...], state: State):
    length = 0

    for i in range(len(stages)):
        if state[i] == 1:
            length = length + stages[i].state_up.path_length

        elif state[i] == 0:
            length = length + stages[i].state_dn.path_length

    return length

print( find_OPL( arm_up, (1,1) ) )

def calculate_OPD(arm_1: list[SwitchStage, ...], arm_2: list[SwitchStage, ...], state_combo: tuple[State, State]):
    arm_1_state = state_combo[0]
    arm_2_state = state_combo[1]

    OPL_1 = find_OPL(arm_1, arm_1_state)
    OPL_2 = find_OPL(arm_2, arm_2_state)

    return abs(OPL_1 - OPL_2)


def permute_switches(arm_1: list, arm_2: list):
    """
    Create all the permutations of switches and corresponds them to their respective
    optical path difference (OPD)

    Args:
        arm_1 (list): list of stages (SwitchStage) in first arm
        arm_2 (list): list of stages (SwitchStage) in second arm

    Returns:
        device_states (dict): {keys=OPD, values=(tuple[Iterable, Iterable]) }
            where each list in the tuple contains 1s and 0s for up and down respectively
    """

    num_switches_in_arm = len(arm_1)

    device_states = {}

    states = [seq for seq in itertools.product([0, 1], repeat=num_switches_in_arm)]
    # i.e. [(0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]

    switch_permutations = [combo for combo in itertools.product(states, states)]

    for state in switch_permutations:
        arm_1_state = state[0]
        arm_2_state = state[1]

        OPD = calculate_OPD(arm_1, arm_2, state)

        device_states[OPD] = arm_1_state, arm_2_state

    return device_states

# permute_switches(arm_up, arm_dn)

print(permute_switches(arm_up, arm_dn))
