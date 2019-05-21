import xbmc, xbmcgui
import os
import json
from resources.lib.helper import *
#######################################################################################

ADDON               = xbmcaddon.Addon()
ADDONID             = ADDON.getAddonInfo('id').decode( 'utf-8' )
CONFIGPATH          = os.path.join( xbmc.translatePath( "special://profile/" ).decode( 'utf-8' ), "addon_data", ADDONID, 'widget_addon_pathes.json').decode("utf-8")

#######################################################################################

class AddonPathManager:
    
    def __init__(self):
        pass        

    def addPath(self, path, label):
        log("add widget path: %s" % path)
        if not path: return
        dialog = xbmcgui.Dialog()
        name = dialog.input(ADDON.getLocalizedString(30274), defaultt=label, type=xbmcgui.INPUT_ALPHANUM)
        if not name: return
        self.add(name, path)

    def add(self, name, path):
        addon_pathes = self.readExisting()
        path_id = self.getNextId(addon_pathes)
        new_path = {
            'id': path_id,
            'name': name,
            'path': path
        }
        addon_pathes.append(new_path)
        base_path = os.path.dirname(CONFIGPATH)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        fh_addon_pathes = open(CONFIGPATH, 'w+')
        json.dump(addon_pathes, fh_addon_pathes)

    def deletePaths(self, paths, paths_del):
        for index_del in sorted(paths_del, reverse=True):
            del paths[index_del]
        fh_addon_pathes = open(CONFIGPATH, 'w+')
        json.dump(paths, fh_addon_pathes)

    def readExisting(self):
        try:
            fh_addon_pathes = open(CONFIGPATH, 'r')
            addon_pathes = fh_addon_pathes.read()
        except Exception:
            addon_pathes = '[]'
        return json.loads(addon_pathes)

    def getNextId(self, addon_pathes):
        if len(addon_pathes) == 0:
            return 0
        return addon_pathes[len(addon_pathes)-1]['id'] + 1
