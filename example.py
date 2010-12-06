from chatty.bots import RoutingBot

nick = 'lightbot'
delish = {'host': 'irc.deli.sh', 'port': 6667, 'chans': ('#bot_test',)}
freenode = {'host': 'irc.freenode.net', 'port': 6667, 'chans': ('#bot_test',)}


bot = RoutingBot(nick, (delish, freenode))

@bot.destination(r'chan:#.* type:PRIVMSG nick:.* msg:[Hh]i$')
def hello(bot, irc):
    irc.privmsg('Hello %s' % irc.msg.nick, chan=irc.msg.chan)

if __name__ == '__main__':
    bot.activate()