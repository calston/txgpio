import time

import RPi.GPIO as gpio

from twisted.application import service
from twisted.internet import task, reactor, defer
from twisted.python import log


BROWN = 26
BROWN_WHITE = 19
GREEN = 13
GREEN_WHITE = 6
BLUE = 5
BLUE_WHITE = 11

def wait(msecs):
    d = defer.Deferred()
    reactor.callLater(msecs/1000.0, d.callback, None)
    return d

class ShiftRegister(object):
    def __init__(self, serial, clock, latch, frequency=0):
        self.serial = serial
        self.clock = clock
        self.latch = latch
        self.freq = frequency

    def setup(self):
        gpio.setup(self.serial, gpio.OUT)
        gpio.setup(self.clock, gpio.OUT)
        gpio.setup(self.latch, gpio.OUT)

    def clear(self):
        # Flush the shift register
        pass

    @defer.inlineCallbacks
    def shiftOut(self, val, bits=8):
        gpio.output(self.latch, 0)
        s = ""
        for i in reversed(xrange(bits)):
            b = (val >> i) & 1

            s += str(b)
            gpio.output(self.clock, 0)
            gpio.output(self.serial, b)
            yield wait(self.freq)
            gpio.output(self.clock, 1)
            yield wait(self.freq)

        gpio.output(self.clock, 0)
        log.msg("[shiftreg] %s:0b%s" % (self.serial, s))
        gpio.output(self.latch, 1)
        
class SegmentDisplay(object):
    def __init__(self, serial, clock, latch):
        self.sr = ShiftRegister(serial, clock, latch)

        self.chars = {
            ' ': 0b00000000,
            '0': 0b01110111,
            '1': 0b01000100,
            '2': 0b01101011,
            '3': 0b01101110,
            '4': 0b01011100,
            '5': 0b00111110,
            '6': 0b00011111,
            '7': 0b01100100,
            '8': 0b01111111,
            '9': 0b01111100,
            '-': 0b00001000,
            'A': 0b01111101,
            'C': 0b00110011,
            'E': 0b00111011,
            'F': 0b00111001,
            'G': 0b01111110,
            'H': 0b01011101,
            'I': 0b00010001,
            'J': 0b01000110,
            'L': 0b00010011,
            'N': 0b00001101,
            'O': 0b00001111,
            'P': 0b01111001,
            'R': 0b00001001,
            'U': 0b01010111,
            'Y': 0b01011001,
        }

    @defer.inlineCallbacks
    def setup(self):
        self.sr.setup()
        yield self.display(0)
        defer.returnValue(None)

    @defer.inlineCallbacks
    def display(self, val):
        i = str(val).upper()
        if i in self.chars:
            v = self.chars[i]

            yield self.sr.shiftOut(v ^ 0b11111111)
        defer.returnValue(None)


class GpiotestService(service.Service):
    def __init__(self, config):
        self.config = config

        self.pins = (BROWN, BROWN_WHITE, GREEN, GREEN_WHITE, BLUE, BLUE_WHITE)

        self.t = None

        self.s1 = False

        self.srval = 0

        self.disp = SegmentDisplay(GREEN_WHITE, BLUE, BLUE_WHITE)
        self.chars = "colin"

    @defer.inlineCallbacks
    def loop(self):

        self.s1 = not self.s1

        if self.s1:
            gpio.output(BROWN, gpio.HIGH)
        else:
            gpio.output(BROWN, gpio.LOW)

        if self.srval == len(self.chars):
            self.srval = 0

        yield self.disp.display(self.chars[self.srval])

        self.srval += 1

    @defer.inlineCallbacks
    def startService(self):
        gpio.setmode(gpio.BCM)
        
        for pin in self.pins:
            gpio.setup(pin, gpio.OUT)
        
        yield self.disp.setup()

        self.t = task.LoopingCall(self.loop)
        self.t.start(0.5)

    def stopService(self):
        gpio.cleanup()
