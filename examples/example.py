from irc.irc import IRCBot
from roadmap.roadmap import Roadmap

class RoutingBot(IRCBot, Roadmap):
    def __init__(self, *args, **kwargs):
        super(RoutingBot, self).__init__(*args, **kwargs)
        
    def process(self, irc):
        self.route((self, irc), key=repr(irc.msg))
        
s1 = ':lightcatcher!lightcatcher@delish-affe345f.sprntx.sbcglobal.net PRIVMSG #woot :hi lightbot'
s2 = ':lightcatcher!lightcatcher@delish-affe345f.sprntx.sbcglobal.net PRIVMSG lightbot :hi'
s3 = ':lightcatcher!lightcatcher@delish-affe345f.sprntx.sbcglobal.net NOTICE lightbot :whats up?'

if __name__ == '__main__':           
    HOST = 'irc.deli.sh'
    PORT = 6667
    chans = ['#woot',]
    nick = 'lightbot'
    info = {'host': HOST, 'port': PORT, 'chans': chans}

    bot = RoutingBot(nick, [info,])
    
    @bot.destination(r'chan:#.* type:PRIVMSG nick:.* msg:[Hh]i$')
    def hello(bot, irc):
        irc.privmsg('Hello %s' % irc.msg.nick, chan=irc.msg.chan)
        print bot.connections
    
    bot.activate()  