import time

from roadmap import Roadmap

from core import IRCConnection

        
class IRCBot(object):
    def __init__(self, nick, server):
        self.connection = IRCConnection(server['host'], server['port'], nick)
        self.connection.connect()
        self.connection.authenticate()
        time.sleep(1)
        for chan in server['chans']:
            self.connection.join(chan)
            
    def activate(self):
        for event in self.connection.event_loop():
            if event:
                self.process(event)
            else:
                continue
                
    def process(self, irc):
        '''Hook for subclasses'''
        pass

class RoutingBot(IRCBot, Roadmap):
    def __init__(self, *args, **kwargs):
        super(RoutingBot, self).__init__(*args, **kwargs)

    def process(self, irc):
        self.route((self, irc), key=repr(irc.msg))