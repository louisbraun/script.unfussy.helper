#!/usr/bin/python
# coding: utf-8
import xbmc, xbmcgui, xbmcvfs
from resources.lib.helper import *
#######################################################################################

ADDON               = xbmcaddon.Addon()

#######################################################################################

class Gui_ChannelGuide( xbmcgui.WindowXMLDialog ):
    
    def __init__( self, *args, **kwargs ):
        self.channelgroups = None
        self.detail_active = False
        self.channels_loaded = self.loadChannels()

    def loadChannels(self):
        if not self.loadChannelGroups():
            return False

        for index, group in enumerate(self.channelgroups):
            id = group['channelgroupid']
            query = json_call('PVR.GetChannels',
                    properties = channeldetail_properties, 
                    params={ 'channelgroupid': id } )
            try:
                self.channelgroups[index]['channels'] = query['result']['channels']
                self.channelgroups[index]['channellistitems'] = None
            except Exception:
                log('error loading channels', WARNING)
                return False
        return True

    def loadChannelGroups(self):
        query = json_call('PVR.GetChannelGroups',
                    params={'channeltype': 'tv'} )
        try:
            self.channelgroups = query['result']['channelgroups']
        except Exception:
            return False
        log("loaded groups: %s" % self.channelgroups, DEBUG)
        hide_all_channels = xbmc.getCondVisibility('Skin.HasSetting(hide_all_channels)')
        if hide_all_channels:
            allchannels = -1
            str_allchannels = xbmc.getLocalizedString(19287)
            for index, group in enumerate(self.channelgroups):
                if group['label'] == str_allchannels:
                    allchannels = index
                    break
            if allchannels > -1:
                del self.channelgroups[allchannels]
        log("groups after hide_all_channels: %s" % self.channelgroups, DEBUG)
        return True

    def onInit( self ):
        self.hor_layout = xbmc.getCondVisibility('Skin.HasSetting(use_channelgroups_fullwidth)')
        if not self.channels_loaded:
            return
        self.list_channelgroups = self.getControl(12)
        self.list_channels = self.getControl(13)
        self.active_channel_number = self.getActiveChannelNumber()
        self.group_index, self.channel_index = self.getActiveChannelIndex()
        self.jump_to_next_group = xbmc.getCondVisibility('Skin.HasSetting(jump_to_next_channelgroup)')
        self.renderChannelGroups()
        self.list_channelgroups.selectItem(self.group_index)
        self.renderChannels()
        self.positionChannellist()
        self.list_channels.selectItem(self.channel_index)
        self.setFocusId(13)
        xbmc.executebuiltin('ClearProperty(loadingchannels,10608)')

    def onClick(self, control_id):
        if not control_id == 13:
            return
        group_index = self.list_channelgroups.getSelectedPosition()
        channel_index = self.list_channels.getSelectedPosition()
        channel_uid = self.channelgroups[group_index]['channels'][channel_index]['broadcastnow']['channeluid']
        xbmc.executebuiltin('SetProperty(noslide,true,10608)')
        self.setProperty('noslide', 'true')
        xbmc.sleep(10)
        self._close()
        self.switchChannel(channel_uid)

    def onAction(self, action):
        if action.getId() == 92:
            self._close()
        elif action.getId() == 1:
            self.keyLeft()
        elif action.getId() == 2:
            self.keyRight()
        elif action.getId() == 3:
            self.keyUp()
        elif action.getId() == 4:
            self.keyDown()

    def _close(self):
        self.clearProperty('showdetail')
        self.close()
        xbmc.executebuiltin('Action(Close,10608)')

    def keyLeft(self):
        focus = self.getFocusId()
        if focus == 13 and not self.detail_active:
            self.setFocusId(12)
        elif focus == 13 and self.detail_active:
            self.clearProperty('showdetail')
            self.detail_active = False
        elif focus == 12:
            self._close()

    def keyRight(self):
        focus = self.getFocusId()
        if focus == 12:
            self.setFocusId(13)
        elif focus == 13:
            self.setProperty('showdetail', 'true')
            self.detail_active = True

    def keyUp(self):
        focus = self.getFocusId()
        if focus == 12:
            self.group_index = self.list_channelgroups.getSelectedPosition()
            self.channel_index = 0
            self.updateChannels()
        elif focus == 13:
            self.channel_index = self.list_channels.getSelectedPosition()
            if self.channel_index == len(self.channelgroups[self.group_index]['channels'])-1 and self.jump_to_next_group:
                self.groupUp()

    def keyDown(self):
        focus = self.getFocusId()
        if focus == 12:
            self.group_index = self.list_channelgroups.getSelectedPosition()
            self.channel_index = 0
            self.updateChannels()
        elif focus == 13:
            self.channel_index = self.list_channels.getSelectedPosition()
            if self.channel_index == 0 and self.jump_to_next_group:
                self.groupDown()

    def groupUp(self):
        self.group_index -= 1
        if self.group_index == -1:
            self.group_index = len(self.channelgroups) - 1
        self.list_channelgroups.selectItem(self.group_index)
        self.channel_index = len(self.channelgroups[self.group_index]['channels'])-1
        self.updateChannels()

    def groupDown(self):
        self.group_index += 1
        if self.group_index == len(self.channelgroups):
            self.group_index = 0
        self.list_channelgroups.selectItem(self.group_index)
        self.channel_index = 0
        self.updateChannels()

    def updateChannels(self):
        self.renderChannels()
        self.positionChannellist()
        self.list_channels.selectItem(self.channel_index)

    def renderChannels(self):
        if not self.channelgroups[self.group_index]['channellistitems']:
            self.setChannelListItems()
        self.list_channels.reset()
        for item in self.channelgroups[self.group_index]['channellistitems']:
            self.list_channels.addItem(item)

    def renderChannelGroups(self):
        for index, group in enumerate(self.channelgroups):
            listitem = xbmcgui.ListItem(group['label'])
            listitem.setProperty('numchannels', str(len(group['channels'])))
            if index == self.group_index:
                listitem.setProperty('group_activechannel', 'true')
                listitem.select(True)
            self.list_channelgroups.addItem(listitem)

    def positionChannellist(self):
        if self.hor_layout: return
        x = 100
        y = 0
        height = 1080
        max_items = 11
        num_channels = len(self.channelgroups[self.group_index]['channels'])
        if num_channels < max_items:
            height = num_channels * 100
            y = int((1080 - height)/2)
        self.list_channels.setHeight(height)
        self.list_channels.setPosition(x, y)

    def setChannelListItems(self):
        self.channelgroups[self.group_index]['channellistitems'] = []
        utc_offset = getUtcOffset()
        for channel in self.channelgroups[self.group_index]['channels']:
            try:
                listitem = xbmcgui.ListItem(channel['label'])
                listitem.setArt({ 'icon': channel['icon'] })
                listitem.setProperty('channelnumber', str(channel['channelnumber']))
                listitem.setProperty('isrecording', str(channel['broadcastnow']['hastimer']))
                listitem.setProperty('progress', str(int(channel['broadcastnow']['progresspercentage'])))
                listitem.setProperty('now_title', channel['broadcastnow']['title'])
                listitem.setProperty('now_episodename', channel['broadcastnow']['episodename'])
                listitem.setProperty('now_episodenum', str(channel['broadcastnow']['episodenum']))
                listitem.setProperty('now_year', str(channel['broadcastnow']['year']))
                listitem.setProperty('now_director', channel['broadcastnow']['director'])
                listitem.setProperty('now_genre', ', '.join(channel['broadcastnow']['genre']))
                listitem.setProperty('now_cast', channel['broadcastnow']['cast'])
                listitem.setProperty('now_plot', channel['broadcastnow']['plot'])
                starttime = getTimeFromString(channel['broadcastnow']['starttime'], '%Y-%m-%d %H:%M:%S', utc_offset)
                endtime = getTimeFromString(channel['broadcastnow']['endtime'], '%Y-%m-%d %H:%M:%S', utc_offset)
                listitem.setProperty('now_starttime', starttime.strftime('%H:%M'))
                listitem.setProperty('now_endtime', endtime.strftime('%H:%M'))
                listitem.setProperty('now_runtime', str(channel['broadcastnow']['runtime']))
                listitem.setProperty('next_title', channel['broadcastnext']['title'])
                listitem.setProperty('next_episodename', channel['broadcastnext']['episodename'])
                listitem.setProperty('next_episodenum', str(channel['broadcastnext']['episodenum']))
                listitem.setProperty('next_year', str(channel['broadcastnext']['year']))
                listitem.setProperty('next_director', channel['broadcastnext']['director'])
                listitem.setProperty('next_genre', ', '.join(channel['broadcastnext']['genre']))
                listitem.setProperty('next_cast', channel['broadcastnext']['cast'])
                listitem.setProperty('next_plot', channel['broadcastnext']['plot'])
                starttime_next = getTimeFromString(channel['broadcastnext']['starttime'], '%Y-%m-%d %H:%M:%S', utc_offset)
                endtime_next = getTimeFromString(channel['broadcastnext']['endtime'], '%Y-%m-%d %H:%M:%S', utc_offset)
                listitem.setProperty('next_starttime', starttime_next.strftime('%H:%M'))
                listitem.setProperty('next_endtime', endtime_next.strftime('%H:%M'))
                listitem.setProperty('next_runtime', str(channel['broadcastnext']['runtime']))
                if channel['channelnumber'] == self.active_channel_number:
                    listitem.select(True)
                self.channelgroups[self.group_index]['channellistitems'].append(listitem)
            except Exception:
                log('no epg for channel: %s' % Exception, WARNING )

    def getActiveChannelNumber(self):
        channel_num = xbmc.getInfoLabel('VideoPlayer.ChannelNumberLabel')
        return int(channel_num)

    def getActiveChannelIndex(self):
        for index, group in enumerate(self.channelgroups):
            for index_channel, channel in enumerate(group['channels']):
                if channel['channelnumber'] == self.active_channel_number:
                    return (index, index_channel)
        return (-1,-1)

    def switchChannel(self, channel_uid):
        all_channels_loc = xbmc.getLocalizedString(19287).encode('utf-8')
        pvr_backend = self.pvrBackendAddonId()
        if not pvr_backend: return
        pvr_url = 'pvr://channels/tv/' + all_channels_loc + '/' + pvr_backend + '_' + str(channel_uid) + '.pvr'
        action = 'PlayMedia(' + pvr_url + ')'
        xbmc.executebuiltin(action)

    def pvrBackendAddonId(self):
        query_addons = json_call('Addons.GetAddons', params={ 'type': 'xbmc.pvrclient' }, properties=['enabled'])
        try:
            addons = query_addons['result']['addons']
            for addon in addons:
                if addon['enabled']:
                    return addon['addonid'].encode('utf-8')
            return None
        except Exception:
            log('error querying pvr addon: %s' % Exception, WARNING )
            return None
