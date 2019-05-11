#!/usr/bin/python
from resources.lib.helper import *
from resources.lib.kodi_monitor import KodiMonitor


WIN = xbmcgui.Window(10000)
MONITOR = KodiMonitor(win=WIN)
REFRESH_INTERVAL = 10

refresh = 0
while not MONITOR.abortRequested():
    if refresh > REFRESH_INTERVAL:
        WIN.setProperty("widgetreload-timers", time.strftime("%Y%m%d%H%M%S", time.gmtime()))
        WIN.setProperty("widgetreload-runningat", time.strftime("%Y%m%d%H%M%S", time.gmtime()))
        refresh = 0
    else:
        refresh += 1
    # sleep for 60 seconds
    MONITOR.waitForAbort(60)

del MONITOR
del WIN
