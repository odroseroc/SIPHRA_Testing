from .d2a_lib import *
from .regs_bit_structure import *

CH_ADDRS = []
SIPHRA_RETURN_SIZE = 15 # bytes. Returned by SIPHRA when D2a.readSIPHRA is called
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
        '''True if the register has a parameter named parameter.'''
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
        return iter(self._registers.values())

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

    def get_reg_value(self, reg_name, chip='A'):
        addr = self._regs[reg_name].addr
        reg_value = self._d2a.readSIPHRA(addr, chip)[SIPHRA_RETURN_SIZE - REG_SIZE:]
        return reg_value

    def read_register(self, reg_name, chip='A'):
        reg_value = self.get_reg_value(reg_name, chip)
        strct = self._regs[reg_name].structure
        parsed_struct = strct.parse(reg_value)
        return parsed_struct

    def _find_reg_containing_param(self, parameter, ch: int=0):
        '''
        Returns the address of the register containing the given parameter.
        :param parameter: Name of the desired parameter.
        :param ch: If the parameter is in one of the 16+1 channel addresses, this argument is used for disambiguation. ``ch`` is a number between 1 and 16 if the parameter belongs to one of the input channels, it is 17 if the parameter belongs to the summing channel and is defaulted to 0 if the parameter belongs to any other register.
        :return: The address of the register containing the given parameter.
        '''
        reg_addr = None
        if not 0 < ch < 17:
            raise ValueError(f"Channel {ch} is out of range. Use channels 1-16 and 17 for summing channel")
        if ch == 0: # Not a channel register
            for reg in self._regs:
                if parameter in reg:
                    reg_addr = reg.addr
        else: # Channel register
            # Verify that the given register exists
            register = self._regs[f"ch{ch}"]
            if parameter in register: reg_addr = register.addr
        if not reg_addr:
            raise NameError(f"Parameter {parameter} does not exist or the register containing it is not implemented.")
        return reg_addr



    def read_param(self, parameter, ch=0, reg_name=None, chip='A'):
        if reg_name:
            reg_addr = self._regs[reg_name].addr
        else:
            reg_addr = self._find_reg_containing_param(parameter, ch)

