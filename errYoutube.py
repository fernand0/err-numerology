from errbot import BotPlugin, botcmd
import subprocess
import urllib.request


class ErrYoutube(BotPlugin):
    """Example 'Hello, world!' plugin for Errbot."""

    def get_configuration_template(self):
        """ configuration entries """
        config = {
            'ytUser': '',
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

        r = str(urllib.request.urlopen('https://www.youtube.com/%s' % usr).read())
        
        word = 'suscriptores'
        start = r.find(word)
        end = r.find('<', start)
        
        txt = "%s tiene %s suscriptores, cabrones" % (usr, r[start+len(word)+2:end])
        if (self._bot.mode == "irc"):
            room = self.build_identifier('#blogalia')
            self.send(room, txt)
        else: 
            yield(txt)


