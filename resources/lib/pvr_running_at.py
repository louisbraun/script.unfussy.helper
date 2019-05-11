#!/usr/bin/python
import time
from datetime import datetime, timedelta
import locale
from resources.lib.helper import *

#######################################################################################

class PVRRunningAt:

    def __init__(self):
        def_loc = locale.getdefaultlocale()[0]
        locale.setlocale(locale.LC_ALL, def_loc)
    
    def getBroadcastAt( self, starttime, channelid ):
        utc_offset = getUtcOffset()
        broadcasts = self.getBroadcasts(channelid)
        if not broadcasts:
            return None
        interval = self.getStartTimeInterval(starttime)
        starttime = interval[0]
        start_interval = interval[1]
        stop_interval = interval[2]
        bc = 0
        fallback = -1
        for broadcast in broadcasts:
            start_bc = getTimeFromString(broadcast['starttime'], '%Y-%m-%d %H:%M:%S', utc_offset)
            end_bc = getTimeFromString(broadcast['endtime'], '%Y-%m-%d %H:%M:%S', utc_offset)
            if start_bc > start_interval and start_bc < stop_interval and end_bc > stop_interval:
                return broadcast
            if start_bc < starttime and end_bc > starttime:
                fallback = bc 
            bc += 1
        if fallback > -1:
            return broadcasts[fallback]
        return None
    
    def showInfo(self, broadcast_id, channel_id, xml_file, xml_filepath):
        bc_id = [
            {
                'broadcastid': int(broadcast_id),
                'channelid': int(channel_id)
            }
        ]
        broadcasts = self.getBroadcastsById(bc_id)
        if len(broadcasts) == 0:
            log("error fetching broadcast details")
            return
        broadcast = broadcasts[0]
        win = xbmcgui.WindowXMLDialog(xml_file, xml_filepath)
        win.setProperty('broadcastid', str(broadcast['broadcastid']))
        win.setProperty('title', broadcast['title'])
        win.setProperty('plot', broadcast['plot'])
        win.setProperty('plotoutline', broadcast['plotoutline'])
        win.setProperty('cast', broadcast['cast'])
        win.setProperty('genre',  ', '.join(broadcast['genre']))
        win.setProperty('director', broadcast['director'])
        win.setProperty('episodename', broadcast['episodename'])
        win.setProperty('episodenum', str(broadcast['episodenum']))
        win.setProperty('episodepart', str(broadcast['episodepart']))
        win.setProperty('thumbnail', broadcast['thumbnail'])
        win.setProperty('year', str(broadcast['year']))
        win.setProperty('date', broadcast['date'])
        win.setProperty('datelong', broadcast['datelong'])
        win.setProperty('starttime', broadcast['starttime'])
        win.setProperty('endtime', broadcast['endtime'])
        win.setProperty('runtime', str(broadcast['runtime']))
        win.setProperty('switchdate', broadcast['switchdate'])
        win.setProperty('channelid', str(broadcast['channel']['channelid']))
        win.setProperty('channel', broadcast['channel']['channel'])
        win.setProperty('channelnumber', str(broadcast['channel']['channelnumber']))
        win.setProperty('channelicon', broadcast['channel']['icon'])
        win.doModal()
        del win

    def setTimer(self, bc_id):
        query = json_call('PVR.AddTimer',
                    params={ 'broadcastid': int(bc_id) }
                )

    #######################################################################################
    # private
    #######################################################################################

    def getBroadcasts(self, channelid):
        query = json_call('PVR.GetBroadcasts',
                    params={ 'channelid': channelid },
                    properties=['starttime', 'endtime']
                )
        try:
            broadcasts = query['result']['broadcasts']
        except Exception:
            log("ERROR getBroadcast")
            return None
        return broadcasts

    def getBroadcastsById(self, broadcast_ids):
        utc_offset = getUtcOffset()
        broadcasts = []
        for bc in broadcast_ids:
            bc_id = bc['broadcastid']
            channel_id = bc['channelid']
            query = json_call('PVR.GetBroadcastDetails',
                        params={ 'broadcastid': bc_id },
                        properties=broadcast_properties
                    )
            try:
                broadcast = query['result']['broadcastdetails']
                starttime = getTimeFromString(broadcast['starttime'], '%Y-%m-%d %H:%M:%S', utc_offset)
                endtime = getTimeFromString(broadcast['endtime'], '%Y-%m-%d %H:%M:%S', utc_offset)
                broadcast['date'] = '%s' % starttime.strftime('%d.%m')
                broadcast['datelong'] = '%s' % starttime.strftime('%a %d.%b')
                broadcast['starttime'] = '%s' % starttime.strftime('%H:%M')
                broadcast['endtime'] = '%s' % endtime.strftime('%H:%M')
                broadcast['switchdate'] = '%s' % starttime.strftime('%d.%m.%Y %H:%M')
                broadcast['cast'] = self.beautifyCast(broadcast['cast'])
                broadcast['channel'] = self.getChannelDetails(channel_id)
                broadcasts.append(broadcast)
            except Exception:
                log("ERROR GetBroadcastDetails")
        return broadcasts

    def beautifyCast(self, cast):
        if not cast:
            return ''
        actors = cast.split(',')
        str_actors = ''
        for actor in actors:
            str_actors += '\n'+actor
        return str_actors

    def getChannelDetails(self, channel_id):
        channel = None
        query = json_call('PVR.GetChannelDetails',
                    properties=channel_properties,
                    params={'channelid': channel_id}
                )
        try:
            channel = query['result']['channeldetails']
        except Exception:
            return None
        return channel
    
    def getStartTimeInterval(self, str_starttime):
        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y")
        starttime = getTimeFromString(date_now + ' ' + str_starttime, '%m-%d-%Y %H:%M')
        if now > starttime:
            starttime = starttime + timedelta(days=1)
        start_interval = starttime - timedelta(seconds=300)
        stop_interval = starttime + timedelta(seconds=300)
        return (starttime, start_interval, stop_interval)
