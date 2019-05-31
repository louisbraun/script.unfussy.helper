#!/usr/bin/python
import locale
from resources.lib.helper import *

#######################################################################################

class PVRChannelList:

    def __init__(self):
        def_loc = ''
        try:
            def_loc = locale.getdefaultlocale()[0]
            locale.setlocale(locale.LC_ALL, def_loc)
        except Exception:
            log("ERROR setting locale: %s" % def_loc)

    def setChannelIds(self):
        query = json_call('PVR.GetChannels',
            properties=['channelnumber'],
            params={'channelgroupid': 'alltv'}
        )
        channels = []
        try:
            channels = query['result']['channels']
        except Exception:
            return None
        channel_ids = {}
        for channel in channels:
            channel_ids[channel['channelnumber']] = channel['channelid']
        win = xbmcgui.Window(10700)
        win.setProperty('channel_ids', json.dumps(channel_ids))

    def fetchBroadcasts(self, channel_id):
        query = json_call('PVR.GetBroadcasts',
            properties=broadcast_properties_short,
            params={'channelid': channel_id}
        )
        broadcasts = []
        try:
            broadcasts = query['result']['broadcasts']
        except Exception:
            return []
        broadcasts_beautified = self.beautifyBroadcasts(channel_id, broadcasts)
        return broadcasts_beautified

    def beautifyBroadcasts(self, channel_id, broadcasts):
        utc_offset = getUtcOffset()
        now = datetime.now()
        broadcasts_beautified = []
        for bc in broadcasts:
            starttime = getTimeFromString(bc['starttime'], '%Y-%m-%d %H:%M:%S', utc_offset)
            endtime = getTimeFromString(bc['endtime'], '%Y-%m-%d %H:%M:%S', utc_offset)
            if endtime < now:
                continue
            bc_beautified = {}
            bc_beautified['id'] = bc['broadcastid']
            bc_beautified['channel_id'] = channel_id
            bc_beautified['title'] = bc['title']
            bc_beautified['episodename'] = bc['episodename']
            bc_beautified['runtime'] = bc['runtime']
            bc_beautified['date'] = '%s' % starttime.strftime('%a %d.%b')
            bc_beautified['starttime'] = '%s' % starttime.strftime('%H:%M')
            bc_beautified['endtime'] = '%s' % endtime.strftime('%H:%M')
            broadcasts_beautified.append(bc_beautified)
        return broadcasts_beautified
