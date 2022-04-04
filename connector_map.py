"""

"""
from dataclasses import dataclass
from typing import Iterable

@dataclass
class AdapterBoard:
    #J2: Iterable
    J3: Iterable
    J4: Iterable
    #J6: Iterable
    J7: Iterable
    J8: Iterable
    #J9: Iterable
    #J10: Iterable

    eq_heater_pin_map = {
        'FA_A':     J7[1-1],  # J7, 1
        'FA_B':     J7[2-1],  # J7, 2
        'HTR_D1_B': J7[3-1],  # J7, 3
        'HTR_D1_A': J7[4-1],  # J7, 4
        'HTR_U1_B': J7[5-1],  # J7, 5
        'HTR_U1_A': J7[6-1],  # J7, 6
        'HTR_D2_B': J7[7-1],  # J7, 7
        'HTR_D2_A': J7[8-1],  # J7, 8
        'HTR_U2_B': J7[9-1],  # J7, 9
        'HTR_U2_A': J7[10-1],  # J7, 10
        'HTR_D3_B': J7[11-1],  # J7, 11
        'HTR_D3_A': J7[12-1],  # J7, 12
        'HTR_U3_B': J7[13-1],  # J7, 13
        'HTR_U3_A': J7[14-1],  # J7, 14
        'HTR_D4_B': J7[15-1],  # J7, 15
        'HTR_D4_A': J7[16-1],  # J7, 16
        'HTR_U4_B': J7[17-1],  # J7, 17
        'HTR_U4_A': J7[18-1],  # J7, 18
        'HTR_D5_B': J7[19-1],  # J7, 19
        'HTR_D5_A': J7[20-1],  # J7, 20
        'HTR_U5_B': J8[1-1],   # J8, 1
        'HTR_U5_A': J8[2-1],   # J8, 2
        'HTR_AB_D_B': J8[3-1],  # J8, 3
        'HTR_AB_D_A': J8[4-1],  # J8, 4
        'HTR_AB_U_B': J8[5-1],  # J8, 5
        'HTR_AB_U_A': J8[6-1],  # J8, 6
    }

    highres_connection_map = {
        'HR_TAP_DOWN_PD_SHIELD': J3[9-1],  # J3, 4
        'HR_TAP_DOWN_PD_SIGNAL': J3[10-1],  # J3, 5
        'HR_OUTPUT_PD_SHIELDL':  J3[11-1],  # J3, 6
        'HR_OUTPUT_PD_SIGNAL':   J3[12-1],  # J3, 7
        'HR_TAP_UP_PD_SHIELD':   J3[9-1],  # J3, 8
        'HR_TAP_UP_PD_SIGNAL':   J3[10-1],  # J3, 9
        'HR_AB_U_A':   J3[10-1],  # J3, 10
        'HR_AB_U_B':   J3[11-1],  # J3, 11
        'HR_AB_D_A':   J3[12-1],  # J3, 12
        'HR_AB_D_B':   J3[13-1],  # J3, 13
        'HR_HTR_U5_A': J3[14-1],  # J3, 14
        'HR_HTR_U5_B': J3[15-1],  # J3, 15
        'HR_HTR_D5_A': J3[16-1],  # J3, 16
        'HR_HTR_D5_B': J3[17-1],  # J3, 17
        'HR_MID_TAP_DOWN_PD_SIGNAL': J3[18-1],  # J3, 18
        'HR_MID_TAP_DOWN_PD_SHIELD': J3[19-1],  # J3, 19
        'HR_MID_TAP_UP_PD_SIGNAL':   J3[20-1],  # J3, 20
        'HR_MID_TAP_UP_PD_SHIELD':   J4[1-1],  # J4, 1
        'HR_HTR_U4_A':   J4[2-1],  # J4, 2
        'HR_HTR_U4_B':   J4[3-1], # J4, 3
        'HR_HTR_D4_A':   J4[4-1], # J4, 4
        'HR_HTR_D4_B':   J4[5-1], # J4, 5
        'HR_HTR_U3_A':   J4[6-1], # J4, 6
        'HR_HTR_U3_B':   J4[7-1], # J4, 7
        'HR_HTR_D3_A':   J4[8-1], # J4, 8
        'HR_HTR_D3_B':   J4[9-1], # J4, 9
        'HR_HTR_U2_A':   J4[10-1],  # J4, 10
        'HR_HTR_U2_B':   J4[11-1],  # J4, 11
        'HR_HTR_D2_A':   J4[12-1],  # J4, 12
        'HR_HTR_D2_B':   J4[13-1],  # J4, 13
        'HR_HTR_D1_B':   J4[14-1],  # J4, 14
        'HR_HTR_D1_A':   J4[15-1],  # J4, 15
        'HR_HTR_U1_B':   J4[16-1],  # J4, 16
        'HR_HTR_U1_A':   J4[17-1],  # J4, 17
        'HR_HTR_FA_A':   J4[18-1],  # J4, 18
        'HR_HTR_FA_B':   J4[19-1],  # J4, 19
    }
