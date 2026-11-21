import threading
from util import COLORS
# This is a "universe" where things happen. One instance should be sufficient to run the sim, while
# also being able to support other instances of itself.

''' I will use this as the state machine. The renderer displays the universe to the user. '''
'''
| Function    | Question it answers                                       | Status         | What's Responsible     |
| ----------- | --------------------------------------------------------- | -------------- | ---------------------- |
| Time        | Who decides how far the simulation advances?              | ✔ Solved!      | Universe               |
| State       | Which version of the world does a rule observe?           | ? Unresolved   | ?????????????????????? |
| Interaction | How does a rule communicate a proposed change?            | ? Unresolved   | ?????????????????????? |
| Conflict    | What happens when two rules make incompatible proposals?  | ? Unresolved   | ?????????????????????? |
| Ordering    | When do changes become visible to other rules?            | ? Unresolved   | ?????????????????????? |
| Structure   | When can objects be created, destroyed, or replaced?      | ? Unresolved   | ?????????????????????? |
| Determinism | What guarantees reproducibility?                          | 𐄂 Known Issues | ?????????????????????? |
'''
# TODO Please address the poor documentation on these functions, it's hard enough sorting through these concepts, let alone validating the behavior.

class Universe:

    # The Universe needs to concern itself with time. I'll provide metric modifiers, but all other units represent measurements of time.
    acceptable_units = {
                            "metric"     : {
                                            'Q'      : 10**30,   # Quetta
                                            'Quetta' : 10**30,   # Quetta
                                            'R'      : 10**27,   # Ronna
                                            'Ronna'  : 10**27,   # Ronna
                                            'Y'      : 10**24,   # Yotta
                                            'Yotta'  : 10**24,   # Yotta
                                            'Z'      : 10**21,   # Zetta
                                            'Zetta'  : 10**21,   # Zetta
                                            'E'      : 10**18,   # Exo
                                            'Exo'    : 10**18,   # Exo
                                            'P'      : 10**15,   # Peta
                                            'Peta'   : 10**15,   # Peta
                                            'T'      : 10**12,   # Tera
                                            'Tera'   : 10**12,   # Tera
                                            'G'      : 10**9,    # Giga
                                            'Giga'   : 10**9,    # Giga
                                            'M'      : 10**6,    # Mega
                                            'Mega'   : 10**6,    # Mega
                                            'k'      : 10**3,    # Kilo
                                            'kilo'   : 10**3,    # Kilo
                                            'h'      : 10**2,    # Hecto
                                            'hecto'  : 10**2,    # Hecto
                                            'da'     : 10**1,    # Deca
                                            'deca'   : 10**1,    # Deca
                                            ''  : 1,       # Base Unit.
                                            'd'      : 10**-1,   # Deci
                                            'deci'   : 10**-1,   # Deci
                                            'c'      : 10**-2,   # Centi
                                            'centi'  : 10**-2,   # Centi
                                            'm'      : 10**-3,   # Milli
                                            'milli'  : 10**-3,   # Milli
                                            'u'      : 10**-6,   # Micro
                                            'micro'  : 10**-6,   # Micro
                                            'n'      : 10**-9,   # Nano
                                            'nano'   : 10**-9,   # Nano
                                            'p'      : 10**-12,  # Pico
                                            'pico'   : 10**-12,  # Pico
                                            'f'      : 10**-15,  # Femto
                                            'femto'  : 10**-15,  # Femto
                                            'a'      : 10**-18,  # Atto
                                            'atto'   : 10**-18,  # Atto
                                            'z'      : 10**-21,  # Zepto
                                            'zepto'  : 10**-21,  # Zepto
                                            'y'      : 10**-24,  # Yocto
                                            'yocto'  : 10**-24,  # Yocto
                                            'r'      : 10**-27,  # Ronto
                                            'ronto'  : 10**-27,  # Ronto
                                            'q'      : 10**-30,  # Quecto
                                            'quecto' : 10**-30   # Quecto
                                           },
                            "units"      : {
                                            's'       : 1,        # Seconds, a real-life second
                                            'second'  : 1,
                                            't'       : 1,        # Ticks, a single program runtime loop.
                                            'tick'    : 1,
                                            'fr'      : 1,        # Frames, effectively ticks
                                            'frame'   : 1,
                                            'mi'      : 60,         # Minute    =   60 seconds
                                            'minute'  : 60,         # Minute    =   60 seconds
                                            'hr'      : 360,        # Hour      =   60 minutes
                                            'hour'    : 360,
                                            'dy'      : 8640,       # Day       =   24   hours
                                            'day'     : 8640,
                                            'wk'      : 60480,      # Week      =    7    days
                                            'week'    : 60480,
                                            'yr'      : 3153600,    # Year      =  365    days
                                            'year'    : 3153600
                                           }
                       }

    def __init__(self, ID=None, simulation_speed=[30, "fps"]):

        # This is such a headache to think through. Maybe I'll come back to this at some point.
        self.disallow_negative_time = True

        # Reference id. Can be whatever, idrc it's your responsibility to sort through this stuff.
        self.id = ID

        # How far should the engine advance time relative to the real world? Some simulations, like physics applications, require time steps not ticks.
        self.simulation_speed = None
        self.set_simulation_speed(simulation_speed)

        # Simplified form of simulation_speed. I need to reduce whatever sim_speed is down to 'x_sub(t) / t' or 'x_sub(s) / s'.
        self.timestep = self.calculate_timestep()

        # This is the list of "objects" in your universe. Think planets, cats, anything.
        # Each object MUST have a "tick" function, even if the function does nothing, or else it will break the universe.
        self.objects = []

    def tick(self): # Simulate time for all objects. Frame generation, physical world updates, ect.

        if(self.simulation_speed == [1, "t/t"]):
            for object in self.objects:
                object.tick()
        elif(self.simulation_speed == [1, "s/s"]):
            for object in self.objects:
                object.tick()
        else:       # Code stub, doesn't actually respect the rate of change set inside self.timestep
            for object in self.objects:
                object.tick()

    def addObject(self, object):
        self.objects.append(object)

    def removeObject(self, object):
        self.objects.remove(object)

    def set_simulation_speed(self, sim_speed):
        valid    = self.validate_units(sim_speed, print_warnings=False)
        temp_str = f"{'\033[94m'}The passed value {'\033[95m'}\'{sim_speed}\'{'\033[94m'} returned "
        if(valid):
            temp_str += f"{'\033[92m'}\'{valid}\'{'\033[94m'}!\n{'\033[0m'}"
            self.simulation_speed = sim_speed
            self.timestep         = self.calculate_timestep()
            #print(f"timestep={self.timestep}")
        else:
            temp_str += f"{'\033[91m'}\'{valid}\'{'\033[94m'}!\n{'\033[0m'}"
        print(temp_str)

    # I need this to know how far to advance per runtime cycle, or tick. Real-time physics can be achieved by waiting to tick on specific intervals, I'm calculating that interval here.
    def calculate_timestep(self):
        # I deleted a check for a valid self.simulation_speed since this should only be called by self.set_simulation_speed(). That function verifies the parameters already.

        # I'm defining a simplify function since I need to simplify the time_units and metric_prefixes to one stable number for each "final" unit set.
        def simplify(sim_speed):
            measurement = sim_speed[1].split("/")
            prefixes    = [self.get_metric_prefix(measurement[0]), self.get_metric_prefix(measurement[1])]
            units       = [self.get_time_unit(measurement[0]), self.get_time_unit(measurement[1])]

            # Converting any metric prefixes and higher-value measurements into fundamental units: seconds and ticks
            # Numerator values first...
            simplified   = self.acceptable_units["metric"][self.get_metric_prefix(measurement[0])] * sim_speed[0]
            #print(f"simulation_speed * metric_prefix = {simplified}")
            simplified  *= self.acceptable_units["units"][self.get_time_unit(measurement[0])]
            #print(f"value * time_multiple = {simplified}")
            # Denomenator values next...
            simplified /= self.acceptable_units["metric"][self.get_metric_prefix(measurement[1])]
            #print(f"value / metric_prefix = {simplified}")
            simplified /= self.acceptable_units["units"][self.get_time_unit(measurement[1])]
            #print(f"value / time_multiple = {simplified}")

            return simplified

        # I need to handle infinity first. I'll interpret that as "as fast as possible" since infinite speed doesn't make sense otherwise.
        if(str(self.simulation_speed[0]) == "inf"):
            if(self.simulation_speed[1] == "fps"): # Since fps basically means 't/s', I can turn the seconds to ticks to not be bound by the real-time clock.
                return [1, "t/t"]
            else:                                  # Infinite rate of change with arbitrary units makes less sense. Why include a larger/smaller time scale but declare infinite speed? Surely there's a reason...
                simple_speed = simplify(self.simulation_speed)
                #print(f"simple_speed={simple_speed}")


        if(self.simulation_speed[1] == "fps"): # I need to handle my specific exception for 'fps' unit.
            if(self.simulation_speed[0] != 0 and self.simulation_speed[0] != 0.0):
                time_step = [(1 / self.simulation_speed[0]), "s/t"]
                #print(f"Current Simulation Speed: {self.simulation_speed}, returning {time_step}!")
                return time_step
            else:
                time_step = [0, "s/t"]
                #print(f"Current Simulation Speed: {self.simulation_speed}, returning {time_step}!")
                return time_step
        else:                                   # Handle all other units.
            #print(f"Current Simulation Speed: {self.simulation_speed}")
            measurement = self.simulation_speed[1].split("/")
            units       = [self.get_time_unit(measurement[0]), self.get_time_unit(measurement[1])]
            prefixes    = [self.get_metric_prefix(measurement[0]), self.get_metric_prefix(measurement[1])]
            #print(f"measurement={measurement}, units={units}, prefixes={prefixes}")

            simple_speed = simplify(self.simulation_speed)
            #print(f"simple_speed={simple_speed}")

            # I'm going to convert frames and the 'tick' unit into 't'
            if(units[0] == 'fr' or units[0] == 'frame' or units[0] == 'tick'):
                units[0] = 't'
            if(units[1] == 'fr' or units[1] == 'frame' or units[1] == 'tick'):
                units[1] = 't'

            # Now that frames and ticks are logically accounted for, every other measurement has a conversion rate for seconds. Since the conversion has already been applied, I must correct it.
            if(units[0] != 't'): # Ticks are allowed and already converted for passed measurements. If it's a tick, I need to leave it alone.
                units[0] = 's'
            if(units[1] != 't'):
                units[1] = 's'

            return [simple_speed, f"{units[0]}/{units[1]}"]

    def validate_units(self, sim_speed, print_warnings=True):
        if(not isinstance(sim_speed, list)): # If the passed value is not a list...
            if(print_warnings):
                print(f"{COLORS[1]}WARNING:{COLORS[4]} validate_units was passed {sim_speed}, but requires format [int/float, str]! Returning False!")
            return False
        elif(len(sim_speed) != 2):                              # If the list does not have 2 elements...
            if(print_warnings):
                print(f"{COLORS[1]}WARNING:{COLORS[4]} validate_units was passed an incorrect number of parameters, but requires 2: [int/float, str]! Returning False!{COLORS[-1]}")
            return False
        elif((not isinstance(sim_speed[0], float) and not isinstance(sim_speed[0], int)) or not isinstance(sim_speed[1], str)): # If either element is not the correct data type...
            if(print_warnings):
                temp_string = f"{COLORS[1]}WARNING:{COLORS[4]} validate_units was passed incorrect parameters! "
                if(not isinstance(sim_speed[0], int) and not isinstance(sim_speed[0], float)):
                    temp_string += f"simulation_speed[0] should be of type int/float, "
                if(not isinstance(sim_speed[1], str)):
                    temp_string += f"simulation_speed[1] should be of type str, "
                temp_string = f"{temp_string[:-2]}! Returning False!{COLORS[-1]}"
                print(temp_string)
            return False
        elif(isinstance(sim_speed[0], bool)):                   # Bools count as ints. In python, they're a subclass. Fucking why?
            if(print_warnings):
                print(f"{COLORS[1]}WARNING:{COLORS[4]} validate_units was passed a bool for the number! Returning False!{COLORS[-1]}")
            return False
        elif(sim_speed[0] < 0 and self.disallow_negative_time): # No negative times. This is a headache, and physicists around the world argue about how this would even work. I'm not implementing it.
            if(print_warnings):
                print(f"{COLORS[1]}WARNING:{COLORS[4]} validate_units was passed a negative time value! Returning False!{COLORS[-1]}")
            return False
        elif(str(sim_speed[0]) == "nan"):                       # NAN? man...
            if(print_warnings):
                print(f"{COLORS[1]}WARNING:{COLORS[4]} validate_units was passed a \'NAN\' value! Returning False!{COLORS[-1]}")
            return False
        elif(sim_speed[1] == "fps"):                            # Explicit exception for 'frames-per-second', often used by people to talk about game speed.
            return True
        else:
            measurement = sim_speed[1].split("/")
            if(len(measurement) != 2):
                if(print_warnings):
                    user_info  = f"{COLORS[1]}WARNING:{COLORS[4]} Passed units are in an incorrect format! The acceptable format is: "
                    user_info += f"{COLORS[5]}\'(metric_prefix)(time_step_unit)/(metric_prefix)(operation_unit)\'{COLORS[4]}!{COLORS[-1]}\n"
                    user_info += f"{COLORS[4]}The time_step_unit is how far should time advice, the operation_unit is how often the simulation performs the time_step_unit."
                    print(f"{user_info}{COLORS[-1]}")
                return False
            valid_step_unit = True
            valid_time_unit = True
            step_unit       = [self.get_metric_prefix(measurement[0]), self.get_time_unit(measurement[0])]
            time_unit       = [self.get_metric_prefix(measurement[1]), self.get_time_unit(measurement[1])]
            if(step_unit[0] == None or step_unit[1] == None):
                valid_step_unit = False
            if(time_unit[0] == None or time_unit[1] == None):
                valid_time_unit = False
            if(not valid_step_unit or not valid_time_unit):
                if(print_warnings):
                    print(f"{COLORS[1]}WARNING:{COLORS[4]} Incorrect units were given \'{measurement}\', returning False!{COLORS[-1]}")
                return False
            else:
                return True
        print(f"{COLORS[1]}WARNING:{COLORS[4]} validate_units had a fatal error occur, ending program!{COLORS[-1]}")
        raise RuntimeError

    def get_metric_prefix(self, units):
        candidate = None
        for unit in self.acceptable_units["units"]:
            temp = units.split(unit)
            if(len(temp) == 2):
                if(temp[0] == '' and temp[1] == ''):
                    candidate =  ''
                if(temp[0] != '' and temp[1] == ''):
                    candidate = temp[0]   # The metric modifier gets split out of the list, the time_step unit stays
        if(candidate in self.acceptable_units["metric"] or candidate == ''):
            return candidate
        else:
            return None # Either invalid units or I messed up my logic somewhere

    def get_time_unit(self, units):
        for unit in self.acceptable_units["units"]:
            temp = units.split(unit)
            if(len(temp) == 2):
                if(temp == ['', '']):
                    return unit   # This is the unit, clearly. It had no modifier.
                elif(temp[1] == ''):
                    return unit   # It had a modifier.
        return None # Either invalid units or I messed up my logic somewhere