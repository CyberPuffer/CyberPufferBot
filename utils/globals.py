try:
    from time import monotonic
except ImportError:
    from time import clock as monotonic
time_start = monotonic()
global_commands = []
webhook = False
dispatcher = None
config = None