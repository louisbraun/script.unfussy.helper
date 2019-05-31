#!/usr/bin/python
# coding: utf-8

########################

import xbmc
import xbmcaddon
import xbmcgui
import json
import time
from datetime import datetime, timedelta, tzinfo

########################

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')

NOTICE = xbmc.LOGNOTICE
WARNING = xbmc.LOGWARNING
DEBUG = xbmc.LOGDEBUG
LOG_ENABLED = True if ADDON.getSetting('log') == 'true' else False
DEBUGLOG_ENABLED = True if ADDON.getSetting('debuglog') == 'true' else False

########################

def log(txt,loglevel=NOTICE,force=False):

    if ((loglevel == NOTICE or loglevel == WARNING) and LOG_ENABLED) or (loglevel == DEBUG and DEBUGLOG_ENABLED) or force:

        ''' Python 2 requires to decode stuff at first
        '''
        try:
            if isinstance(txt, str):
                txt = txt.decode('utf-8')
        except AttributeError:
            pass

        message = u'[ %s ] %s' % (ADDON_ID,txt)

        try:
            xbmc.log(msg=message.encode('utf-8'), level=loglevel) # Python 2
        except TypeError:
            xbmc.log(msg=message, level=loglevel)


def json_call(method,properties=None,sort=None,query_filter=None,limit=None,params=None,item=None):

    json_string = {'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': {}}

    if properties is not None:
        json_string['params']['properties'] = properties

    if limit is not None:
        json_string['params']['limits'] = {'start': 0, 'end': limit}

    if sort is not None:
        json_string['params']['sort'] = sort

    if query_filter is not None:
        json_string['params']['filter'] = query_filter

    if item is not None:
        json_string['params']['item'] = item

    if params is not None:
        json_string['params'].update(params)

    json_string = json.dumps(json_string)
    result = xbmc.executeJSONRPC(json_string)

    ''' Python 2 compatibility
    '''
    try:
        result = unicode(result, 'utf-8', errors='ignore')
    except NameError:
        pass

    result = json.loads(result)

    log('json-string: %s' % json_string, DEBUG)
    log('json-result: %s' % result, DEBUG)

    return result

def visible(condition):
    return xbmc.getCondVisibility(condition)

def indent(elem, level=0):
  i = "\n" + level*"  "
  if len(elem):
    if not elem.text or not elem.text.strip():
      elem.text = i + "  "
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
    for elem in elem:
      indent(elem, level+1)
    if not elem.tail or not elem.tail.strip():
      elem.tail = i
  else:
    if level and (not elem.tail or not elem.tail.strip()):
      elem.tail = i

def pvrAvailable():
    retries = 0
    num_retries = 50
    while retries < num_retries:
        channels = json_call('PVR.GetChannels', limit=1, params={'channelgroupid': 'alltv'})
        try:
            channel_id = channels['result']['channels'][0]['channelid']
            broadcast = json_call('PVR.GetBroadcasts', params={ 'channelid': channel_id }, limit=1)
            try:
                bc = broadcast['result']['broadcasts']
                xbmc.sleep(200)
                log("pvrAvailable: success...continue")
                return True
            except Exception:
                retries += 1
                log("pvrAvailable: no broadcast found, sleep 500ms")
                xbmc.sleep(500)                
                continue
        except:
            retries += 1
            log("pvrAvailable: no channel found, sleep 500ms")
            xbmc.sleep(500)                
    return False

def encode4XML(value):
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, unicode):
        return value
    else:
        return value.decode('utf-8')

def getTimeFromString(str_time, format, utc_offset=None):
    dt = None
    ok = False
    while not ok:
        try:
            dt = datetime(*(time.strptime(str_time, format)[0:6]))
            if utc_offset:
                dt += utc_offset
            ok = True
        except Exception:
            ok = False
    return dt

def getUtcOffset():
    now_local = datetime.now()
    now_utc = datetime.utcnow()
    if now_local > now_utc:
        return now_local - now_utc
    else:
        return now_utc - now_local

######################################################################
# plugin content helpers
######################################################################
movie_properties = [
                    'title',
                    'originaltitle',
                    'votes',
                    'playcount',
                    'year',
                    'genre',
                    'studio',
                    'country',
                    'tagline',
                    'plot',
                    'runtime',
                    'file',
                    'plotoutline',
                    'lastplayed',
                    'trailer',
                    'rating',
                    'resume',
                    'art',
                    'streamdetails',
                    'mpaa',
                    'director',
                    'writer',
                    'cast',
                    'dateadded',
                    'imdbnumber'
                ]

