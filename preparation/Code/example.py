try:
    if state:
        setRed(True)
        setGreen(False)
        state = False
    else:
        setRed(False)
        setGreen(True)
        state = True
except:
    state = True
