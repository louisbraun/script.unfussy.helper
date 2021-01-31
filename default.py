#!/usr/bin/python
import xbmcgui, xbmcaddon
try:
    from urllib2 import urlparse
except ImportError:
    import urllib.parse as urlparse
from resources.lib.helper import *
from resources.lib.gui_menu import Gui_Menu
from resources.lib.menu_datastore import MenuDataStore
from resources.lib.gui_widgets import Gui_Widgets
from resources.lib.widgets_datastore import WidgetsDataStore
from resources.lib.pvr_running_at import PVRRunningAt
from resources.lib.pvr_timers import PVRTimers
from resources.lib.gui_channelguide import Gui_ChannelGuide
from resources.lib.pvr_channellist import PVRChannelList
#######################################################################################

ADDON     = xbmcaddon.Addon()
CWD       = ADDON.getAddonInfo('path')

#######################################################################################

class Main:

    def __init__(self):
        self._parse_argv()
        self.action = self.params.get('action')
        if self.action:
            self.run()

    def run(self):
        changed = False
        if self.action == 'configure_menu':
            ui= Gui_Menu( "script-configure_menu.xml", CWD )
            ui.doModal()
            changed = ui.hasChanged()
            del ui
        elif self.action == 'configure_widgets':
            ui= Gui_Widgets( "script-configure_widgets.xml", CWD )
            ui.doModal()
            changed = ui.hasChanged()
        elif self.action == 'channelguide':
            xml_file = "script-channelguide.xml"
            if xbmc.getCondVisibility('Skin.HasSetting(use_channelgroups_fullwidth)'):
                xml_file = "script-channelguide-hor.xml"
            ui= Gui_ChannelGuide( xml_file, CWD )
            ui.doModal()
        elif self.action == 'loadchannelids':
            cl = PVRChannelList()
            cl.setChannelIds()
        elif self.action == 'info_runningat':
            running_at = PVRRunningAt()
            running_at.showInfo(self.params.get('bc_id'), self.params.get('c_id'), 'script-show_info.xml', CWD)
        elif self.action == 'record_runningat':
            running_at = PVRRunningAt()
            running_at.setTimer(self.params.get('bc_id'))
            timers = PVRTimers()
            timers.refresh()
        elif self.action == 'info_timer':
            timers = PVRTimers()
            ok = timers.delTimerDialog(self.params.get('timer_id'))
            if ok:
                timers.refresh()
        elif self.action == 'refresh_timers':
            timers = PVRTimers()
            timers.refresh()
        elif self.action == 'check_includes':
            mds = MenuDataStore()
            wds = WidgetsDataStore()
            built_menu_includes = mds.checkXMLIncludes()
            built_widget_includes = wds.checkXMLIncludes()
            changed = built_menu_includes or built_widget_includes
            if not changed:
                self.setWidgetIds()
        elif self.action == 'check_defaultsettings':
            init_done = xbmc.getCondVisibility('Skin.HasSetting(init_done)')
            if not init_done:
                self.setSkinDefaults()
        
        if changed:
            self.setWidgetIds()
            xbmc.executebuiltin('ReloadSkin()')

    def _parse_argv(self):
        try:
            args = sys.argv[1]
            self.params = dict(urlparse.parse_qsl(args))
        except Exception:
            self.params = {}

    def setWidgetIds(self):
        wds = WidgetsDataStore()
        wds.loadWidgets()
        widget_timers_id = wds.getWidgetId(0, 4)
        widget_nextepisodes_id = wds.getWidgetId(2, 1)
        win_home = xbmcgui.Window(10000)
        win_home.setProperty('widget_timers_id',str(widget_timers_id))
        win_home.setProperty('widget_nextepisodes_id',str(widget_nextepisodes_id))

    def setSkinDefaults(self):
        xbmc.executebuiltin('Skin.SetBool(init_done)')
        xbmc.executebuiltin('Skin.SetBool(tvguide_show_detail)')
        xbmc.executebuiltin('Skin.SetBool(tvguide_show_channelgroups)')
        xbmc.executebuiltin('Skin.SetBool(use_channelgroups)')
        xbmc.executebuiltin('Skin.SetBool(jump_to_next_channelgroup)')
        xbmc.executebuiltin('Skin.SetBool(hide_all_channels)')
        xbmc.executebuiltin('Skin.SetBool(start_live_tv)')
        xbmc.executebuiltin('Skin.SetBool(use_view_animations)')
        xbmc.executebuiltin('Skin.SetBool(use_pvr_view_animations)')
        xbmc.executebuiltin('Skin.SetBool(music_background_fanart)')
        xbmc.executebuiltin('Skin.SetBool(music_enable_scrollingtext)')


#######################################################################################
if (__name__ == '__main__'):
    Main()
