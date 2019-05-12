#!/usr/bin/python
# coding: utf-8
import xbmc, xbmcgui, xbmcvfs
import xml.etree.ElementTree as xml
from resources.lib.helper import *
from resources.lib.widgets_datastore import WidgetsDataStore
from resources.lib.widget_manager import WidgetManager
#######################################################################################

ADDON               = xbmcaddon.Addon()

#######################################################################################

class Gui_Widgets( xbmcgui.WindowXMLDialog ):
    
    def __init__( self, *args, **kwargs ):
        self.wm = WidgetManager()
        self.widgets = WidgetsDataStore(self.wm)
        if not self.widgets.loadWidgets():
            log("fatal error loading widgets structure")
            self.close()
    
    def onInit( self ):
        #position in menu
        self.index_widget = -1
        #controls
        self.control_widgets = self.getControl(100)
        self.label_header = self.getControl(302)
        self.button_limit = self.getControl(306)
        self.radio_visible = self.getControl(307)
        self.label_category = self.getControl(402)
        self.label_widget = self.getControl(502)
        self.button_widget = self.getControl(503)
        self.channel_selector = ChannelSelector(self)
        self.channel_selector.setVisible(False)
        self.addon_selector = AddonSelector(self)
        self.addon_selector.setVisible(False)
        self.playlist_selector = PlaylistSelector(self)
        self.playlist_selector.setVisible(False)
        #init
        self.renderWidgets()
        self.setFocus(self.control_widgets)
        self.setWidgetIndex()
        self.setDetail()

    def onClick(self, control_id):
        self.setWidgetIndex()
        if control_id == 201:
            self.moveItem(up=True)
        elif control_id == 203:
            self.moveItem(up=False)
        elif control_id == 221:
            self.newElement()
        elif control_id == 223:
            self.deleteElement()
        elif control_id == 224:
            self.reset2Default()
        elif control_id == 303:
            self.editHeader()
        elif control_id == 306:
            self.editLimit()
        elif control_id == 307:
            self.setVisibility()
        elif control_id == 403:
            self.editCategory(next=True)
        elif control_id == 404:
            self.editCategory(next=False)
        elif control_id == 503:
            self.editWidget()
        elif control_id == 604:
            self.editChannels()
        elif control_id == 608:
            self.editPointInTime()
        elif control_id == 704:
            self.editAddons()
        elif control_id == 707:
            self.editAddonOrder(next=False)
        elif control_id == 708:
            self.editAddonOrder(next=True)
        elif control_id == 804:
            self.editPlaylist()

    def onAction(self, action):
        self.setWidgetIndex()
        if action.getId() == 92:
            #key back
            self.widgets.saveWidgets()
            self.widgets.setSkinStrings()
            self.close()
        elif action.getId() == 3 or action.getId() == 4:
            #key up or down
            if self.getFocusId() == 100:
                self.setDetail()

    def hasChanged(self):
        return self.widgets.changed

    def renderWidgets(self):
        self.control_widgets.reset()
        for widget in self.widgets.widgets:
            listitem = self.createListItem(widget)
            self.control_widgets.addItem(listitem)

    def reloadWidgets(self, focus=-1):
        self.renderWidgets()
        if focus > -1:
            self.control_widgets.selectItem(focus)
        else:
            self.control_widgets.selectItem(self.index_widget)

    def createListItem(self, widget):
        listitem = xbmcgui.ListItem(widget['header'])
        if widget['header'].isdigit():
            listitem.setLabel(xbmc.getLocalizedString(int(widget['header'])))
        listitem.setArt({ 'thumb': 'icons/settings/widget.png' })
        if widget['visible']:
            listitem.setProperty('is_visible', 'true')
        else:
            listitem.setProperty('is_visible', 'false')
        listitem.setProperty('category', self.wm.getCategory(widget['category']))
        listitem.setProperty('type', self.wm.getType(widget['category'], widget['type']))
        listitem.setProperty('desc', self.wm.getDesc(widget['category'], widget['type']))
        listitem.setProperty('styledesc', self.wm.getStyleDesc(widget['category'], widget['type'], widget['style']))
        listitem.setProperty('size', self.wm.getSize(widget['category'], widget['type'], widget['style']))
        listitem.setProperty('layout', self.wm.getLayout(widget['category'], widget['type'], widget['style']))
        if widget['limit'] > 0:
            listitem.setProperty('limit', str(widget['limit']))
        else:
            listitem.setProperty('limit', '')
        return listitem

    def setWidgetIndex(self):
        self.index_widget = self.control_widgets.getSelectedPosition()

    #Actions

    def setDetail(self):
        log("index_widget: %s" % self.index_widget)
        category = self.widgets.getValue(self.index_widget, 'category')
        type = self.widgets.getValue(self.index_widget, 'type')
        style = self.widgets.getValue(self.index_widget, 'style')
        #limit
        if not self.wm.setLimit(category, type):
            self.button_limit.setVisible(False)
        elif not self.button_limit.isVisible():
            self.button_limit.setVisible(True)
        #radio "is visible"
        is_visible = self.widgets.getValue(self.index_widget, 'visible')
        self.radio_visible.setSelected(is_visible)        
        #label "category"
        self.label_category.setLabel(self.wm.getCategory(category, True))
        #label "widget"
        self.label_widget.setLabel(self.wm.getWidget(category, type, style))
        if category == -1:
            self.button_widget.setEnabled(False)
        else:
            self.button_widget.setEnabled(True)

        if self.channel_selector.show(category, type):
            self.channel_selector.setVisible(True)
            self.channel_selector.setDetail(self.widgets.getValue(self.index_widget, 'channels'), self.widgets.getValue(self.index_widget, 'pointintime'))
        elif self.channel_selector.hide(category, type):
            self.channel_selector.setVisible(False)

        if self.addon_selector.show(category, type):
            self.addon_selector.setVisible(True)
            self.addon_selector.setDetail(self.widgets.getValue(self.index_widget, 'addons'))
        elif self.addon_selector.hide(category, type):
            self.addon_selector.setVisible(False)

        if self.playlist_selector.show(category, type):
            self.playlist_selector.setVisible(True)
            self.playlist_selector.setDetail(self.widgets.getValue(self.index_widget, 'playlist'))
        elif self.playlist_selector.hide(category, type):
            self.playlist_selector.setVisible(False)

    def moveItem(self, up=False):
        pos_new = self.widgets.switchElements(self.index_widget, up)
        self.reloadWidgets(pos_new)

    def newElement(self):
        self.widgets.newElement(self.index_widget)
        self.index_widget += 1
        self.reloadWidgets()
        self.setDetail()
        self.setFocusId(303)

    def deleteElement(self):
        dialog = xbmcgui.Dialog()
        header = ADDON.getLocalizedString(30112)
        content = ADDON.getLocalizedString(30113) + '?\n"' + self.widgets.getHeader(self.index_widget) + '"'
        ok = dialog.yesno(header, content)
        if not ok:
            return
        self.widgets.deleteElement(self.index_widget)
        self.reloadWidgets()
        self.setDetail()
    
    def reset2Default(self):
        dialog = xbmcgui.Dialog()
        header = ADDON.getLocalizedString(30112)
        content = ADDON.getLocalizedString(30117)
        ok = dialog.yesno(header, content)
        if not ok:
            return
        self.widgets.reset()
        self.index_widget = 0
        self.reloadWidgets()
        self.setDetail()

    def editHeader(self):
        header = self.widgets.getValue(self.index_widget, 'header')
        if header.isdigit():
            header = xbmc.getLocalizedString(int(header))
        dialog = xbmcgui.Dialog()
        new_header = dialog.input(ADDON.getLocalizedString(30030), type=xbmcgui.INPUT_ALPHANUM, defaultt=header)
        if new_header == '': return
        self.widgets.setValue(self.index_widget, 'header', new_header)
        self.reloadWidgets()

    def editLimit(self):
        limit = str(self.widgets.getValue(self.index_widget, 'limit'))
        dialog = xbmcgui.Dialog()
        new_limit = dialog.numeric(0, ADDON.getLocalizedString(30019), limit)
        if new_limit == '': return
        self.widgets.setValue(self.index_widget, 'limit', int(new_limit))
        self.reloadWidgets()

    def setVisibility(self):
        selected = self.radio_visible.isSelected()
        self.widgets.setValue(self.index_widget, 'visible', selected)
        self.reloadWidgets()

    def editCategory(self, next=False):
        new_cat = self.widgets.getValue(self.index_widget, 'category')
        if next:
            new_cat = (new_cat+1) % self.wm.numCategories()
        else:
            new_cat = new_cat - 1
            if new_cat < 0:
                new_cat = self.wm.numCategories() - 1
        self.widgets.setValue(self.index_widget, 'category', new_cat)
        self.widgets.setValue(self.index_widget, 'limit', 20)
        self.widgets.setValue(self.index_widget, 'type', -1)
        self.widgets.setValue(self.index_widget, 'style', -1)
        self.widgets.setValue(self.index_widget, 'channels', [])
        self.widgets.setValue(self.index_widget, 'pointintime', '20:15')
        self.widgets.setValue(self.index_widget, 'addons', [])
        self.widgets.setValue(self.index_widget, 'playlist', '')
        self.button_widget.setEnabled(True)
        self.setDetail()

    def editWidget(self):
        category = self.widgets.getValue(self.index_widget, 'category')
        cat_name = self.wm.getCategory(category)
        type = int(self.widgets.getValue(self.index_widget, 'type'))
        style = int(self.widgets.getValue(self.index_widget, 'style'))
        index_selected = self.wm.getWidgetIndex(category, type, style)
        type_items = self.wm.getWidgetItems(category)
        dialog = xbmcgui.Dialog()
        widget_new = dialog.select(cat_name, type_items, preselect=index_selected, useDetails=True)
        if widget_new == -1:
            return
        widget_new = self.wm.getWidgetDetails(category, widget_new)
        new_type = widget_new[0]
        new_style = widget_new[1]
        self.widgets.setValue(self.index_widget, 'type', new_type)
        self.widgets.setValue(self.index_widget, 'style', new_style)
        self.widgets.setValue(self.index_widget, 'header', self.wm.getType(category, new_type))
        if not self.wm.setLimit(category, new_type):
            self.widgets.setValue(self.index_widget, 'limit', -1)
        if self.channel_selector.show(category, new_type):
            self.widgets.addArray(self.index_widget, 'channels')
            self.widgets.addValue(self.index_widget, 'pointintime', '20:15')
        elif self.addon_selector.show(category, new_type):
            self.widgets.addArray(self.index_widget, 'addons')
        elif self.playlist_selector.show(category, new_type):
            self.widgets.addValue(self.index_widget, 'playlist', '')
        self.reloadWidgets()
        self.setDetail()

    def editChannels(self):
        channels_new = self.channel_selector.showSelector(self.widgets.getValue(self.index_widget, 'channels'))
        self.widgets.setValue(self.index_widget, 'channels', channels_new)
        self.setDetail()

    def editPointInTime(self):
        time_new = self.channel_selector.showTimeSelector(self.widgets.getValue(self.index_widget, 'pointintime'))
        self.widgets.setValue(self.index_widget, 'pointintime', time_new)
        self.setDetail()

    def editAddons(self):
        addons_new = self.addon_selector.showSelector(self.widgets.getValue(self.index_widget, 'addons'))
        self.widgets.setValue(self.index_widget, 'addons', addons_new)
        self.setDetail()

    def editAddonOrder(self, next=False):
        self.addon_selector.editOrder(next)
        self.widgets.hasChanged()

    def editPlaylist(self):
        pl_selected = self.widgets.getValue(self.index_widget, 'playlist')
        category = self.widgets.getValue(self.index_widget, 'category')
        type = self.widgets.getValue(self.index_widget, 'type')
        playlist_new = self.playlist_selector.showSelector(category, type, pl_selected)
        if playlist_new == '':
            return
        self.widgets.setValue(self.index_widget, 'playlist', playlist_new)
        self.setDetail()

