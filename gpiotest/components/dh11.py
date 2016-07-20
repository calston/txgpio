import RPi.GPIO as gpio

from twisted.internet import task, reactor, defer


def wait(msecs):
    d = defer.Deferred()
    reactor.callLater(msecs/1000.0, d.callback, None)
    return d

class DH11(object):
    def __init__(self, pin):
        self.pin = pin

    def setup(self):
        pass

    def _wait_for_input(self):
        d = defer.Deferred
        def _check(d):
            v = gpio.input(self.pin)

            if not v:
                reactor.callLater(0, self._check, d)
        



    @defer.inlineCallbacks
    def read(self):
        gpio.setup(self.pin, gpio.OUT)
        gpio.output(self.pin, gpio.HIGH)
        yield wait(500)
        gpio.output(self.pin, gpio.LOW)
        yield wait(20)
        
        gpio.setup(self.pin, gpio.IN)

        
        
