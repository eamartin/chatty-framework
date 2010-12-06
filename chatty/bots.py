import itertools
import time
from threading import Thread

from roadmap import Roadmap

from core import IRCConnection
from messages import IRCMessage


class IRCBot(object):
    def __init__(self, nick, server_infos):
        self.conns = {}
        self.nick = nick
        self.server_infos = server_infos

    def activate(self):
        t = Thread(target=self._activate)
        t.start()

    def _activate(self):
        for connection in itertools.cycle(self.conns.values()):
            line = connection.event_loop().next()
            if line:
                msg = IRCMessage.parse(line)
                if msg:
                    connection.msg = msg
                    self.process(connection)

    def make_connections(self):
       for server in self.server_infos:
            self.conns[server['host']] = IRCConnection(server['host'],
                                                      server['port'], self.nick)
            self.conns[server['host']].connect()
            self.conns[server['host']].authenticate()
            time.sleep(2)
            for chan in server['chans']:
                self.conns[server['host']].join(chan)

    def process(self, irc):
        '''Hook for subclasses'''
        pass

class RoutingBot(IRCBot, Roadmap):
    def process(self, irc):
        self.route((self, irc), key=repr(irc.msg))