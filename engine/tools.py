import engine.debug as c
c.d_log("Module \"tools.py\" as \"tools\" loaded.")


def t_numerate(char: str, addressedChars=None):
    if addressedChars is None:
        addressedChars = list("0123456789ABCDEF")
    return addressedChars.index(char.upper())


def t_hexToRgb(hexCode: str):
    """
    Turns hex-code into RGB
    """
    hexList = list("0123456789ABCDEF")
    r = t_numerate(hexCode[0], hexList) * 16 + t_numerate(hexCode[1], hexList)
    g = t_numerate(hexCode[2], hexList) * 16 + t_numerate(hexCode[3], hexList)
    b = t_numerate(hexCode[4], hexList) * 16 + t_numerate(hexCode[5], hexList)
    return r, g, b


def t_rgbToHex(r: int, g: int, b: int) -> str:
    """
    Turns RGB into hex-code
    """
    return "{:02X}{:02X}{:02X}".format(r, g, b)
