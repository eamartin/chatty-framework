from chatty.bots import RoutingBot
import time

HOST = 'irc.deli.sh'
PORT = 6667
chans = ['#woot',]
nick = 'lightbot'
info = {'host': HOST, 'port': PORT, 'chans': chans}

bot = RoutingBot(nick, info)

@bot.destination(r'chan:#.* type:PRIVMSG nick:.* msg:[Hh]i$')
def hello(bot, irc):
    irc.privmsg('Hello %s' % irc.msg.nick, chan=irc.msg.chan)

bot.activate()
time.sleep(3)
bot.connection.privmsg('its working!', chan='#woot')