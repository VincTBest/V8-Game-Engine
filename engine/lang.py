
LANG = "en"
LANG_LIB = {}


def l_addLang(name):
    global LANG_LIB
    LANG_LIB[name] = {}


def l_changeLang(name):
    global LANG
    LANG = name


def l_addKey(name, lang, value):
    global LANG_LIB
    LANG_LIB[lang][name] = value
    print(LANG_LIB)


def l_getKey(name):
    global LANG
    global LANG_LIB
    return LANG_LIB[LANG][name]
