from errbot import BotPlugin, botcmd, backends
import subprocess
import urllib.request


class ErrNumerology(BotPlugin):
    """
    A very basic module to check the number of subscribers of some user.
    It expects to have the interface in Spanish.  For other languages, you 
    can try changing the line:

        word = 'suscriptores'
    """

    def get_configuration_template(self):
        """ configuration entries """
        config = {
            'ytUser': '',
            'msgTemplate': '',
            'channel': '#someChannel',
        }
        return config

    def _check_config(self, option):
        # if no config, return nothing
        if self.config is None:
            return None
        else:
            # now, let's validate the key
            if option in self.config:
                return self.config[option]
            else:
                return None

    @botcmd(split_args_with=None)
    def subscribers(self, msg, args):
        """Subscribers in YouTube"""
        self.log.debug("Args %s %s"%(args,type(args)))
        if args: 
            if isinstance(args, str):
                usr = args
            else:
                usr = args[0]
        else: 
            usr = self._check_config('ytUser')
        yield "Looking for the subscribers of %s" % usr
        msgTemplate = self._check_config('msgTemplate')
        chan = self._check_config('channel')
 

        r = str(urllib.request.urlopen('https://www.youtube.com/%s' % usr).read())
        
        word = 'suscriptores'
        start = r.find(word)
        end = r.find('<', start)
        
        if not msgTemplate:
            msgTemplate = "%s has %s followers"
        txt = msgTemplate % (usr, r[start+len(word)+2:end])

        yield(msg)
        self.log.info("msg %s type %s" % (msg, type(msg)))
        if (self._bot.mode == "irc") and isinstance(msg, backends.base.Message):
            room = self.build_identifier(chan)
            self.send(room, txt)
        else: 
            yield(txt)

    @botcmd(split_args_with=None)
    def followers(self, msg, args):
        """Followers in Twiter"""
        if args: 
            usr = args[0]
        else: 
            usr = self._check_config('ytUser')
        yield "Looking for the followers of %s" % usr

        msgTemplate = '' # self._check_config('msgTemplate')
        chan = self._check_config('channel')
 

        r = str(urllib.request.urlopen('https://twitter.com/%s' % usr).read())
        
        word = 'Seguidores'
        end = r.find(word)
        start = r.rfind('"', 0, end)
        if not msgTemplate:
            msgTemplate = "%s has %s followers"
        txt = msgTemplate % (usr, r[start+1:end])

        if (self._bot.mode == "irc") and isinstance(msg, backends.base.Message):
            room = self.build_identifier(chan)
            self.send(room, txt)
        else: 
            yield(txt)

