import socket

class IRCConnection(object):
    def __init__(self, host, port, nick):
        self.host = host
        self.port = port
        self.nick = nick

    def connect(self):
        self._sock = socket.create_connection((self.host, self.port)).makefile()

    def disconnect(self):
        self.send('QUIT')
        self._sock.close()

    def send(self, data):
        self._sock.write('%s\r\n' % data)
        self._sock.flush()

    def authenticate(self):
        self.send('NICK %s' % self.nick)
        self.send('USER %s %s bla :%s' % (self.nick, self.host, self.nick))

    def join(self, channel):
        channel = channel.lstrip('#')
        self.send('JOIN #%s' % channel)

    def part(self, channel):
        channel = channel.lstrip('#')
        self.send('PART #%s' % channel)

    def privmsg(self, msg, chan=None, nick=None):
        if chan:
            chan = chan.lstrip('#')
            self.send('PRIVMSG #%s :%s' % (chan, msg))
        elif nick:
            self.send('PRIVMSG %s :%s' % (nick, msg))
        else:
            raise Exception('Chan or nick must be defined')

    def notice(self, msg, recip):
        self.send('NOTICE %s :%s' % (recip, msg))

    def event_loop(self):
        while not self._sock.closed:
            line = self._sock.readline()
            if not line:
                yield None
                continue
            line = line.rstrip()
            if line.startswith('PING'):
                self.send('PONG %s' % line.split()[1])
            else:
                self.text = line
                yield self
        self.text = 'CONNECTION_CLOSED'
        yield self
  