#!/usr/bin/python
import xbmcplugin
from resources.lib.helper import *
from resources.lib.pvr_running_at import PVRRunningAt
from resources.lib.pvr_timers import PVRTimers

#######################################################################################

class PluginContent:

    def __init__(self):
        self.resultlist = list()

    def result(self):
        return self.resultlist

    def fetchNextEpisodes( self ):
        inprogress_shows = self.getInprogressTVShows()
        for show in inprogress_shows:
            tvshowid = int(show['tvshowid'])
            last_played_episode = self.getLastPlayedEpisode(tvshowid)
            if not last_played_episode:
                continue
            next_episode_id = self.getNextEpisode(tvshowid, last_played_episode)
            if (next_episode_id > 0):
                next_episode = self.getEpisode(next_episode_id)
                append_items(self.resultlist,[next_episode],type='episodes')

    def fetchActors( self, movie_id, tvshow ):
        cast = []
        if movie_id:
            query = json_call('VideoLibrary.GetMovieDetails',
                    properties=['cast'],
                    params={'movieid': int(movie_id)}
                )
            cast = query['result']['moviedetails']['cast']
        elif tvshow:
            query = json_call('VideoLibrary.GetTVShows',
                    properties=['cast'],
                    limit=1,
                    query_filter={'operator': 'is', 'field': 'title', 'value': tvshow}
                )
            cast = query['result']['tvshows'][0]['cast']
        append_items(self.resultlist,cast,type='cast')

    def fetchRunningAt( self, pointintime, channel_ids ):
        running_at = PVRRunningAt()
        ok = pvrAvailable()
        if not ok:
            log("pvr not available, aborting")
            return
        channel_ids = channel_ids.replace('-', ',')
        channel_ids = json.loads(channel_ids)
        broadcast_ids = []
        for channel_id in channel_ids:
            bc = running_at.getBroadcastAt(pointintime, channel_id)
            if bc:
                broadcast = {
                    'broadcastid': bc['broadcastid'],
                    'channelid': channel_id
                }
                broadcast_ids.append(broadcast)
        broadcasts = running_at.getBroadcastsById(broadcast_ids)
        append_items(self.resultlist, broadcasts, type='broadcasts')

    def fetchTimers(self):
        ok = pvrAvailable()
        if not ok:
            log("pvr not available, aborting")
            return
        ti = PVRTimers()
        timers = ti.fetchTimers()
        for t in timers:
            channel = ti.fetchChannel(t['channelid'])
            if channel:
                t['channelicon'] = channel['icon']
            else:
                t['channelicon'] = ''
        append_items(self.resultlist, timers, type='timers')

    #######################################################################################
    # private
    #######################################################################################
    def getInprogressTVShows(self):
        query = json_call('VideoLibrary.GetTVShows',
                            properties=[], 
                            limit=25,
                            query_filter={'field': 'inprogress', 'operator': 'true', 'value': ''}
                        )
        try:
            tvshows = query['result']['tvshows']
        except Exception:
            log('getNextEpisodes: No Inprogress TVShows found.')
            return []
        return tvshows

    def getLastPlayedEpisode( self, tvshowid ):
        query = json_call('VideoLibrary.GetEpisodes',
                            properties=['season'],
                            limit=1,
                            sort={"method": "lastplayed", "order": "descending"},
                            query_filter={"field":"playcount", "operator":"isnot", "value":"0"},
                            params={'tvshowid': tvshowid}
                        )
        try:
            last_played = query['result']['episodes']
        except Exception:
            log('getLastPlayedEpisode: No Last Played Episode found.')
            return 0
        return last_played[0]

    def getNextEpisode( self, tvshowid, last_played_episode ):
        season = last_played_episode['season'] - 1
        query = json_call('VideoLibrary.GetEpisodes',
                            properties=[],
                            sort={"method": "episode"},
                            query_filter={"field":"season", "operator":"greaterthan", "value":"%s" % season},
                            params={'tvshowid': tvshowid}
                        )
        try:
            episodes = query['result']['episodes']
        except Exception:
            return 0

        found = False
        for episode in episodes:
            if (found):
                return episode['episodeid']
            if (episode['episodeid'] == last_played_episode['episodeid']):
                found = True
        return 0

    def getEpisode( self, episodeid ):
        query = json_call('VideoLibrary.GetEpisodeDetails',
                            properties=episode_properties,
                            params={'episodeid': episodeid}
                        )
        try:
            episode = query['result']['episodedetails']
        except Exception:
            return {}
        return episode
