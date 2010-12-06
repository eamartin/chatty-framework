import time
from threading import Thread

from roadmap import Roadmap

from core import IRCConnection
from messages import IRCMessage


class IRCBot(object):
    def __init__(self, nick, server):
        self.connection = IRCConnection(server['host'], server['port'], nick)
        self.connection.connect()
        self.connection.authenticate()
        time.sleep(2)
        for chan in server['chans']:
            self.connection.join(chan)

    def activate(self):
        for line in self.connection.event_loop():
            if line:
                msg = IRCMessage.parse(line)
                if msg:
                    self.connection.msg = msg
                    Thread(target=self.process, args=(self.connection,)).start()
            else:
                continue

    def process(self, irc):
        '''Hook for subclasses'''
        pass

class RoutingBot(IRCBot, Roadmap):
    def __init__(self, *args, **kwargs):
        super(RoutingBot, self).__init__(*args, **kwargs)

    def process(self, irc):
        time.sleep(5)
        self.route((self, irc), key=repr(irc.msg))