episode_properties = [
                    'title',
                    'playcount',
                    'season',
                    'episode',
                    'showtitle',
                    'plot',
                    'file',
                    'rating',
                    'resume',
                    'tvshowid',
                    'firstaired',
                    'art',
                    'streamdetails',
                    'runtime',
                    'director',
                    'writer',
                    'cast',
                    'dateadded',
                    'lastplayed'
                ]

season_properties = [
                    'season',
                    'episode',
                    'art',
                    'watchedepisodes',
                    'showtitle',
                    'playcount',
                    'tvshowid'
                ]

tvshow_properties = [
                    'title',
                    'studio',
                    'year',
                    'plot',
                    'cast',
                    'rating',
                    'votes',
                    'genre',
                    'episode',
                    'season',
                    'mpaa',
                    'premiered',
                    'playcount',
                    'art',
                    'dateadded',
                    'watchedepisodes',
                    'imdbnumber'
                ]

channel_properties = [
                    'channel',
                    'icon',
                    'channelnumber'
]

channeldetail_properties = [
                    'broadcastnext',
                    'broadcastnow',
                    'channel',
                    'channelnumber',
                    'icon'
]

broadcast_properties = [
                    'title',
                    'starttime',
                    'endtime',
                    'plot',
                    'plotoutline',
                    'cast',
                    'genre',
                    'director', 
                    'episodename',
                    'episodenum',
                    'episodepart',
                    'thumbnail',
                    'year',
                    'runtime'
                ]

broadcast_properties_short = [
                    'title',
                    'starttime',
                    'endtime',
                    'episodename',
                    'runtime'
                ]

timer_properties = [
                    'channelid',
                    'endtime',
                    'isradio',
                    'starttime',
                    'state',
                    'summary',
                    'title'
]

def append_items(li, json_query, type):

    for item in json_query:

        if type == 'movies':
            parse_movies(li, item)
        elif type ==  'tvshows':
            parse_tvshows(li, item)
        elif type == 'seasons':
            parse_seasons(li, item)
        elif type == 'episodes':
            parse_episodes(li, item)
        elif type == 'genre':
            parse_genre(li, item)
        elif type == 'cast':
            parse_cast(li, item)
        elif type == 'broadcasts':
            parse_broadcast(li, item)
        elif type == 'broadcasts_short':
            parse_broadcast_short(li, item)
        elif type == 'timers':
            parse_timers(li, item)

def parse_movies(li, item):

    if 'cast' in item:
        cast = _get_cast(item['cast'])

    li_item = xbmcgui.ListItem(item['title'])
    li_item.setInfo(type='Video', infoLabels={'Title': item['title'],
                                            'OriginalTitle': item['originaltitle'],
                                            'Year': item['year'],
                                            'Genre': _get_joined_items(item.get('genre', '')),
                                            'Studio': _get_first_item(item.get('studio', '')),
                                            'Country': _get_first_item(item.get('country', '')),
                                            'Plot': item['plot'],
                                            'PlotOutline': item['plotoutline'],
                                            'dbid': item['movieid'],
                                            'imdbnumber': item['imdbnumber'],
                                            'Tagline': item['tagline'],
                                            'Rating': str(float(item['rating'])),
                                            'Votes': item['votes'],
                                            'MPAA': item['mpaa'],
                                            'lastplayed': item['lastplayed'],
                                            'Cast': cast[0],
                                            'CastAndRole': cast[1],
                                            'mediatype': 'movie',
                                            'Trailer': item['trailer'],
                                            'Playcount': item['playcount']})
    li_item.setProperty('resumetime', str(item['resume']['position']))
    li_item.setProperty('totaltime', str(item['resume']['total']))
    li_item.setProperty('fanart_image', item['art'].get('fanart', ''))
    li_item.setArt(item['art'])
    li_item.setThumbnailImage(item['art'].get('poster', ''))
    li_item.setIconImage('DefaultVideo.png')

    hasVideo = False

    for key, value in iter(item['streamdetails'].items()):
        for stream in value:
            if 'video' in key:
                hasVideo = True
            li_item.addStreamInfo(key, stream)

    if not hasVideo: # if duration wasnt in the streaminfo try adding the scraped one
        stream = {'duration': item['runtime']}
        li_item.addStreamInfo('video', stream)

    li.append((item['file'], li_item, False))


