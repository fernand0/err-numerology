from errbot import BotPlugin, botcmd
import subprocess
import urllib.request


class ErrYoutube(BotPlugin):
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

    @botcmd
    def subscribers(self, msg, args):
        """Say hello to the world."""
        usr = self._check_config('ytUser')
        msgTemplate = self._check_config('msgTemplate')

        r = str(urllib.request.urlopen('https://www.youtube.com/%s' % usr).read())
        
        word = 'suscriptores'
        start = r.find(word)
        end = r.find('<', start)
        
        if not msgTemplate:
            msgTemplate = "%s has %s followers"
        txt = msgTemplate % (usr, r[start+len(word)+2:end])

        if (self._bot.mode == "irc"):
            room = self.build_identifier('#blogalia')
            self.send(room, txt)
        else: 
            yield(txt)


