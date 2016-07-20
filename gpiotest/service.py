import time

import RPi.GPIO as gpio

from twisted.application import service
from twisted.internet import task, reactor, defer
from twisted.python import log

from .components import * 


class GpiotestService(service.Service):
    def __init__(self, config):
        self.config = config

        self.t = None
        self.srval = 0
        self.srval2 = 0


        self.adc = MCP3008(4, 27, 17, 22)

    #@defer.inlineCallbacks
    def loop(self):

        srval = self.adc.read(0)
        srval2 = self.adc.read(1)

        if srval != self.srval:
            self.srval = srval
            print "P1", "%d%%" % ((srval/800.0)*100)

        if srval2 != self.srval2:
            self.srval2 = srval2
            print "P2", "%d%%" % ((srval2/800.0)*100)


    #@defer.inlineCallbacks
    def startService(self):
        gpio.setmode(gpio.BCM)
        
        self.adc.setup()

        self.t = task.LoopingCall(self.loop)
        self.t.start(1)

    def stopService(self):
        gpio.cleanup()
