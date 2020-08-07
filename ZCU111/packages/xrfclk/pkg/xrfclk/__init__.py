"""
Driver to configure RF reference clocks for the ZCU111.

For simple (safe) use, refer to get_freq_list() and set_all_ref_clks().

Expert use:
If you need to specify custom clock frequencies AND you know what you're doing(!)
call _write_lmk04208_regs() and _write_lmx2594_regs() with custom register values.

See this forum post for information on how to generate custom register values...
https://forums.xilinx.com/t5/Evaluation-Boards/How-to-setup-ZCU111-RFSoC-DAC-clock/td-p/896221
"""
import cffi
import os

# global variables
board = os.environ['BOARD']

_ffi = cffi.FFI()
_ffi.cdef("int clearInt(int IicNum);"
          "int writeLmx2594Regs(int IicNum, unsigned int RegVals[113]);"
          "int writeLmk04208Regs(int IicNum, unsigned int RegVals[26]);"
          "int writeLmk04832Regs(int IicNum, unsigned int RegVals[125]);")

_lib = _ffi.dlopen(os.path.join(os.path.dirname(__file__), 'libxrfclk.so'))

if board=="ZCU111":
    _iic_channel = 12
elif board=="XUPRFSOC":
    _iic_channel = 8
else:
    raise ValueError("Board {} is not supported.".format(board))

    
def _safe_wrapper(name, *args, **kwargs):
    """Wrapper function for FFI function calls a la xrfdc.py
    """
    if not hasattr(_lib, name):
        raise RuntimeError(f"Function {name} not in library")
    if getattr(_lib, name)(*args, **kwargs):
        raise RuntimeError(f"Function {name} call failed")
        
def _clear_int():
    _safe_wrapper("clearInt", _iic_channel)

def _write_lmk04208_regs(reg_vals):
    """Write values to the LMK04208 registers.
    This is an internal function --- here be dragons.

    reg_vals: list of 26 32bit register values
    """
    _safe_wrapper("writeLmk04208Regs", _iic_channel, reg_vals)

def _write_Lmk04832Regs_regs(reg_vals):
    """Write values to the LMK04208 registers.
    This is an internal function --- here be dragons.

    reg_vals: list of 26 32bit register values
    """
    _safe_wrapper("writeLmk04832Regs", _iic_channel, reg_vals)

def _write_lmx2594_regs(reg_vals):
    """Write values to the LMX2594 registers.
    This is an internal function --- here be dragons.

    reg_vals: list of 113 32bit register values
    """
    _safe_wrapper("writeLmx2594Regs", _iic_channel, reg_vals)


def get_freq_list():
    """Return a list of supported reference clock frequencies in MHz.
    """
    return _lmx2594Config.keys()


def set_all_ref_clks(freq):
    """Set all RF data converter tile reference clocks to a given frequency.

    freq: Target frequency, as selected from `get_freq_list()`.
    """
    if not freq in _lmx2594Config:
        raise RuntimeError(f"Frequency of {freq} MHz is not an option. "
                           "Please see available options in "
                           "getFreqList()")
    else:
        if board=="ZCU111":
            _safe_wrapper("writeLmk04208Regs", _iic_channel, _lmk04208Config[122.88])
            _safe_wrapper("writeLmx2594Regs", _iic_channel, _lmx2594Config[freq])
        elif board=="XUPRFSOC":
            _safe_wrapper("writeLmk04832Regs", _iic_channel, _lmk04832Config[122.88])
            _safe_wrapper("writeLmx2594Regs", _iic_channel, _lmx2594Config[freq])

