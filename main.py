from Cyberspace import *
from Renderer import *
from util import *

def gen_sim_speed(range):
    all_prefixes = []
    all_units    = []
    for prefix in acceptable_units["metric"]:
        all_prefixes.append(prefix)
    for unit in acceptable_units["units"]:
        all_units.append(unit)
    #print(f"prefix_list={all_prefixes}\nunit_list={all_units}")

    integer  = 0
    flt      = 0.0
    speed = []
    function = random(15)
    if(function % 2 == 0): # Generate an integer speed
        integer = random(int(range))
        speed.append(integer)
    else:
        flt = float(f"{str(random(range - 1))}.{str(random(range - 1))}")
        speed.append(flt)
    #print(speed)

    prefixes = [all_prefixes[random(len(all_prefixes) - 1)], all_prefixes[random(len(all_prefixes) - 1)]]
    units    = [all_units[random(len(all_units) - 1)], all_units[random(len(all_units) - 1)]]
    #print(f"chosen prefixes: {prefixes}, chosen units: {units}")

    string = f"{prefixes[0]}{units[0]}/{prefixes[1]}{units[1]}"
    speed.append(string)
    #print(speed)

    return speed

def main():
    universe          = Universe()
    game_window       = Renderer(window_title="Suika Game Proto")
    frametime_counter = 0

    value = gen_sim_speed(1000)
    for i in range(5):
        universe.set_simulation_speed(value)
        value = gen_sim_speed(1000)

    #'''
    universe.addObject(game_window)

    frametimes = []

    total_start = perf_counter()
    for i in range(500):
        frametime_counter = perf_counter()
        universe.tick()
        frametimes.append((perf_counter() - frametime_counter))
        print(f"{'\033[92m'}Frametime was: {'\033[94m'}{frametimes[len(frametimes) - 1]:.6f}s")
    total_end   = perf_counter() - total_start

    average_frametime = 0
    max_frametime     = (-1, -1)
    min_frametime     = (99999999999, -1)
    for i in range(len(frametimes)):
        average_frametime += frametimes[i]
        if(frametimes[i] > max_frametime[0]):
            max_frametime = (frametimes[i], i)
        if(frametimes[i] < min_frametime[0]):
            min_frametime = (frametimes[i], i)
    average_frametime = average_frametime / len(frametimes)
    print(f"{'\033[0m'}Average Frametime:  {average_frametime}s\nMax Frametime:     {max_frametime}\nMin Frametime:     {min_frametime}")
    print(f"Total runtime was: {total_end:.6f}")

    try:
        universe.reverse_tick()
    except AttributeError:
        print("Object does not have a reverse_tick() function!")
    except TypeError:
        print("Object has reverse_tick, but it is not a function!")
    #'''

main()