############################################################################
# ChannelSelector
############################################################################
class ChannelSelector:

    def __init__( self, window ):
        self.label_channels = window.getControl(602)
        self.label_channels_selected = window.getControl(603)
        self.button_select_channels = window.getControl(604)
        self.label_time = window.getControl(606)
        self.label_time_selected = window.getControl(607)
        self.button_select_time = window.getControl(608)

    def setVisible( self, show ):
        self.label_channels.setVisible(show)
        self.label_channels_selected.setVisible(show)
        self.button_select_channels.setVisible(show)
        self.label_time.setVisible(show)
        self.label_time_selected.setVisible(show)
        self.button_select_time.setVisible(show)

    def show( self, cat, type ):
        if cat == 0 and type == 3:
            return True
        return False

    def hide( self, cat, type ):
        if self.label_channels.isVisible() and not(cat == 0 and type == 3):
            return True
        return False

    def setDetail(self, channels, point_in_time):
        num_channels = len(channels)
        self.label_channels_selected.setLabel(str(num_channels))
        if point_in_time == '':
            point_in_time = ADDON.getLocalizedString(30116)
        self.label_time_selected.setLabel(point_in_time)
        

    def showSelector(self, channel_ids):
        channels_list = self.loadChannels()
        channel_listitems = self.getListitems(channels_list)
        channels_selected = self.getChannelIndexes(channels_list, channel_ids)
        dialog = xbmcgui.Dialog()
        channels_new = dialog.multiselect(ADDON.getLocalizedString(30035), channel_listitems, preselect=channels_selected, useDetails=True)
        channel_ids = self.getChannelIds(channels_list, channels_new)
        return channel_ids

    def showTimeSelector( self, point_in_time ):
        if point_in_time == '':
            point_in_time = '00:00'
        dialog = xbmcgui.Dialog()
        time_new = dialog.numeric(2, ADDON.getLocalizedString(30037), defaultt=point_in_time)
        return time_new

    def loadChannels(self):
        query = json_call('PVR.GetChannels',
                    properties=['icon', 'channelnumber'],
                    params={'channelgroupid': 'alltv'}
                )
        try:
            channels = query['result']['channels']
        except Exception:
            return []
        return channels

    def getListitems(self, channels):
        items = []
        for channel in channels:
            label = str(channel['channelnumber']) + '. ' + channel['label']
            listitem = xbmcgui.ListItem(label)
            listitem.setArt({ 'thumb': channel['icon'] })
            items.append(listitem)
        return items

    def getChannelIds(self, channels, channels_new):
        channel_ids = []
        for channel_new in channels_new:
            channel_ids.append(channels[channel_new]['channelid'])
        return channel_ids

    def getChannelIndexes(self, channels, channel_ids):
        channel_indexes = []
        for channel_id in channel_ids:
            i = 0
            for channel in channels:
                if channel['channelid'] == channel_id:
                    channel_indexes.append(i)
                    break
                i += 1
        return channel_indexes

