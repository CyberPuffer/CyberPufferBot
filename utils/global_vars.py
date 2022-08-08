# Speciel global varibles
try:
    from time import monotonic
except ImportError:
    from time import clock as monotonic
start_time = monotonic()

# Message handler registry
message_handler = {}