_lmx2594Config = {
    102.4: [
        0x700000, 0x6F0000, 0x6E0000, 0x6D0000, 0x6C0000, 0x6B0000, 0x6A0000, 0x690021,
        0x680000, 0x670000, 0x663F80, 0x650011, 0x640000, 0x630000, 0x620200, 0x610888,
        0x600000, 0x5F0000, 0x5E0000, 0x5D0000, 0x5C0000, 0x5B0000, 0x5A0000, 0x590000,
        0x580000, 0x570000, 0x560000, 0x55D300, 0x540001, 0x530000, 0x521E00, 0x510000,
        0x506666, 0x4F0026, 0x4E0003, 0x4D0000, 0x4C000C, 0x4B0AC0, 0x4A0000, 0x49003F,
        0x480001, 0x470081, 0x46C350, 0x450000, 0x4403E8, 0x430000, 0x4201F4, 0x410000,
        0x401388, 0x3F0000, 0x3E0322, 0x3D00A8, 0x3C0000, 0x3B0001, 0x3A8001, 0x390020,
        0x380000, 0x370000, 0x360000, 0x350000, 0x340820, 0x330080, 0x320000, 0x314180,
        0x300300, 0x2F0300, 0x2E07FC, 0x2DC0CC, 0x2C0C23, 0x2B0000, 0x2A0000, 0x290000,
        0x280000, 0x270001, 0x260000, 0x250304, 0x240050, 0x230004, 0x220000, 0x211E21,
        0x200393, 0x1F43EC, 0x1E318C, 0x1D318C, 0x1C0488, 0x1B0002, 0x1A0DB0, 0x190624,
        0x18071A, 0x17007C, 0x160001, 0x150401, 0x14E048, 0x1327B7, 0x120064, 0x11012C,
        0x100080, 0x0F064F, 0x0E1E70, 0x0D4000, 0x0C5001, 0x0B0018, 0x0A10D8, 0x090604,
        0x082000, 0x0740B2, 0x06C802, 0x0500C8, 0x040A43, 0x030642, 0x020500, 0x010808,
        0x00249C
    ],
    204.8: [
        0x700000, 0x6F0000, 0x6E0000, 0x6D0000, 0x6C0000, 0x6B0000, 0x6A0000, 0x690021,
        0x680000, 0x670000, 0x663F80, 0x650011, 0x640000, 0x630000, 0x620200, 0x610888,
        0x600000, 0x5F0000, 0x5E0000, 0x5D0000, 0x5C0000, 0x5B0000, 0x5A0000, 0x590000,
        0x580000, 0x570000, 0x560000, 0x55D300, 0x540001, 0x530000, 0x521E00, 0x510000,
        0x506666, 0x4F0026, 0x4E0003, 0x4D0000, 0x4C000C, 0x4B0A00, 0x4A0000, 0x49003F,
        0x480001, 0x470081, 0x46C350, 0x450000, 0x4403E8, 0x430000, 0x4201F4, 0x410000,
        0x401388, 0x3F0000, 0x3E0322, 0x3D00A8, 0x3C0000, 0x3B0001, 0x3A8001, 0x390020,
        0x380000, 0x370000, 0x360000, 0x350000, 0x340820, 0x330080, 0x320000, 0x314180,
        0x300300, 0x2F0300, 0x2E07FC, 0x2DC0CC, 0x2C0C23, 0x2B0000, 0x2A0000, 0x290000,
        0x280000, 0x270001, 0x260000, 0x250304, 0x240050, 0x230004, 0x220000, 0x211E21,
        0x200393, 0x1F43EC, 0x1E318C, 0x1D318C, 0x1C0488, 0x1B0002, 0x1A0DB0, 0x190624,
        0x18071A, 0x17007C, 0x160001, 0x150401, 0x14E048, 0x1327B7, 0x120064, 0x11012C,
        0x100080, 0x0F064F, 0x0E1E70, 0x0D4000, 0x0C5001, 0x0B0018, 0x0A10D8, 0x090604,
        0x082000, 0x0740B2, 0x06C802, 0x0500C8, 0x040A43, 0x030642, 0x020500, 0x010808,
        0x00249C
    ],
    409.6: [
        0x700000, 0x6F0000, 0x6E0000, 0x6D0000, 0x6C0000, 0x6B0000, 0x6A0000, 0x690021,
        0x680000, 0x670000, 0x663F80, 0x650011, 0x640000, 0x630000, 0x620200, 0x610888,
        0x600000, 0x5F0000, 0x5E0000, 0x5D0000, 0x5C0000, 0x5B0000, 0x5A0000, 0x590000,
        0x580000, 0x570000, 0x560000, 0x55D300, 0x540001, 0x530000, 0x521E00, 0x510000,
        0x506666, 0x4F0026, 0x4E0003, 0x4D0000, 0x4C000C, 0x4B0980, 0x4A0000, 0x49003F,
        0x480001, 0x470081, 0x46C350, 0x450000, 0x4403E8, 0x430000, 0x4201F4, 0x410000,
        0x401388, 0x3F0000, 0x3E0322, 0x3D00A8, 0x3C0000, 0x3B0001, 0x3A8001, 0x390020,
        0x380000, 0x370000, 0x360000, 0x350000, 0x340820, 0x330080, 0x320000, 0x314180,
        0x300300, 0x2F0300, 0x2E07FC, 0x2DC0CC, 0x2C0C23, 0x2B0000, 0x2A0000, 0x290000,
        0x280000, 0x270001, 0x260000, 0x250304, 0x240050, 0x230004, 0x220000, 0x211E21,
        0x200393, 0x1F43EC, 0x1E318C, 0x1D318C, 0x1C0488, 0x1B0002, 0x1A0DB0, 0x190624,
        0x18071A, 0x17007C, 0x160001, 0x150401, 0x14E048, 0x1327B7, 0x120064, 0x11012C,
        0x100080, 0x0F064F, 0x0E1E70, 0x0D4000, 0x0C5001, 0x0B0018, 0x0A10D8, 0x090604,
        0x082000, 0x0740B2, 0x06C802, 0x0500C8, 0x040A43, 0x030642, 0x020500, 0x010808,
        0x00249C
    ],
    737: [
        0x700000, 0x6F0000, 0x6E0000, 0x6D0000, 0x6C0000, 0x6B0000, 0x6A0000, 0x690021,
        0x680000, 0x670000, 0x663F80, 0x650011, 0x640000, 0x630000, 0x620200, 0x610888,
        0x600000, 0x5F0000, 0x5E0000, 0x5D0000, 0x5C0000, 0x5B0000, 0x5A0000, 0x590000,
        0x580000, 0x570000, 0x560000, 0x55D300, 0x540001, 0x530000, 0x521E00, 0x510000,
        0x506666, 0x4F0026, 0x4E0003, 0x4D0000, 0x4C000C, 0x4B0900, 0x4A0000, 0x49003F,
        0x480001, 0x470081, 0x46C350, 0x450000, 0x4403E8, 0x430000, 0x4201F4, 0x410000,
        0x401388, 0x3F0000, 0x3E0322, 0x3D00A8, 0x3C0000, 0x3B0001, 0x3A8001, 0x390020,
        0x380000, 0x370000, 0x360000, 0x350000, 0x340820, 0x330080, 0x320000, 0x314180,
        0x300300, 0x2F0300, 0x2E07FC, 0x2DC0CC, 0x2C0C23, 0x2B0000, 0x2A0000, 0x290000,
        0x280000, 0x270001, 0x260000, 0x250304, 0x240048, 0x230004, 0x220000, 0x211E21,
        0x200393, 0x1F43EC, 0x1E318C, 0x1D318C, 0x1C0488, 0x1B0002, 0x1A0DB0, 0x190624,
        0x18071A, 0x17007C, 0x160001, 0x150401, 0x14E048, 0x1327B7, 0x120064, 0x11012C,
        0x100080, 0x0F064F, 0x0E1E70, 0x0D4000, 0x0C5001, 0x0B0018, 0x0A10D8, 0x090604,
        0x082000, 0x0740B2, 0x06C802, 0x0500C8, 0x040A43, 0x030642, 0x020500, 0x010808,
        0x00249C
    ]
}

