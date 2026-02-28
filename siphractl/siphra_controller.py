from .d2a_lib import *
from .regs_bit_structure import *

CH_ADDRS = []
SIPHRA_RETURN_SIZE = 12 # bytes. Returned by SIPHRA when D2a.readSIPHRA is called
# TODO: Check the size of the packet returned by D2a.readSIPHRA
REG_SIZE = 4 # bytes. Size of the bytearray passed to D2a.writeSIPHRA

# Register map classes

class SIPHRARegister:
    def __init__(self, addr, structure):
        self.addr = addr
        self.structure = structure

    def __getitem__(self, param_name):
        pass


    def __contains__(self, param_name):
        '''True if the register has a parameter named param_name.'''
        params = self.structure.subcon.subcons
        param_names = [param.name for param in params if param.name]
        return param_name in param_names

    def parse(self, value):
        return self.structure.parse(value)

    def set_param(self, param_name, value, reg_current_value):
        old_register = parse(reg_current_value)


class SIPHRARegMap:
    def __init__(self):
        self._registers = {}

        for i in range(1,17):
            self._registers[f"ch{i}"] = SIPHRARegister(i, CHANNEL)

        self._registers["summ"] = SIPHRARegister(0x10, SUMM_CHANNEL)
        self._registers["ch_config"] = SIPHRARegister(0x11, CHANNEL_CONFIG)

    def __getitem__(self, name):
        return self._registers[name]

    def __getattr__(self, name):
        return self._registers[name]

    def __iter__(self):
        return iter(self._registers)

    def __len__(self):
        return len(self._registers)

    def __contains__(self, name):
        return name in self._registers

    def items(self):
        return self._registers.items()

    def keys(self):
        return self._registers.keys()

    def values(self):
        return self._registers.values()


class SIPHRA:
    def __init__(self, d2a: D2a):
        self._d2a = d2a
        self._regs = SIPHRARegMap()

    def get_register(self, chip, reg_name):
        addr, struct = self._regs[reg_name].addr, self._regs[reg_name].structure
        reg_value = self._d2a.readSIPHRA(addr, chip)[SIPHRA_RETURN_SIZE - REG_SIZE:]
        parsedStruct = struct.parse(reg_value)
        return parsedStruct

    def _get_reg_containing_param(self, param, ch: int=0):
        if not 0 < ch < 17:
            raise ValueError(f"Channel {ch} is out of range. Use channels 1-16 and 17 for summing channel")
        if ch > 0:




    def get_param(self, chip, param, reg_name):
        pass

