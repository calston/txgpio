from zope.interface import implements
 
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
 
import gpiotest
 
class Options(usage.Options):
    optParameters = [
        ["config", "c", "gpiotest.yml", "Config file"],
    ]
 
class GpiotestServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "gpiotest"
    description = "gpiotest"
    options = Options
 
    def makeService(self, options):
        try:
            config = yaml.load(open(options['config']))
        except:
            config = {}
        return gpiotest.makeService(config)
 
serviceMaker = GpiotestServiceMaker()
