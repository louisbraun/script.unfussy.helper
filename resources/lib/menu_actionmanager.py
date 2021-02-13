#!/usr/bin/python
# coding: utf-8
import xbmc, xbmcgui, xbmcvfs
from resources.lib.helper import *

#######################################################################################
ADDON     = xbmcaddon.Addon()
#######################################################################################

class MenuActionManager:
    #############################################################
    #Action Types:
    # 0:  Link to Video Database
    # 1:  Link to TV Show Database
    # 2:  Link to Music Database
    # 3:  Link to Music Video Database
    # 4:  Live TV Window
    # 5:  Live Radio Window
    # 6:  Common Window
    # 7:  Execute Command
    # 8:  Link to Video Playlist
    # 9:  Link to Music Playlist
    # 10: Start Addon
    ##############################################################
    def __init__(self):

        self.thumbsizes = [
            ADDON.getLocalizedString(30294),
            ADDON.getLocalizedString(30293),
            ADDON.getLocalizedString(30292)
        ]

        self.actiontypes = [
            ADDON.getLocalizedString(30100),
            ADDON.getLocalizedString(30101),
            ADDON.getLocalizedString(30102),
            ADDON.getLocalizedString(30103),
            ADDON.getLocalizedString(30104),
            ADDON.getLocalizedString(30105),
            ADDON.getLocalizedString(30106),
            ADDON.getLocalizedString(30107),
            ADDON.getLocalizedString(30108),
            ADDON.getLocalizedString(30109),
            ADDON.getLocalizedString(30110)
        ]
        self.actionconstraints = [
            {
                'cond':     'Library.HasContent(movies)',
                'alt_path': 'ActivateWindow(Videos,sources://video/,return)'
            },
            {
                'cond':     'Library.HasContent(tvshows)',
                'alt_path': 'ActivateWindow(Videos,sources://video/,return)'
            },
            {
                'cond':     'Library.HasContent(music)',
                'alt_path': 'ActivateWindow(Music,sources://music/,return)'
            },
            {
                'cond':     'Library.HasContent(musicvideos)',
                'alt_path': 'ActivateWindow(Videos,sources://video/,return)'
            }
        ]
        self.actions = []
        # 0:  Links to Video Database
        self.actions.append([
            {
                'label': '342',
                'path': 'titles',
                'thumb': 'DefaultMovies.png'
            },
            {
                'label': '20382',
                'path': 'recentlyaddedmovies',
                'thumb': 'DefaultRecentlyAddedMovies.png'
            },
            {
                'label': '135',
                'path': 'genres',
                'thumb': 'DefaultGenre.png'
            },
            {
                'label': '652',
                'path': 'years',
                'thumb': 'DefaultYear.png'
            },
            {
                'label': '344',
                'path': 'actors',
                'thumb': 'DefaultActor.png'
            },
            {
                'label': '20348',
                'path': 'directors',
                'thumb': 'DefaultDirector.png'
            },
            {
                'label': '20388',
                'path': 'studios',
                'thumb': 'DefaultStudios.png'
            },
            {
                'label': '20434',
                'path': 'sets',
                'thumb': 'DefaultSets.png'
            },
            {
                'label': '20451',
                'path': 'countries',
                'thumb': 'DefaultCountry.png'
            },
            {
                'label': '20459',
                'path': 'tags',
                'thumb': 'DefaultTags.png'
            }
        ])
        # 1:  Links to TV Show Database
        self.actions.append([
            {
                'label': '20343',
                'path': 'titles',
                'thumb': 'DefaultTVShows.png'
            },
            {
                'label': '20382',
                'path': 'recentlyaddedepisodes',
                'thumb': 'DefaultRecentlyAddedEpisodes.png'
            },
            {
                'label': '575',
                'path': 'inprogresstvshows',
                'thumb': 'DefaultInProgressShows.png'
            },
            {
                'label': '135',
                'path': 'genres',
                'thumb': 'DefaultGenre.png'
            },
            {
                'label': '652',
                'path': 'years',
                'thumb': 'DefaultYear.png'
            },
            {
                'label': '344',
                'path': 'actors',
                'thumb': 'DefaultActor.png'
            },
            {
                'label': '20348',
                'path': 'directors',
                'thumb': 'DefaultDirector.png'
            },
            {
                'label': '20388',
                'path': 'studios',
                'thumb': 'DefaultStudios.png'
            },
            {
                'label': '20459',
                'path': 'tags',
                'thumb': 'DefaultTags.png'
            }
        ])
        # 2:  Links to Music Database
        self.actions.append([
            {
                'label': '133',
                'path': 'artists',
                'thumb': 'DefaultMusicArtists.png'
            },
            {
                'label': '135',
                'path': 'genres',
                'thumb': 'DefaultMusicGenres.png'
            },
            {
                'label': '132',
                'path': 'albums',
                'thumb': 'DefaultMusicAlbums.png'
            },
            {
                'label': '1050',
                'path': 'singles',
                'thumb': 'DefaultMusicSongs.png'
            },
            {
                'label': '134',
                'path': 'songs',
                'thumb': 'DefaultMusicSongs.png'
            },
            {
                'label': '652',
                'path': 'years',
                'thumb': 'DefaultMusicYears.png'
            },
            {
                'label': '517',
                'path': 'recentlyplayedalbums',
                'thumb': 'DefaultMusicRecentlyPlayed.png'
            },
            {
                'label': '359',
                'path': 'recentlyaddedalbums',
                'thumb': 'DefaultMusicRecentlyAdded.png'
            },
            {
                'label': '521',
                'path': 'compilations',
                'thumb': 'DefaultMusicCompilations.png'
            }
        ])
        # 3:  Links to Music Video Database
        self.actions.append([
            {
                'label': '20389',
                'path': 'titles',
                'thumb': 'DefaultMusicVideos.png'
            },
            {
                'label': '20382',
                'path': 'recentlyaddedmusicvideos',
                'thumb': 'DefaultRecentlyAddedMusicVideos.png'
            },
            {
                'label': '135',
                'path': 'genres',
                'thumb': 'DefaultGenre.png'
            },
            {
                'label': '652',
                'path': 'years',
                'thumb': 'DefaultYear.png'
            },
            {
                'label': '133',
                'path': 'artists',
                'thumb': 'DefaultMusicArtists.png'
            },
            {
                'label': '20348',
                'path': 'directors',
                'thumb': 'DefaultDirector.png'
            },
            {
                'label': '132',
                'path': 'albums',
                'thumb': 'DefaultMusicAlbums.png'
            },
            {
                'label': '20388',
                'path': 'studios',
                'thumb': 'DefaultStudios.png'
            },
            {
                'label': '20459',
                'path': 'tags',
                'thumb': 'DefaultTags.png'
            }
        ])
        # 4:  Live TV Windows
        self.actions.append([
            {
                'label': '19019',
                'path': 'TVChannels',
                'thumb': 'DefaultAddonPeripheral.png'
            },
            {
                'label': '19069',
                'path': 'TVGuide',
                'thumb': 'icons/pvr/epg.png'
            },
            {
                'label': '19017',
                'path': 'TVRecordings',
                'thumb': 'icons/pvr/recording_small.png'
            },
            {
                'label': '19040',
                'path': 'TVTimers',
                'thumb': 'icons/pvr/timer_small.png'
            },
            {
                'label': '19138',
                'path': 'TVTimerRules',
                'thumb': 'icons/pvr/timer-rule.png'
            },
            {
                'label': '137',
                'path': 'TVSearch',
                'thumb': 'DefaultAddonsSearch.png'
            }
        ])
        # 5:  Live Radio Windows
        self.actions.append([
            {
                'label': '19019',
                'path': 'RadioChannels',
                'thumb': 'DefaultAddonPeripheral.png'
            },
            {
                'label': '19069',
                'path': 'RadioGuide',
                'thumb': 'icons/pvr/epg.png'
            },
            {
                'label': '19017',
                'path': 'RadioRecordings',
                'thumb': 'icons/pvr/recording_small.png'
            },
            {
                'label': '19040',
                'path': 'RadioTimers',
                'thumb': 'icons/pvr/timer_small.png'
            },
            {
                'label': '19138',
                'path': 'RadioTimerRules',
                'thumb': 'icons/pvr/timer-rule.png'
            },
            {
                'label': '137',
                'path': 'RadioSearch',
                'thumb': 'DefaultAddonsSearch.png'
            }
        ])
        # 6:  Common Windows
        self.actions.append([
            {
                'label': '24001',
                'path': 'addonbrowser',
                'thumb': 'icons/mainmenu/addons.png'
            },
            {
                'label': '1',
                'path': 'Pictures',
                'thumb': 'icons/mainmenu/pictures.png'
            },
            {
                'label': '3',
                'path': 'Videos',
                'thumb': 'icons/mainmenu/videos.png'
            },
            {
                'label': '10134',
                'path': 'favourites',
                'thumb': 'icons/mainmenu/favourites.png'
            },
            {
                'label': '8',
                'path': 'Weather',
                'thumb': 'icons/mainmenu/weather.png'
            },
            {
                'label': ADDON.getLocalizedString(30289),
                'path': 'special://profile/playlists/video/',
                'thumb': 'defaultplaylist.png'
            },
            {
                'label': ADDON.getLocalizedString(30290),
                'path': 'special://profile/playlists/music/',
                'thumb': 'defaultplaylist.png'
            }
        ])
        # 7:  Execute Command
        self.actions.append([
            {
                'label': ADDON.getLocalizedString(30242),
                'path': 'PlayPvrTV',
                'thumb': 'icons/mainmenu/tv.png'
            },
            {
                'label': ADDON.getLocalizedString(30243),
                'path': 'PlayPvrRadio',
                'thumb': 'icons/mainmenu/radio.png'
            },
            {
                'label': ADDON.getLocalizedString(30244),
                'path': 'PlayDVD',
                'thumb': 'DefaultCdda.png'
            }
        ])
        # 8:  Link to Video Playlist
        # 9:  Link to Music Playlist
        self.playlists = {
            'video': [],
            'music': []
        }
        # 10: Start Addon
        self.addons = []

    def getActionType(self, index, with_index = True):
        if index == -1:
            return ADDON.getLocalizedString(30116)
        if with_index:
            return str(index+1) + '. ' + self.actiontypes[index]
        else:
            return self.actiontypes[index]

    def getActionName(self, action_type, action):
        if action == -1:
            return ADDON.getLocalizedString(30116)
        label = ''
        if action_type < 8:
            label = self.actions[action_type][action]['label']
            if label.isdigit():
                label = xbmc.getLocalizedString(int(label))
        elif action_type == 8 or action_type == 9:
            label = action[0:-4]
        elif action_type == 10:
            if len(self.addons) == 0:
                self.loadAddons()
            index = self.getAddonIndex(action)
            label = self.addons[index]['name']
        return label

    def getThumb(self, action_type, action):
        thumb = ''
        if action_type > -1 and action_type < 8:
            thumb = self.actions[action_type][action]['thumb']
        elif action_type == 8:
            thumb = 'icons/mainmenu/' + self.playlists['video'][action]['type'] + '.png'
        elif action_type == 9:
            thumb = 'icons/mainmenu/' + self.playlists['music'][action]['type'] + '.png'
        elif action_type == 10:
            thumb = self.addons[action]['thumbnail']
        return thumb

    def getOnClick(self, action_type, action):
        onclick = ''
        path = ''
        if action_type > -1 and action_type < 8:
            path = self.actions[action_type][action]['path']
        if action_type == 0:
            if not path.startswith('recentlyadded'):
                path = 'movies/' + path
            onclick = 'ActivateWindow(Videos,videodb://%s/,return)' % path
        elif action_type == 1:
            if not path.startswith('recentlyadded') and not path.startswith('inprogress'):
                path = 'tvshows/' + path
            onclick = 'ActivateWindow(Videos,videodb://%s/,return)' % path
        elif action_type == 2:
            onclick = 'ActivateWindow(Music,musicdb://%s/,return)' % path
        elif action_type == 3:
            if not path.startswith('recentlyadded'):
                path = 'musicvideos/' + path
            onclick = 'ActivateWindow(Videos,videodb://%s/,return)' % path
        elif action_type == 4 or action_type == 5:
            onclick = 'ActivateWindow(%s)' % path
        elif action_type == 6:
            if action < 5:
                onclick = 'ActivateWindow(%s)' % path
            elif action == 5:
                onclick = 'ActivateWindow(Videos,%s,return)' % path
            elif action == 6:
                onclick = 'ActivateWindow(Music,%s,return)' % path
        elif action_type == 7:
            onclick = 'Action(%s)' % path
        elif action_type == 8:
            onclick = 'ActivateWindow(Videos,special://profile/playlists/video/%s,return)' % action
        elif action_type == 9:
            onclick = 'ActivateWindow(Music,special://profile/playlists/music/%s,return)' % action
        elif action_type == 10:
            onclick = 'RunAddon(%s)' % action
        return onclick

    def getOnClickCond(self, action_type):
        if action_type < 0 or action_type > 3:
            return ''
        return self.actionconstraints[action_type]['cond']

    def getOnClickAlt(self, action_type):
        if action_type < 0 or action_type > 3:
            return ''
        return self.actionconstraints[action_type]['alt_path']

    def getActionItems(self, action_type):
        if action_type == -1:
            return []
        action_items = []
        if action_type < 8:
            for item in self.actions[action_type]:
                label = item['label']
                if label.isdigit():
                    label = xbmc.getLocalizedString(int(label))
                action_items.append(self.getActionListItem(label, item['thumb']))
        elif action_type == 8:
            #Video Playlists
            if len(self.playlists['video']) == 0:
                self.loadPlaylist('video')
            for playlist in self.playlists['video']:
                thumb = 'icons/mainmenu/' + playlist['type'] + '.png'
                action_items.append(self.getActionListItem(playlist['name'], thumb))
        elif action_type == 9:
            #Audio Playlists
            if len(self.playlists['music']) == 0:
                self.loadPlaylist('music')
            for playlist in self.playlists['music']:
                thumb = 'icons/mainmenu/' + playlist['type'] + '.png'
                action_items.append(self.getActionListItem(playlist['name'], thumb))
        elif action_type == 10:
            #Addons
            if len(self.addons) == 0:
                self.loadAddons()
            for addon in self.addons:
                action_items.append(self.getActionListItem(addon['name'], addon['thumbnail']))
        return action_items

    def getActionListItem(self, label, thumb):
        listitem = xbmcgui.ListItem(label=label)
        listitem.setArt( { 'thumb': thumb } )
        return listitem

    def numActions(self):
        return len(self.actiontypes)

    def loadAddons(self):
        addon_types = [
            'xbmc.addon.video',
            'xbmc.addon.audio',
            'xbmc.addon.image'
        ]
        for addon_type in addon_types:
            query_addons = json_call('Addons.GetAddons',
                                      properties=['author', 'name', 'thumbnail'],
                                      params={
                                        'type': addon_type
                                      })
            try:
                addons = query_addons['result']['addons']
                for addon in addons:
                    self.addons.append(addon)
            except Exception:
                return

    def getAddonId(self, index):
        return self.addons[index]['addonid']

    def getAddonIndex(self, addon_id):
        i = 0
        for addon in self.addons:
            if addon['addonid'] == addon_id:
                return i
            i = i+1
        return 0

    def loadPlaylist(self, playlist_type):
        path_playlists = xbmcvfs.translatePath(  'special://' + playlist_type + 'playlists' ).decode("utf-8")
        dirs, files = xbmcvfs.listdir(path_playlists)
        playlists = []
        exts = ['.xsp', '.m3u']
        for playlist in files:
            playlist_ext = ''
            for ext in exts:
                if playlist.find(ext) > -1:
                    playlist_ext = ext[1:4]
            playlist = {
                'name': playlist[0:-4],
                'type': playlist_ext
            }
            playlists.append(playlist)
        self.playlists[playlist_type] = playlists

    def getPlaylistId(self, action_type, playlist_index):
        playlists = self.playlists['video']
        if action_type == 9:
            playlists = self.playlists['music']
        return playlists[playlist_index]['name'] + '.' + playlists[playlist_index]['type']