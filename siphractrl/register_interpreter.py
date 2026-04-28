# ******************************************************************************************
# Description: Contains dicts, lists and functions to convert the values of some of the SIPHRA registers to a human-readable form.
# Written by: Oscar Rosero (KTH)
# ....
#    Date: 04/2026

CMIS_GAIN_VALUES = dict(zip((0,1,3,7),('1/10', '1/100', '1/200', '1/400')))
CI_GAIN_VALUES = ['1V/30pC', '1V/27.75pC', '1V/3pC', '1V/0.75pC'] # List index coincides with the parameter value

def interpret_hold_delay(tune, delay):
    ''' Return the hold_delay in nanoseconds from params tune and hold in reg 0x18'''
    # Constants given in the manual
    A = 0.0748
    B = 1700

    return (1 + A*tune)/(1 + (15 - delay))

