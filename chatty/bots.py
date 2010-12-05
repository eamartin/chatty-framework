import itertools
import time

from core import IRCConnection
from messages import IRCMessage
        
class IRCBot(object):
    def __init__(self, nick, server_infos):
        self.connections = {}
        for server in server_infos:
            c = IRCConnection(server['host'], server['port'], nick)
            c.connect()
            c.authenticate()
            time.sleep(1)
            for chan in server['chans']:
                c.join(chan)
            self.connections[server['host']] = c
            
    def activate(self):
        for c in itertools.cycle(self.connections.values()):
            event =  c.event_loop().next()
            if event:
                event.msg = IRCMessage.parse(event.text)
                if event.msg:
                    self.process(event)
                
    def process(self, irc):
        '''Hook for subclasses'''
        pass