############################################################################
# AddonSelector
############################################################################
class AddonSelector:

    def __init__( self, window ):
        self.label_addons = window.getControl(702)
        self.label_addons_selected = window.getControl(703)
        self.button_select_addons = window.getControl(704)
        self.list_addons = window.getControl(705)
        self.button_addon_left = window.getControl(707)
        self.button_addon_right = window.getControl(708)

    def setVisible( self, show ):
        self.label_addons.setVisible(show)
        self.label_addons_selected.setVisible(show)
        self.button_select_addons.setVisible(show)
        self.list_addons.setVisible(show)
        self.button_addon_left.setVisible(show)
        self.button_addon_right.setVisible(show)

    def show( self, cat, type ):
        if cat == 5 and type == 0:
            return True
        return False

    def hide( self, cat, type ):
        if self.label_addons.isVisible() and not(cat == 5 and type == 0):
            return True
        return False

    def setDetail(self, addons):
        self.addons = addons
        self.label_addons_selected.setLabel(str(len(addons)))
        self.renderAddonList()

    def showSelector(self, addons):
        addons_list = self.loadAddons()
        if len(addons_list) == 0: return
        addons_listitems = self.getListitems(addons_list)
        addons_selected = self.getAddonIndexes(addons_list, addons)
        dialog = xbmcgui.Dialog()
        addons_new = dialog.multiselect(ADDON.getLocalizedString(30233), addons_listitems, preselect=addons_selected, useDetails=True)
        addon_ids = self.getAddonIds(addons_list, addons_new)
        return addon_ids

    def editOrder(self, next=False):
        selected = self.list_addons.getSelectedPosition()
        if not next and selected == 0:
            return
        if next and selected == len(self.addons) - 1:
            return
        tmp = self.addons[selected]
        if not next:
            self.addons[selected] = self.addons[selected-1]
            self.addons[selected-1] = tmp
            selected -= 1
        else:
            self.addons[selected] = self.addons[selected+1]
            self.addons[selected+1] = tmp
            selected += 1
        self.renderAddonList()
        self.list_addons.selectItem(selected)

    def renderAddonList(self):
        self.list_addons.reset()
        for addon in self.addons:
            listitem = xbmcgui.ListItem(addon['name'])
            listitem.setArt({ 'thumb': addon['thumb'] })
            self.list_addons.addItem(listitem)

    def loadAddons(self):
        addon_types = [
            'xbmc.addon.video',
            'xbmc.addon.audio',
            'xbmc.addon.image'
        ]
        list_addons = []
        for addon_type in addon_types:
            query_addons = json_call('Addons.GetAddons',
                                      properties=['name', 'thumbnail'],
                                      params={ 'type': addon_type }
                                      )
            try:
                addons = query_addons['result']['addons']
                for addon in addons:
                    if not self.addonExists(list_addons, addon):
                        list_addons.append(addon)
            except Exception:
                pass
        return list_addons

    def addonExists(self, addons, addon_new):
        for a in addons:
            if a['addonid'] == addon_new['addonid']:
                return True
        return False

    def getListitems(self, addons):
        items = []
        for addon in addons:
            listitem = xbmcgui.ListItem(addon['name'])
            listitem.setArt({ 'thumb': addon['thumbnail'] })
            items.append(listitem)
        return items

    def getAddonIds(self, addons, addons_new):
        addon_ids = []
        for addon_new in addons_new:
            addon = {
                'id': addons[addon_new]['addonid'],
                'name': addons[addon_new]['name'],
                'thumb': addons[addon_new]['thumbnail']
            }
            addon_ids.append(addon)
        return addon_ids

    def getAddonIndexes(self, addons, addon_ids):
        addon_indexes = []
        for addon in addon_ids:
            i = 0
            addon_id = addon['id']
            for addon in addons:
                if addon['addonid'] == addon_id:
                    addon_indexes.append(i)
                    break
                i += 1
        return addon_indexes

