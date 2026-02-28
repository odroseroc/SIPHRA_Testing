from construct import BitStruct, BitsInteger, Padding

# ---------- Bit Structures of SIPHRA registers ----------

# Registers 0x00 - 0x0F: Channel configuration registers
CHANNEL = BitStruct(
    Padding(6),
    'cmis_detector_voffset' / BitsInteger(8),
    'cmis_detector_ioffset' / BitsInteger(3),
    'cmis_impedance_reduction' / BitsInteger(1),
    'cal_select_channel' / BitsInteger(1),
    'qc_threshold' / BitsInteger(8),
    'qc_hysteresis' / BitsInteger(3),
    'pu_channel' / BitsInteger(1),
    'enable_triggering' / BitsInteger(1),
)

# Register 0x10: Summing channel configuration registers
SUMM_CHANNEL = BitStruct(
    Padding(18),
    'cal_select_channel' / BitsInteger(1),
    'qc_threshold' / BitsInteger(8),
    'qc_hysteresis' / BitsInteger(3),
    'pu_channel' / BitsInteger(1),
    'enable_triggering' / BitsInteger(1),
)

# Register 0x11: Configuration register - channel_config
CHANNEL_CONFIG = BitStruct(
    Padding(8),
    'cmis_gain' / BitsInteger(4),
    'ci_gain' / BitsInteger(2),
    'ci_compmode' / BitsInteger(1),
    'shaper_bias' / BitsInteger(4),
    'shaper_feedback_cap' / BitsInteger(4),
    'shaper_feedback_res' / BitsInteger(3),
    'shaper_hold_cap' / BitsInteger(3),
    'shaper_input_cap' / BitsInteger(4),
)

# Register 0x12: Configuration register - channel_control