def parse_tvshows(li, item):

    if 'cast' in item:
        cast = _get_cast(item['cast'])

    rating = str(round(item['rating'],1))
    dbid = str(item['tvshowid'])
    season = str(item['season'])
    episode = str(item['episode'])
    watchedepisodes = str(item['watchedepisodes'])

    if int(episode) > int(watchedepisodes):
        unwatchedepisodes = int(episode) - int(watchedepisodes)
        unwatchedepisodes = str(unwatchedepisodes)
    else:
        unwatchedepisodes = '0'

    year = str(item['year'])
    mpaa = item['year']

    if not visible('Window.IsVisible(movieinformation)'):
        folder = True
        item['file'] = 'videodb://tvshows/titles/%s/' % dbid
    else:
        folder = False
        item['file'] = 'plugin://script.embuary.helper/?action=jumptoshow&dbid=%s' % dbid

    li_item = xbmcgui.ListItem(item['title'])
    li_item.setInfo(type='Video', infoLabels={'Title': item['title'],
                                            'Year': year,
                                            'Genre': _get_joined_items(item.get('genre', '')),
                                            'Studio': _get_first_item(item.get('studio', '')),
                                            'Country': _get_first_item(item.get('country', '')),
                                            'Plot': item['plot'],
                                            'Rating': rating,
                                            'Votes': item['votes'],
                                            'Premiered': item['premiered'],
                                            'MPAA': mpaa,
                                            'Cast': cast[0],
                                            'CastAndRole': cast[1],
                                            'mediatype': 'tvshow',
                                            'dbid': dbid,
                                            'season': season,
                                            'episode': episode,
                                            'tvshowtitle': item['title'],
                                            'imdbnumber': str(item['imdbnumber']),
                                            'Path': item['file'],
                                            'DateAdded': item['dateadded'],
                                            'Playcount': item['playcount']})
    li_item.setProperty('TotalSeasons', season)
    li_item.setProperty('TotalEpisodes', episode)
    li_item.setProperty('WatchedEpisodes', watchedepisodes)
    li_item.setProperty('UnwatchedEpisodes', unwatchedepisodes)
    li_item.setArt(item['art'])
    li_item.setThumbnailImage(item['art'].get('poster', ''))
    li_item.setIconImage('DefaultVideo.png')

    li.append((item['file'], li_item, folder))


def parse_seasons(li, item):

    tvshowdbid = str(item['tvshowid'])
    seasonnr = str(item['season'])
    episode = str(item['episode'])
    watchedepisodes = str(item['watchedepisodes'])

    if seasonnr == '0':
        title = '%s' % (xbmc.getLocalizedString(20381))
    else:
        title = '%s %s' % (xbmc.getLocalizedString(20373), seasonnr)

    if int(episode) > int(watchedepisodes):
        unwatchedepisodes = int(episode) - int(watchedepisodes)
        unwatchedepisodes = str(unwatchedepisodes)
    else:
        unwatchedepisodes = '0'

    if not visible('Window.IsVisible(movieinformation)'):
        folder = True
        file = 'videodb://tvshows/titles/%s/%s/' % (tvshowdbid, seasonnr)
    else:
        folder = False
        file = 'plugin://script.embuary.helper/?action=jumptoseason&dbid=%s&season=%s' % (tvshowdbid, seasonnr)

    li_item = xbmcgui.ListItem(title)
    li_item.setInfo(type='Video', infoLabels={'Title': title,
                                            'season': seasonnr,
                                            'episode': episode,
                                            'tvshowtitle': item['showtitle'],
                                            'playcount': item['playcount'],
                                            'mediatype': 'season',
                                            'dbid': item['seasonid']})
    li_item.setArt(item['art'])
    li_item.setProperty('WatchedEpisodes', watchedepisodes)
    li_item.setProperty('UnwatchedEpisodes', unwatchedepisodes)
    li_item.setThumbnailImage(item['art'].get('poster', ''))
    li_item.setIconImage('DefaultVideo.png')

    if seasonnr == '0':
        li_item.setProperty('IsSpecial', 'true')

    li.append((file, li_item, folder))


