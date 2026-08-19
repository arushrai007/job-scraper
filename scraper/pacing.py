import random
import time

def polite_delay(min_seconds=2.0, max_seconds=5.0):
    """
    Pauses execution for a random duration between min_seconds and max_seconds.

    Why random instead of a fixed delay?
    A bot that waits exactly 3.000 seconds between every request is trivially
    detectable by timing analysis. Real humans (and even well-behaved scripts)
    have irregular gaps. Randomizing within a range mimics that irregularity
    without being wasteful or slow.
    """
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Waiting {delay:.2f}s before next request...")
    time.sleep(delay)