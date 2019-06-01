#!/usr/bin/python
# coding: utf-8
import xbmc, xbmcgui, xbmcvfs
from resources.lib.helper import *

#######################################################################################
ADDON     = xbmcaddon.Addon()
#######################################################################################

class WidgetManager:
    #############################################################
    # Categories:
    # 0:  Live TV Widget
    #     Type 0: LiveTV
    #     Type 1: Recordings
    #     Type 2: GTO
    #     Type 4: Running At
    #     Type 5: Timers
    # 1:  Movie Widget
    #     Type 0: Inprogress Movies
    #     Type 1: Recently added Movies
    #     Type 2: Movie Playlist
    # 2:  TVShow Widget
    #     Type 0: Recently added TVShows
    #     Type 1: Inprogress TVShows
    #     Type 2: Series Playlist
    #     Type 3: Episode Playlist
    # 3:  Music Widget
    #     Type 0: unplayed albums
    #     Type 1: mostplayed albums
    #     Type 2: random albums
    #     Type 3: music playlist - songs
    #     Type 4: music playlist - albums
    #     Type 5: music playlist - artists
    # 4:  Music Video Widget
    #     Type 0: recent unwatched musicvideos
    #     Type 1: random_musicvideos
    #     Type 2: musicvideo playlist
    # 5:  Addon Widget
    #     Type 0: addons
    #     Type 1: addon path
    #     Type 2: favorites
    # 6:  Weather Widget
    #     Type 0: weather hourly
    #     Type 1: weather daily
    ##############################################################

    def __init__(self):
        self.categories = [
            ADDON.getLocalizedString(30200),
            ADDON.getLocalizedString(30201),
            ADDON.getLocalizedString(30202),
            ADDON.getLocalizedString(30203),
            ADDON.getLocalizedString(30204),
            ADDON.getLocalizedString(30205),
            ADDON.getLocalizedString(30207)
        ]

        self.types = []
        # 0:  Live TV Widgets
        self.types.append(
            [
                {
                    'header': ADDON.getLocalizedString(30208),
                    'headeraction': 'Action(PlayPvrTV)',
                    'description': ADDON.getLocalizedString(30209),
                    'path': 'pvr://channels/tv/*',
                    'sortby': '',
                    'sortorder': 'descending',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': ADDON.getLocalizedString(30266),
                            'widget': 'livetv_small',
                            'width': 260,
                            'height': 250
                        },
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30267),
                            'widget': 'livetv_large',
                            'width': 260,
                            'height': 425
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30210),
                    'headeraction': 'ActivateWindow(tvrecordings)',
                    'description': ADDON.getLocalizedString(30211),
                    'path': 'pvr://recordings/tv/active?view=flat',
                    'setlimit': True,
                    'sortby': 'date',
                    'sortorder': 'descending',
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': ADDON.getLocalizedString(30266),
                            'widget': 'recordings_small',
                            'width': 260,
                            'height': 250
                        },
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30266),
                            'widget': 'recordings_large',
                            'width': 260,
                            'height': 425
                        }
                    ]
                },
                {
                    'header': 'German Telecast Offers',
                    'headeraction': 'ActivateWindow(tvguide)',
                    'description': ADDON.getLocalizedString(30268),
                    'setlimit': False,
                    'path': 'plugin://script.service.gto?action=getcontent&ts=$INFO[Window(Home).Property(GTO.timestamp)]',
                    'onclick': 'RunScript(script.service.gto,action=infopopup&blob=$INFO[ListItem.Property(BlobID)])',
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30265),
                            'desc': '',
                            'widget': 'gto',
                            'width': 366,
                            'height': 250
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30224),
                    'headeraction': 'ActivateWindow(tvguide)',
                    'description': ADDON.getLocalizedString(30225),
                    'setlimit': False,
                    'path': 'plugin://script.unfussy.helper/?info=getrunningat&reload=$INFO[Window(Home).Property(widgetreload-runningat)]',
                    'onclick': 'RunScript(script.unfussy.helper,action=info_runningat&bc_id=$INFO[ListItem.Property(broadcastid)]&c_id=$INFO[ListItem.Property(channelid)])',
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': ADDON.getLocalizedString(30266),
                            'widget': 'tv_runningat_small',
                            'width': 260,
                            'height': 250
                        },
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30226),
                    'headeraction': 'ActivateWindow(tvtimers)',
                    'description': ADDON.getLocalizedString(30227),
                    'path': 'plugin://script.unfussy.helper/?info=gettimers&reload=$INFO[Window(Home).Property(widgetreload-timers)]',
                    'onclick': 'RunScript(script.unfussy.helper,action=info_timer&timer_id=$INFO[ListItem.Property(timerid)])',
                    'setlimit': True,
                    'sortby': 'date',
                    'sortorder': 'descending',
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': ADDON.getLocalizedString(30266),
                            'widget': 'tv_runningat_small',
                            'width': 260,
                            'height': 250
                        }
                    ]
                }
            ]
        )
        # 1:  Movie Widgets
        self.types.append(
            [
                {
                    'header': ADDON.getLocalizedString(30212),
                    'headeraction': 'ActivateWindow(Videos,videodb://movies/titles/,return)',
                    'description': ADDON.getLocalizedString(30213),
                    'path': 'special://skin/playlists/inprogress_movies.xsp',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30269),
                            'widget': 'movies',
                            'width': 260,
                            'height': 425
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30214),
                    'headeraction': 'ActivateWindow(Videos,videodb://recentlyaddedmovies/,return)',
                    'description': ADDON.getLocalizedString(30215),
                    'path': 'special://skin/playlists/recent_unwatched_movies.xsp',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30269),
                            'widget': 'movies',
                            'width': 260,
                            'height': 425
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30247),
                    'description': ADDON.getLocalizedString(30248),
                    'path': 'special://masterprofile/playlists/video',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30269),
                            'widget': 'movies',
                            'width': 260,
                            'height': 425
                        }
                    ]
                }
            ]
        )
        # 2:  TV Show Widgets
        self.types.append(
            [
                {
                    'header': ADDON.getLocalizedString(30216),
                    'headeraction': 'ActivateWindow(Videos,videodb://recentlyaddedepisodes/,return)',
                    'description': ADDON.getLocalizedString(30217),
                    'path': 'special://skin/playlists/recent_unwatched_episodes.xsp',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30265),
                            'desc': ADDON.getLocalizedString(30270),
                            'widget': 'episode',
                            'width': 541,
                            'height': 250
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30218),
                    'headeraction': 'ActivateWindow(Videos,videodb://inprogresstvshows/,return)',
                    'description': ADDON.getLocalizedString(30219),
                    'path': 'plugin://script.unfussy.helper/?info=getnextepisodes&reload=$INFO[Window(Home).Property(widgetreload-nextepisodes)]',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30265),
                            'desc': ADDON.getLocalizedString(30270),
                            'widget': 'episode',
                            'width': 541,
                            'height': 250
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30251),
                    'description': ADDON.getLocalizedString(30252),
                    'path': 'special://masterprofile/playlists/video',
                    'onclick': 'ActivateWindow(Videos,videodb://tvshows/titles/$INFO[ListItem.DBID]/,return)',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30271),
                            'widget': 'movies',
                            'width': 260,
                            'height': 425
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30253),
                    'description': ADDON.getLocalizedString(30254),
                    'path': 'special://masterprofile/playlists/video',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30265),
                            'desc': ADDON.getLocalizedString(30270),
                            'widget': 'episode',
                            'width': 541,
                            'height': 250
                        }
                    ]
                }
            ]
        )
        # 3:  Music Widget
        self.types.append(
            [
                {
                    'header': ADDON.getLocalizedString(30238),
                    'headeraction': 'ActivateWindow(Music,musicdb://recentlyaddedalbums/,return)',
                    'description': ADDON.getLocalizedString(30239),
                    'path': 'special://skin/playlists/unplayed_albums.xsp',
                    'onclick': 'ActivateWindow(Music,musicdb://albums/$INFO[ListItem.DBID]/,return)',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'musicalbums',
                            'width': 260,
                            'height': 300
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30240),
                    'headeraction': 'ActivateWindow(Music,musicdb://artists/,return)',
                    'description': ADDON.getLocalizedString(30241),
                    'path': 'special://skin/playlists/mostplayed_albums.xsp',
                    'onclick': 'ActivateWindow(Music,musicdb://albums/$INFO[ListItem.DBID]/,return)',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'musicalbums',
                            'width': 260,
                            'height': 300
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30245),
                    'headeraction': 'ActivateWindow(Music,musicdb://artists/,return)',
                    'description': ADDON.getLocalizedString(30246),
                    'path': 'special://skin/playlists/random_albums.xsp',
                    'onclick': 'ActivateWindow(Music,musicdb://albums/$INFO[ListItem.DBID]/,return)',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'musicalbums',
                            'width': 260,
                            'height': 300
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30257),
                    'description': ADDON.getLocalizedString(30258),
                    'path': 'special://masterprofile/playlists/music',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'musicsongs',
                            'width': 260,
                            'height': 300
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30259),
                    'description': ADDON.getLocalizedString(30260),
                    'path': 'special://masterprofile/playlists/music',
                    'onclick': 'ActivateWindow(Music,musicdb://albums/$INFO[ListItem.DBID]/,return)',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'musicalbums',
                            'width': 260,
                            'height': 300
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30261),
                    'description': ADDON.getLocalizedString(30262),
                    'path': 'special://masterprofile/playlists/music',
                    'onclick': 'ActivateWindow(Music,musicdb://artists/$INFO[ListItem.DBID]/,return)',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'musicartists',
                            'width': 260,
                            'height': 300
                        }
                    ]
                }
            ]
        )
        # 4:  Music Video Widget
        self.types.append(
            [
                {
                    'header': ADDON.getLocalizedString(30220),
                    'description': ADDON.getLocalizedString(30221),
                    'path': 'special://skin/playlists/recent_unwatched_musicvideos.xsp',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30272),
                            'widget': 'movies',
                            'width': 260,
                            'height': 425
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30222),
                    'description': ADDON.getLocalizedString(30223),
                    'path': 'special://skin/playlists/random_musicvideos.xsp',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30272),
                            'widget': 'movies',
                            'width': 260,
                            'height': 425
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30255),
                    'description': ADDON.getLocalizedString(30256),
                    'path': 'special://masterprofile/playlists/video',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': ADDON.getLocalizedString(30272),
                            'widget': 'movies',
                            'width': 260,
                            'height': 425
                        }
                    ]
                }
            ]
        )
        # 5:  Addon Widget
        self.types.append(
            [
                {
                    'header': ADDON.getLocalizedString(30228),
                    'headeraction': 'ActivateWindow(addonbrowser)',
                    'description': ADDON.getLocalizedString(30229),
                    'path': 'addons',
                    'static_content': True,
                    'setlimit': False,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'favorites',
                            'width': 260,
                            'height': 250
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30275),
                    'description': ADDON.getLocalizedString(30276),
                    'path': '',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30265),
                            'desc': '',
                            'widget': 'addonpath_thumb',
                            'width': 260,
                            'height': 260
                        },
                        {
                            'label': ADDON.getLocalizedString(30282),
                            'desc': '',
                            'widget': 'addonpath_thumb_large',
                            'width': 310,
                            'height': 300
                        },
                        {
                            'label': ADDON.getLocalizedString(30264),
                            'desc': '',
                            'widget': 'addonpath_poster',
                            'width': 260,
                            'height': 425
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30230),
                    'headeraction': 'ActivateWindow(favourites)',
                    'description': ADDON.getLocalizedString(30231),
                    'path': 'favourites://',
                    'setlimit': True,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'favorites',
                            'width': 260,
                            'height': 250
                        }
                    ]
                }
            ]
        )
        # 6:  Weather Widget
        self.types.append(
            [
                {
                    'header': ADDON.getLocalizedString(30234),
                    'headeraction': 'ActivateWindow(Weather)',
                    'description': ADDON.getLocalizedString(30235),
                    'path': 'weather_hourly_items',
                    'static_content': True,
                    'setlimit': False,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'weather_listitem',
                            'width': 260,
                            'height': 300
                        }
                    ]
                },
                {
                    'header': ADDON.getLocalizedString(30236),
                    'headeraction': 'ActivateWindow(Weather)',
                    'description': ADDON.getLocalizedString(30237),
                    'path': 'weather_daily_items',
                    'static_content': True,
                    'setlimit': False,
                    'styles': [
                        {
                            'label': ADDON.getLocalizedString(30263),
                            'desc': '',
                            'widget': 'weather_listitem',
                            'width': 260,
                            'height': 300
                        }
                    ]
                }            
            ]
        )
    
    def isAddonWidget(self, cat, type):
        if cat == 5 and type == 0:
            return True
        return False

    def isOrderableWidget(self, cat, type):
        if cat == 0 and type == 0:
            return True
        return False
    
    def staticContent(self, cat, type):
        if 'static_content' in self.types[cat][type]:
            return True
        return False

    def getCategory(self, cat, numbered = False):
        if cat == -1:
            return ADDON.getLocalizedString(30116)
        if not numbered:
            return self.categories[cat]
        return str(cat+1) + '. ' + self.categories[cat]

    def numCategories(self):
        return len(self.categories)

    def getType(self, cat, type):
        if cat < 0 or type < 0:
            return ADDON.getLocalizedString(30116)
        return self.types[cat][type]['header']

    def getTypeDesc(self, cat, type):
        if cat < 0 or type < 0:
            return ''
        return self.types[cat][type]['description']

    def getWidget(self, cat, type, style):
        if cat < 0 or type < 0:
            return ADDON.getLocalizedString(30116)
        widget = self.getType(cat, type)
        style_ext = self.types[cat][type]['styles'][style]['label']
        if style_ext != '':
            widget += ' (' + style_ext + ')'
        return widget

    def getWidgetIndex(self, cat, type, style):
        if cat == -1 or type == -1 or style == -1:
            return -1
        index = 0
        current_type = 0
        for widget in self.types[cat]:
            current_style = 0
            for styles in widget['styles']:
                if type == current_type and style == current_style:
                    return index
                current_style += 1
                index += 1
            current_type += 1
        return -1

    def getWidgetItems(self, cat):
        if cat == -1:
            return []
        widget_items = []
        for widget in self.types[cat]:
            for style in widget['styles']:
                label = widget['header']
                if style['label'] != '':
                    label += ' (' + style['label'] + ', ' + str(style['width']) + 'x' + str(style['height']) + 'px)'
                else:
                    label += ' (' + str(style['width']) + 'x' + str(style['height']) + 'px)'
                label2 = widget['description']
                if style['desc'] != '':
                    label2 += ' (' + style['desc'] + ')'
                widget_items.append(xbmcgui.ListItem(label=label, label2=label2))
        return widget_items

    def getWidgetDetails(self, cat, widget_new):
        item = 0
        type = 0
        for widget in self.types[cat]:
            style = 0
            for st in widget['styles']:
                if widget_new == item:
                    return (type, style)
                style += 1
                item += 1
            type += 1


    def getSize(self, cat, type, style):
        if cat < 0 or type < 0:
            return ''
        width  = self.types[cat][type]['styles'][style]['width']
        height = self.types[cat][type]['styles'][style]['height']
        return str(width) + 'x' + str(height) + 'px'

    def getDesc(self, cat, type):
        if cat < 0 or type < 0:
            return ''
        return self.types[cat][type]['description']

    def getStyleDesc(self, cat, type, style):
        if cat < 0 or type < 0:
            return ''
        return self.types[cat][type]['styles'][style]['desc']

    def getStyleWidget(self, cat, type, style):
        if cat < 0 or type < 0:
            return ''
        return self.types[cat][type]['styles'][style]['widget']

    def getWidth(self, cat, type, style):
        if cat < 0 or type < 0:
            return 0
        return self.types[cat][type]['styles'][style]['width']

    def getHeight(self, cat, type, style):
        if cat < 0 or type < 0:
            return 0
        return self.types[cat][type]['styles'][style]['height']

    def getPath(self, cat, type):
        if cat < 0 or type < 0:
            return ''
        return self.types[cat][type]['path']

    def getHeaderAction(self, cat, type):
        if cat < 0 or type < 0:
            return ''
        if 'headeraction' not in self.types[cat][type]:
            return ''
        return self.types[cat][type]['headeraction']

    def getLayout(self, cat, type, style):
        if cat < 0 or type < 0:
            return ''
        width = self.types[cat][type]['styles'][style]['width']
        height = self.types[cat][type]['styles'][style]['height']
        layout = ''
        if width == height:
            layout = 'square'
        elif width > height:
            layout = 'landscape'
        elif height > width:
            layout = 'portrait'
        return layout

    def hasOnClick(self, cat, type):
        if 'onclick' in self.types[cat][type]:
            return True
        return False

    def getOnClick(self, cat, type):
        return self.types[cat][type]['onclick']

    def getSortby(self, cat, type):
        if 'sortby' in self.types[cat][type]:
            return self.types[cat][type]['sortby']
        return ''

    def getSortbyDynamic(self, sortby):
        if sortby == 0:
            return 'lastplayed'
        return ''

    def getSortorder(self, cat, type):
        if 'sortorder' in self.types[cat][type]:
            return self.types[cat][type]['sortorder']
        return ''

    def setLimit(self, cat, type):
        if cat == -1:
            return True
        return self.types[cat][type]['setlimit']

    def hasTarget(self, cat, type):
        if 'target' in self.types[cat][type]:
            return True
        return False

    def getTarget(self, cat, type):
        return self.types[cat][type]['target']
