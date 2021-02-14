#!/usr/bin/python
import xbmc
import time
from resources.lib.helper import *

class KodiMonitor(xbmc.Monitor):

    def __init__(self, **kwargs):
        xbmc.Monitor.__init__(self)
        self.win = kwargs.get('win')

    def onDatabaseUpdated(self, database):
        pass

    def onNotification(self, sender, method, data):
        #log('unfussy_Monitor: sender %s - method: %s  - data: %s' % (sender, method, data))
        try:
            mediatype = ''
            data = json.loads(data)
            if data and isinstance(data, dict):
                if data.get('item'):
                    mediatype = data['item'].get('type', '')
                elif data.get('type'):
                    mediatype = data['type']
            if method == 'Player.OnStop':
                if mediatype == 'episode':
                    self.refresh_widget('nextepisodes')
        except Exception as ex:
            log('Exception in unfussy_Monitor: %s' % ex)


    def refresh_widget(self, widget):
        prop = 'widgetreload-' + widget
        self.win.setProperty(prop, time.strftime("%Y%m%d%H%M%S", time.gmtime()))