#!/usr/bin/python
import xbmcplugin
try:
    from urllib2 import urlparse
except ImportError:
    import urllib.parse as urlparse
from resources.lib.helper import *
from resources.lib.plugin_content import PluginContent
#######################################################################################

class Main:

    def __init__(self):
        self._parse_argv()
        self.info = self.params.get('info')
        if self.info:
            self.LoadInfos()

    def LoadInfos(self):
        pc = PluginContent()
        if self.info == 'getnextepisodes':
            pc.fetchNextEpisodes()
        elif self.info == 'getcast':
            pc.fetchActors(self.params.get('movie'), self.params.get('tvshow'))
        if self.info == 'getrunningat':
            pc.fetchRunningAt(self.params.get('pointintime'), self.params.get('channels'))
        elif self.info == 'gettimers':
            pc.fetchTimers()

        xbmcplugin.addDirectoryItems(self.widget_handle, pc.result())
        xbmcplugin.endOfDirectory(handle=self.widget_handle)

    def _parse_argv(self):
        try:
            path = sys.argv[2]
            self.params = dict(urlparse.parse_qsl(path[1:]))
            self.widget_handle = int(sys.argv[1])
        except Exception:
            self.params = {}
    
#######################################################################################

if __name__ == '__main__':
    Main()
