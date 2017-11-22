import sys
import math

usage = """Lunar Lander

Usage:
Start with no options or three values for initial altitude, speed and fuel.
"""

if len(sys.argv) > 1:
    if len(sys.argv) != 4:
        print(usage)
        sys.exit()
    else:
        h_0, v_0, fuel = map(float, sys.argv[1:])
else:
    # some sensible defaults
    h_0 = 500.0
    v_0 = 50.0
    fuel = 120.0

print('Enter a thrust value beteen 0 and 10 to counter gravity.\n')
spacer = ' ' * int(h_0/4 - 14)
print('TIME  ALTITUDE   SPEED   FUEL       PLOT OF DISTANCE {spacer} THRUST'.format(spacer=spacer))
t = 0
status = ' {:>2}      {:>4}    {:>4}   {:>4}    |    {graph}  ? '
g = 5.0
v = v_0
h = h_0
max_thrust = 10
while True:
    if h <= 0:
        # remaining time is probably less than 1s
        t_rem = (math.sqrt(2 * g * prev_h + prev_v * prev_v) - prev_v) / g
        v = prev_v + t_rem * g
        print('Touchdown at {:>4.2f} seconds'.format(t+t_rem-1))
        print('You hit the ground with speed {:>5.3f}'.format(v))
        if v <= 10:
            print('You made it home safely :)')
        else:
            print('You were crushed on impact :(')
        break

    pre = ' ' * int(h/4)
    post = ' ' * int(h_0/4 - int(h/4))
    graph = pre + 'X' + post

    try:
        s = raw_input(status.format(t, int(h), int(v), int(fuel), graph=graph))
    except (EOFError, KeyboardInterrupt):
        print
        break
    try:
        if len(s) == 0 or fuel <= 0:
            thrust = 0
        else:
            thrust = float(s)
            if thrust < 0:
                thrust = 0
            if thrust > max_thrust:
                thrust = max_thrust
            if thrust > fuel:
                thrust = fuel
    except ValueError:
        continue

    prev_h = h
    prev_v = v
    accel = g - thrust
    v = prev_v + accel
    h = prev_h - prev_v - accel/2

    t += 1
    fuel -= thrust