_lmk04208Config = {
    122.88: [
        0x00160040, 0x00143200, 0x00143201, 0x00140322,
        0xC0140023, 0x40140024, 0x80141E05, 0x01100006,
        0x01100007, 0x06010008, 0x55555549, 0x9102410A,
        0x0401100B, 0x1B0C006C, 0x2302886D, 0x0200000E,
        0x8000800F, 0xC1550410, 0x00000058, 0x02C9C419,
        0x8FA8001A, 0x10001E1B, 0x0021201C, 0x0180033D,
        0x0200033E, 0x003F001F
    ]
}

_lmk04832Config = {         
    122.88: [
          0x000090, 0x000010, 0x000200, 0x000306, 0x0004D1, 0x000563, 0x000650, 0x000C51,
          0x000D04, 0x010090, 0x01010A, 0x010201, 0x010340, 0x010410, 0x010512, 0x010604,
          0x010710, 0x010890, 0x01090A, 0x010A01, 0x010B40, 0x010C10, 0x010D12, 0x010E04,
          0x010F01, 0x011008, 0x01110A, 0x011280, 0x011350, 0x011410, 0x011512, 0x011604,
          0x011700, 0x011819, 0x01190A, 0x011A80, 0x011B50, 0x011C10, 0x011D12, 0x011E04,
          0x011F33, 0x012019, 0x01210A, 0x012200, 0x012340, 0x012410, 0x012512, 0x012604,
          0x012701, 0x012819, 0x01290A, 0x012A00, 0x012B40, 0x012C10, 0x012D12, 0x012E04,
          0x012F11, 0x013002, 0x01310A, 0x013280, 0x013350, 0x013410, 0x013512, 0x013604,
          0x013700, 0x013801, 0x013900, 0x013A0C, 0x013B00, 0x013C00, 0x013D08, 0x013E03,
          0x013F00, 0x01400F, 0x014100, 0x014200, 0x014311, 0x014400, 0x014500, 0x014618,
          0x01470A, 0x014803, 0x014943, 0x014A03, 0x014B06, 0x014C00, 0x014D00, 0x014EC0, 
          0x014F7F, 0x015001, 0x015102, 0x015200, 0x015300, 0x015478, 0x015500, 0x015678,
          0x015700, 0x015896, 0x015904, 0x015AB0, 0x015BD4, 0x015C20, 0x015D00, 0x015E1E,
          0x015F3B, 0x016000, 0x016102, 0x01624C, 0x016300, 0x016400, 0x016519, 0x016958,
          0x016A20, 0x016B00, 0x016C00, 0x016D00, 0x016E04, 0x017310, 0x017700, 0x018200,
          0x018300, 0x016600, 0x016700, 0x016819, 0x055500
    ]
}
