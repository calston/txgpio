import RPi.GPIO as gpio

from twisted.internet import reactor, defer
from twisted.python import log


def wait(msecs):
    d = defer.Deferred()
    reactor.callLater(msecs/1000.0, d.callback, None)
    return d

class ShiftRegister(object):
    def __init__(self, serial, clock, latch, frequency=0.01):
        self.serial = serial
        self.clock = clock
        self.latch = latch
        self.freq = frequency

    def setup(self):
        gpio.setup(self.serial, gpio.OUT)
        gpio.setup(self.clock, gpio.OUT)
        gpio.setup(self.latch, gpio.OUT)

    def clear(self):
        return self.shiftOut(0)

    @defer.inlineCallbacks
    def shiftOut(self, val, bits=8, msbf=True):
        gpio.output(self.latch, 0)

        s = ""
        if msbf:
            cnt = reversed(xrange(bits))
        else:
            cnt = xrange(bits)

        for i in cnt:
            b = (val >> i) & 1

            s += str(b)
            gpio.output(self.clock, 0)
            gpio.output(self.serial, b)
            yield wait(self.freq)
            gpio.output(self.clock, 1)

        gpio.output(self.clock, 0)
        #log.msg("[shiftreg] %s:0b%s" % (self.serial, s))
        gpio.output(self.latch, 1)
        
