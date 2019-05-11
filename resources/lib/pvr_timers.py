#!/usr/bin/python
import time
from resources.lib.helper import *

#######################################################################################

class PVRTimers:

    def __init__(self):
        return

    def refresh(self):
        win_home = xbmcgui.Window(10000)
        widget_id = int(win_home.getProperty('widget_timers_id'))
        if widget_id == -1:
            return
        timestr = time.strftime("%Y%m%d%H%M%S", time.gmtime())
        win_home.setProperty('widgetreload-timers', timestr)
        widget = win_home.getControl(widget_id)
        if not widget.isVisible() and self.timersAvailable():
            widget.setVisibleCondition('true')
        log("timers widget reloaded")

    def delTimerDialog(self, timer_id):
        utc_offset = getUtcOffset()
        timer = self.fetchTimer(timer_id)
        header = xbmc.getLocalizedString(19060) + '?'
        line1 = timer['title']
        line2 = xbmc.getLocalizedString(846)
        dialog = xbmcgui.Dialog()
        yes = dialog.yesno(header, line1, line2)        
        if not yes:
            return False
        self.delTimer(timer_id)
        return True

    def timersAvailable(self):
        timers = self.fetchTimers()
        if len(timers) > 0:
            return True
        return False

    def fetchTimers(self):
        query = json_call('PVR.GetTimers',
                    properties=timer_properties
                )
        timers = None
        try:
            timers = query['result']['timers']
        except Exception:
            log("ERROR FETCH TIMERS")
            return []
        return timers

    def fetchTimer(self, timer_id):
        query = json_call('PVR.GetTimerDetails',
                    properties=timer_properties,
                    params={'timerid': int(timer_id)}
                )
        timer = None
        try:
            timer = query['result']['timerdetails']
        except Exception:
            log("ERROR FETCH TIMER")
            return None
        return timer

    def fetchChannel(self, channel_id):
        query = json_call('PVR.GetChannelDetails',
                properties=channel_properties,
                params={'channelid': channel_id}
            )
        channel = None
        try:
            channel = query['result']['channeldetails']
        except Exception:
            return None
        return channel

    def delTimer(self, timer_id):
        query = json_call('PVR.DeleteTimer',
                    params={ 'timerid': int(timer_id) }
                )

    def toggleTimer(self, timer_id):
        return
        #query = json_call('PVR.ToggleTimer',
        #            params={ 'timerid': int(timer_id) }
        #        )