############################################################################
# PlaylistSelector
############################################################################
class PlaylistSelector:

    def __init__( self, window ):
        self.playlist_widgets = [
            { 'cat': 1, 'type': 2, 'pl_type': 'video', 'pl_subtype': 'movies' },
            { 'cat': 2, 'type': 2, 'pl_type': 'video', 'pl_subtype': 'tvshows' },
            { 'cat': 2, 'type': 3, 'pl_type': 'video', 'pl_subtype': 'episodes' },
            { 'cat': 3, 'type': 3, 'pl_type': 'music', 'pl_subtype': 'songs' },
            { 'cat': 3, 'type': 4, 'pl_type': 'music', 'pl_subtype': 'albums' },
            { 'cat': 3, 'type': 5, 'pl_type': 'music', 'pl_subtype': 'artists' },
            { 'cat': 4, 'type': 2, 'pl_type': 'video', 'pl_subtype': 'musicvideos' }
        ]
        self.label_playlist = window.getControl(802)
        self.label_playlist_selected = window.getControl(803)
        self.button_select_playlist = window.getControl(804)

    def setVisible( self, show ):
        self.label_playlist.setVisible(show)
        self.label_playlist_selected.setVisible(show)
        self.button_select_playlist.setVisible(show)

    def show( self, cat, type ):
        for pw in self.playlist_widgets:
            if pw['cat'] == cat and pw['type'] == type:
                return True
        return False

    def hide( self, cat, type ):
        if not self.label_playlist.isVisible():
            return False
        for pw in self.playlist_widgets:
            if not (pw['cat'] == cat and pw['type'] == type):
                return True
        return False

    def setDetail(self, playlist):
        if playlist == '':
            playlist = ADDON.getLocalizedString(30116)
        self.label_playlist_selected.setLabel(playlist)

    def showSelector(self, category, type, playlist_presel):
        playlist_widget_index = self.getPlaylistWidgetIndex(category, type)
        if playlist_widget_index == -1:
            return
        pl_type = self.playlist_widgets[playlist_widget_index]['pl_type']
        pl_subtype = self.playlist_widgets[playlist_widget_index]['pl_subtype']
        playlists = self.loadPlaylist(pl_type, pl_subtype)
        listitems = []
        for pl in playlists:
            thumb = 'icons/mainmenu/' + pl['type'] + '.png'
            listitem = xbmcgui.ListItem(label=pl['name'])
            listitem.setArt( { 'thumb': thumb } )
            listitems.append(listitem)
        playlist_selected = self.getPlaylistIndex(playlists, playlist_presel)
        dialog = xbmcgui.Dialog()
        playlist_new = dialog.select(ADDON.getLocalizedString(30250), listitems, preselect=playlist_selected, useDetails=True)
        if playlist_new == -1:
            return ''
        return playlists[playlist_new]['name'] + '.' + playlists[playlist_new]['type']

    def loadPlaylist(self, playlist_type, playlist_subtype):
        path_playlists = xbmc.translatePath(  'special://masterprofile/playlists/' + playlist_type ).decode("utf-8")
        log('path_playlists %s' % path_playlists)
        dirs, files = xbmcvfs.listdir(path_playlists)
        playlists = []
        exts = ['.xsp', '.m3u']
        for playlist in files:
            log('checking %s' % playlist)            
            playlist_ext = ''
            for ext in exts:
                if playlist.find(ext) > -1:
                    playlist_ext = ext[1:4]
            log('ext %s' % playlist_ext)
            subtype = ''
            if playlist_ext == 'xsp':
                subtype = self.getPlaylistSubType(path_playlists, playlist)
            elif playlist_ext == 'm3u':
                subtype = 'songs'
            log('subtype %s, playlist subtype %s' % (subtype, playlist_subtype))            
            if subtype != playlist_subtype:
                continue
            playlist = {
                'name': playlist[0:-4],
                'type': playlist_ext
            }
            playlists.append(playlist)
        return playlists

    def getPlaylistSubType(self, path, playlist):
        file = path + '/' + playlist
        log("checking %s" % file)
        tree = xml.parse(file)
        root = tree.getroot()
        return root.attrib['type']

    def getPlaylistIndex(self, playlists, playlist):
        index = 0
        for pl in playlists:
            pl_file = pl['name'] + '.' + pl['type']
            if pl_file == playlist:
                return index
            index += 1
        return -1

    def getPlaylistWidgetIndex(self, cat, type):
        index = 0
        for pw in self.playlist_widgets:
            if pw['cat'] == cat and pw['type'] == type:
                return index
            index += 1
        return -1

