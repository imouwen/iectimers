# iectimers
IEC 61131-3 timers for Python

## Contents:
- TON: On Delay Timer
- TOF: Off Delay Timer
- TP: Pulse Timer

Like in a PLC these classes need to be called in a loop so they will be most useful
when you're building a GUI or are doing Computer Vision for instance.

## Example:

    import iectimers

    # Initialize timer
    TON_0 = iectimers.TON()

    # Set duration of the timer in seconds
    TON_0.PT = 0.5

    while True:
        TON_0.IN = some condition
        TON_0()
        if TON_0.Q:
            # do something

        # Alternatively:
        if TON_0(IN = some condition):
            # do something
