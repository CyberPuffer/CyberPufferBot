try:
    from time import monotonic
except ImportError:
    from time import clock as monotonic
time_start = monotonic()