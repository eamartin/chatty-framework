import re

class IRCMessage(object):
    regex = re.compile(r':(?P<nick>.*?)!\S+\s+?(?P<type>[A-Z]+)\s+(?P<chan>.+?)\s+:(?P<msg>.+)')

    @classmethod
    def parse(cls, text):
        '''Fails silently and returns None if can't be parsed'''

        obj = cls()
        m = cls.regex.match(text)
        if m:
            D = m.groupdict()
            if '#' not in D['chan']:
                del D['chan']
            for key, value in D.iteritems():
                if key and value:
                    setattr(obj, key, value)
            return obj

    def __repr__(self):
        s = ''
        if hasattr(self, 'chan'):
            s = 'chan:' + self.chan + ' '
        s += 'type:' + self.type + ' nick:' + self.nick + ' msg:' + self.msg
        return s