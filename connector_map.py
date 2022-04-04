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

    south = chip_pin_out.eq_pin_map
    north = chip_pin_out.highres_pin_map

    eq_connector_map = {
        south[2]:  J7[1 - 1],  # J7, 1
        south[3]:  J7[2 - 1],  # J7, 2
        south[4]:  J7[3 - 1],  # J7, 3
        south[5]:  J7[4 - 1],  # J7, 4
        south[6]:  J7[5 - 1],  # J7, 5
        south[7]:  J7[6 - 1],  # J7, 6
        south[8]:  J7[7 - 1],  # J7, 7
        south[9]:  J7[8 - 1],  # J7, 8
        south[10]: J7[9 - 1],  # J7, 9
        south[11]: J7[10 - 1], # J7, 10
        south[12]: J7[11 - 1], # J7, 11
        south[13]: J7[12 - 1], # J7, 12
        south[14]: J7[13 - 1], # J7, 13
        south[15]: J7[14 - 1], # J7, 14
        south[16]: J7[15 - 1], # J7, 15
        south[17]: J7[16 - 1], # J7, 16
        south[18]: J7[17 - 1], # J7, 17
        south[19]: J7[18 - 1], # J7, 18
        south[20]: J7[19 - 1], # J7, 19
        south[21]: J7[20 - 1], # J7, 20
        south[22]: J8[1 - 1],  # J8, 1
        south[23]: J8[2 - 1],  # J8, 2
        south[24]: J8[3 - 1],  # J8, 3
        south[25]: J8[4 - 1],  # J8, 4
        south[26]: J8[5 - 1],  # J8, 5
        south[27]: J8[6 - 1],  # J8, 6
    }

    highres_connector_map = {
        north[28]: J3[4 - 1],   # J3, 4
        north[29]: J3[5 - 1],   # J3, 5
        north[30]: J3[6 - 1],   # J3, 6
        north[31]: J3[7 - 1],   # J3, 7
        north[32]: J3[8 - 1],   # J3, 8
        north[33]: J3[9 - 1],   # J3, 9
        north[34]: J3[10 - 1],  # J3, 10
        north[35]: J3[11 - 1],  # J3, 11
        north[36]: J3[12 - 1],  # J3, 12
        north[37]: J3[13 - 1],  # J3, 13
        north[38]: J3[14 - 1],  # J3, 14
        north[39]: J3[15 - 1],  # J3, 15
        north[40]: J3[16 - 1],  # J3, 16
        north[41]: J3[17 - 1],  # J3, 17
        north[42]: J3[18 - 1],  # J3, 18
        north[43]: J3[19 - 1],  # J3, 19
        north[44]: J3[20 - 1],  # J3, 20
        north[45]: J4[1 - 1],   # J4, 1
        north[46]: J4[2 - 1],   # J4, 2
        north[47]: J4[3 - 1],   # J4, 3
        north[48]: J4[4 - 1],   # J4, 4
        north[49]: J4[5 - 1],   # J4, 5
        north[50]: J4[6 - 1],   # J4, 6
        north[51]: J4[7 - 1],   # J4, 7
        north[52]: J4[8 - 1],   # J4, 8
        north[53]: J4[9 - 1],   # J4, 9
        north[54]: J4[10 - 1],  # J4, 10
        north[55]: J4[11 - 1],  # J4, 11
        north[56]: J4[12 - 1],  # J4, 12
        north[57]: J4[13 - 1],  # J4, 13
        north[58]: J4[14 - 1],  # J4, 14
        north[59]: J4[15 - 1],  # J4, 15
        north[60]: J4[16 - 1],  # J4, 16
        north[61]: J4[17 - 1],  # J4, 17
        north[62]: J4[18 - 1],  # J4, 18
        north[63]: J4[19 - 1],  # J4, 19
    }

@dataclass:
class chip_pin_out:
    # South Connector map of Pin Number: On-chip Device
    eq_pin_map = {
        2: 'FA_A',
        3: 'FA_B',
        4: 'HTR_D1_B',
        5: 'HTR_D1_A',
        6: 'HTR_U1_B',
        7: 'HTR_U1_A',
        8: 'HTR_D2_B',
        9: 'HTR_D2_A',
        10: 'HTR_U2_B',
        11: 'HTR_U2_A',
        12: 'HTR_D3_B',
        13: 'HTR_D3_A',
        14: 'HTR_U3_B',
        15: 'HTR_U3_A',
        16: 'HTR_D4_B',
        17: 'HTR_D4_A',
        18: 'HTR_U4_B',
        19: 'HTR_U4_A',
        20: 'HTR_D5_B',
        21: 'HTR_D5_A',
        22: 'HTR_U5_B',
        23: 'HTR_U5_A',
        24: 'HTR_AB_D_B',
        25: 'HTR_AB_D_A',
        26: 'HTR_AB_U_B',
        27: 'HTR_AB_U_A',
    }

    # North Connector map of Pin Number: On-chip Device
    highres_pin_map = {
        28: 'HR_TAP_DOWN_PD_SHIELD',
        29: 'HR_TAP_DOWN_PD_SIGNAL',
        30: 'HR_OUTPUT_PD_SHIELD',
        31: 'HR_OUTPUT_PD_SIGNAL',
        32: 'HR_TAP_UP_PD_SHIELD',
        33: 'HR_TAP_UP_PD_SIGNAL',
        34: 'HR_AB_U_A',
        35: 'HR_AB_U_B',
        36: 'HR_AB_D_A',
        37: 'HR_AB_D_B',
        38: 'HR_HTR_U5_A',
        39: 'HR_HTR_U5_B',
        40: 'HR_HTR_D5_A',
        41: 'HR_HTR_D5_B',
        42: 'HR_MID_TAP_DOWN_PD_SIGNAL',
        43: 'HR_MID_TAP_DOWN_PD_SHIELD',
        44: 'HR_MID_TAP_UP_PD_SIGNAL',
        45: 'HR_MID_TAP_UP_PD_SHIELD',
        46: 'HR_HTR_U4_A',
        47: 'HR_HTR_U4_B',
        48: 'HR_HTR_D4_A',
        49: 'HR_HTR_D4_B',
        50: 'HR_HTR_U3_A',
        51: 'HR_HTR_U3_B',
        52: 'HR_HTR_D3_A',
        53: 'HR_HTR_D3_B',
        54: 'HR_HTR_U2_A',
        55: 'HR_HTR_U2_B',
        56: 'HR_HTR_D2_A',
        57: 'HR_HTR_D2_B',
        58: 'HR_HTR_D1_B',
        59: 'HR_HTR_D1_A',
        60: 'HR_HTR_U1_B',
        61: 'HR_HTR_U1_A',
        62: 'HR_HTR_FA_A',
        63: 'HR_HTR_FA_B',
    }