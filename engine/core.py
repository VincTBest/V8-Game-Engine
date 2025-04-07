# if it works, don't touch it (prime-example)

def d_log(msg, t=0, ext=""):
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
        print(f"[{ext2}]: {msg}")


class c_globalWindow:
    pass