def parse_episodes(li, item):

    if 'cast' in item:
        cast = _get_cast(item['cast'])

    label = str(item['season']) + 'x' + str(item['episode']).zfill(2) + '. ' + item['title']
    li_item = xbmcgui.ListItem(label)
    li_item.setInfo(type='Video', infoLabels={'Title': item['title'],
                                            'Episode': item['episode'],
                                            'Season': item['season'],
                                            'Premiered': item['firstaired'],
                                            'Dbid': str(item['episodeid']),
                                            'Plot': item['plot'],
                                            'TVshowTitle': item['showtitle'],
                                            'lastplayed': item['lastplayed'],
                                            'Rating': str(float(item['rating'])),
                                            'Playcount': item['playcount'],
                                            'Director': _get_joined_items(item.get('director', '')),
                                            'Writer': _get_joined_items(item.get('writer', '')),
                                            'Cast': cast[0],
                                            'CastAndRole': cast[1],
                                            'mediatype': 'episode'})
    li_item.setProperty('resumetime', str(item['resume']['position']))
    li_item.setProperty('totaltime', str(item['resume']['total']))
    li_item.setProperty('fanart_image', item['art'].get('item.fanart', ''))
    li_item.setArt(item['art'])
    li_item.setThumbnailImage(item['art'].get('thumb', ''))
    li_item.setIconImage('DefaultTVShows.png')

    hasVideo = False

    for key, value in iter(item['streamdetails'].items()):
        for stream in value:
            if 'video' in key:
                hasVideo = True
            li_item.addStreamInfo(key, stream)

    if not hasVideo: # if duration wasnt in the streaminfo try adding the scraped one
        stream = {'duration': item['runtime']}
        li_item.addStreamInfo('video', stream)

    if item['season'] == '0':
        li_item.setProperty('IsSpecial', 'true')

    li.append((item['file'], li_item, False))


def parse_cast(li,item):
    li_item = xbmcgui.ListItem(item['name'])
    li_item.setLabel(item['name'])
    li_item.setLabel2(item['role'])
    li_item.setThumbnailImage(item.get('thumbnail', ''))
    li_item.setIconImage('DefaultActor.png')

    li.append(('', li_item, False))

def parse_broadcast(li, item):
    li_item = xbmcgui.ListItem(item['label'])
    li_item.setInfo(type='Video', infoLabels={'Title': item['title']})
    li_item.setArt({ 'icon': item['channel']['icon'] })
    li_item.setProperty('date', item['date'])
    li_item.setProperty('datelong', item['datelong'])
    li_item.setProperty('starttime', item['starttime'])
    li_item.setProperty('endtime', item['endtime'])
    li_item.setProperty('channelid', str(item['channel']['channelid']))
    li_item.setProperty('broadcastid', str(item['broadcastid']))
    plot = item['plot'].replace('\n', ' ')
    li_item.setProperty('plot', plot)
    genre = ''
    for g in item['genre']: genre += g + ', '
    genre = genre[:-2]
    li_item.setProperty('genre', genre)
    li.append(('', li_item, False))

def parse_broadcast_short(li, item):
    li_item = xbmcgui.ListItem(item['title'])
    li_item.setProperty('broadcastid', str(item['id']))
    li_item.setProperty('channelid', str(item['channel_id']))
    li_item.setProperty('date', item['date'])
    li_item.setProperty('starttime', item['starttime'])
    li_item.setProperty('endtime', item['endtime'])
    li_item.setProperty('episodename', item['episodename'])
    li_item.setProperty('runtime', str(item['runtime']))
    li.append(('', li_item, False))

def parse_timers(li, item):
    utc_offset = getUtcOffset()
    li_item = xbmcgui.ListItem(item['label'])
    li_item.setInfo(type='Video', infoLabels={'Title': item['title']})
    li_item.setArt({ 'icon': item['channelicon'] })
    starttime = getTimeFromString(item['starttime'], '%Y-%m-%d %H:%M:%S', utc_offset)
    endtime = getTimeFromString(item['endtime'], '%Y-%m-%d %H:%M:%S', utc_offset)
    li_item.setProperty('date', starttime.strftime('%d.%m'))
    li_item.setProperty('starttime', starttime.strftime('%H:%M'))
    li_item.setProperty('endtime', endtime.strftime('%H:%M'))
    li_item.setProperty('state', item['state'])
    li_item.setProperty('timerid', str(item['timerid']))
    li.append(('', li_item, False))

def parse_genre(li,item):
    li_item = xbmcgui.ListItem(item['label'])
    li_item.setInfo(type='Video', infoLabels={'Title': item['label'],
                                            'dbid': str(item['genreid']),
                                            'Path': item['file']})
    li_item.setArt(item['art'])
    li_item.setIconImage('DefaultGenre.png')

    li.append((item['file'], li_item, True))

def _get_cast(castData):
        listCast = []
        listCastAndRole = []
        for castmember in castData:
            listCast.append(castmember['name'])
            listCastAndRole.append((castmember['name'], castmember['role']))
        return [listCast, listCastAndRole]


def _get_first_item(item):
        if len(item) > 0:
            item = item[0]
        else:
            item = ''
        return item


def _get_joined_items(item):
        if len(item) > 0:
            item = ' / '.join(item)
        else:
            item = ''
        return item
