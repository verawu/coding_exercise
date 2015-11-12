# vim: set fileencoding=utf-8 :

from __future__ import absolute_import, print_function
import math
import os
import signal
import sys
import time
from datetime import date, datetime
# ---
from hailstorm.data.hail import Hail


epoch = datetime(*date.today().timetuple()[:-2])
interrupt = False

def gen(ts=None):
    then = datetime.now()
    delta = (then - epoch).total_seconds()

    while not interrupt:
        now = ts if ts is not None and isinstance(ts, datetime) else datetime.now()
        delta = (now - epoch).total_seconds() / 3600
        then = now
        coeff = _get_freq_coeff(delta)
        snooze = 0.1 / coeff

        yield Hail()

        time.sleep(snooze)

    sys.exit(0)


def _get_freq_coeff(x):
    # See: https://www.desmos.com/calculator/kgmnznvqhx
    #coeff = (2.25 * math.sin(((math.pi / 6) * x) + 3.25)) + 2.75
    coeff = (2.25 * (math.cos(((math.pi / 4) * x) + 1.5) * math.cos(((math.pi / 2.5) * x) + 4))) + 2.75
    return coeff


def _handle_sigint(*args):
    global interrupt
    interrupt = True


signal.signal(signal.SIGINT, _handle_sigint)
__all__ = ['gen']
