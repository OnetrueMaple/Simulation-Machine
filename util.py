acceptable_units = {
                            "metric"     : {
                                            "Q"      : 10**30,   # Quetta
                                            "Quetta" : 10**30,   # Quetta
                                            "R"      : 10**27,   # Ronna
                                            "Ronna"  : 10**27,   # Ronna
                                            "Y"      : 10**24,   # Yotta
                                            "Yotta"  : 10**24,   # Yotta
                                            "Z"      : 10**21,   # Zetta
                                            "Zetta"  : 10**21,   # Zetta
                                            "E"      : 10**18,   # Exo
                                            "Exo"    : 10**18,   # Exo
                                            "P"      : 10**15,   # Peta
                                            "Peta"   : 10**15,   # Peta
                                            "T"      : 10**12,   # Tera
                                            "Tera"   : 10**12,   # Tera
                                            "G"      : 10**9,    # Giga
                                            "Giga"   : 10**9,    # Giga
                                            "M"      : 10**6,    # Mega
                                            "Mega"   : 10**6,    # Mega
                                            "k"      : 10**3,    # Kilo
                                            "kilo"   : 10**3,    # Kilo
                                            "h"      : 10**2,    # Hecto
                                            "hecto"  : 10**2,    # Hecto
                                            "da"     : 10**1,    # Deca
                                            "deca"   : 10**1,    # Deca
                                            #""  : 1,       # Base Unit.
                                            "d"      : 10**-1,   # Deci
                                            "deci"   : 10**-1,   # Deci
                                            "c"      : 10**-2,   # Centi
                                            "centi"  : 10**-2,   # Centi
                                            "m"      : 10**-3,   # Milli
                                            "milli"  : 10**-3,   # Milli
                                            "u"      : 10**-6,   # Micro
                                            "micro"  : 10**-6,   # Micro
                                            "n"      : 10**-9,   # Nano
                                            "nano"   : 10**-9,   # Nano
                                            "p"      : 10**-12,  # Pico
                                            "pico"   : 10**-12,  # Pico
                                            "f"      : 10**-15,  # Femto
                                            "femto"  : 10**-15,  # Femto
                                            "a"      : 10**-18,  # Atto
                                            "atto"   : 10**-18,  # Atto
                                            "z"      : 10**-21,  # Zepto
                                            "zepto"  : 10**-21,  # Zepto
                                            "y"      : 10**-24,  # Yocto
                                            "yocto"  : 10**-24,  # Yocto
                                            "r"      : 10**-27,  # Ronto
                                            "ronto"  : 10**-27,  # Ronto
                                            "q"      : 10**-30,  # Quecto
                                            "quecto" : 10**-30   # Quecto
                                           },
                            "units"      : {
                                            "s"       : 1,        # Seconds, a real-life second
                                            "second"  : 1,
                                            "t"       : 1,        # Ticks, a single program runtime loop.
                                            "tick"    : 1,
                                            "fr"      : 1,        # Frames, effectively ticks
                                            "frame"   : 1,
                                            "mi"      : 60,         # Minute    =   60 seconds
                                            "minute"  : 60,         # Minute    =   60 seconds
                                            "hr"      : 360,        # Hour      =   60 minutes
                                            "hour"    : 360,
                                            "dy"      : 8640,       # Day       =   24   hours
                                            "day"     : 8640,
                                            "wk"      : 60480,      # Week      =    7    days
                                            "week"    : 60480,
                                            "yr"      : 3153600,    # Year      =  365    days
                                            "year"    : 3153600
                                           }
                       }
'''
tempstr = "Colors: "
for i in COLORS:
    tempstr += f"{COLORS[i]}{i}{COLORS[-1]}, "
print(tempstr)
'''
COLORS = {
            -1: "\033[0m",  # RESET
            0 : "\033[90m", # BLACK
            1 : "\033[91m", # RED
            2 : "\033[92m", # GREEN
            3 : "\033[93m", # BLUE
            4 : "\033[94m", # YELLOW
            5 : "\033[95m", # PURPLE
            6 : "\033[96m", # CYAN
            7 : "\033[97m"  # WHITE
         }

def random(bound):
    if(bound <= 0): # The below code isn't capable of generating a negative number, so...
        return 0    #    I will bypass that by explicitly making a blanket case skip random number generation entirely if the boundary is negative or 0.
    urandom    = open("/dev/urandom", "rb")   # Linux OS's CSPRNG. Layman's terms: Well supported and thoroughly vetted pseudo-random number generator.
    binbound   = int(len(bin(bound)[2:]))     # How many bits I should keep inside candidate at a time.
    source     = ""                           # Stores data read from urandom.
    candidate  = bound + 1                    # Candidate number to return.
    while(candidate > bound):                 # While the candidate number is above the passed bound...
        if(len(source) < binbound):                                              # If the source doesn't have enough bits to refill candidate...
            source += f"{bin(list(urandom.read(int(binbound / 8) + 1))[0])[2:]}" # Pull all the necessary bytes plus a few extra for producing a number within the passed 'bound'.
        candidate = int(f"{source[0:binbound]}", 2)# Fill up the candidate with bytes read from urandom
        source = source[binbound:]                 # Remove the bits I just added to candidate from source.
    urandom.close() # Close the file I'm reading "random" bits from
    return candidate# Return the final number.