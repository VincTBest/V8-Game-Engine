
def d_log(msg: str, t=0, ext=""):
    """
    Logs a message to the console.
    """
    ext2 = ""
    if ext != "":
        ext2 = f"::{ext}"

    if t == 0:
        print(f"[INFO{ext2}]: {msg}")
    elif t == 1:
        print(f"[WARN{ext2}]: {msg}")
    elif t == 2:
        print(f"[ERROR{ext2}]: {msg}")
    elif t == 3:
        print(f"[C|{ext2}]: {msg}")


d_log("Module \"debug.py\" as \"debug\" loaded.")
