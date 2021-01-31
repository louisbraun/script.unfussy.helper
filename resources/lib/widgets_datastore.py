#!/usr/bin/python
# coding: utf-8
import os, json
import xml.etree.ElementTree as xml
import xbmc, xbmcgui, xbmcvfs
from resources.lib.helper import *
from resources.lib.widget_manager import WidgetManager
#######################################################################################

ADDON               = xbmcaddon.Addon()
ADDONID             = ADDON.getAddonInfo('id')
CWD                 = ADDON.getAddonInfo('path')
DEFAULTPATH         = xbmc.translatePath( os.path.join(CWD, 'resources','widgets_default.json') )
CONFIGPATH          = os.path.join( xbmc.translatePath( "special://profile/" ), "addon_data", ADDONID, 'widgets.json')
SKININCLUDEPATH     = xbmc.translatePath( os.path.join('special://skin', 'xml','Includes_Home_Widgetcontent.xml') )

#######################################################################################

class WidgetsDataStore:

    def __init__(self, wm = None):
        if not wm:
            self.wm = WidgetManager()
        else:
            self.wm = wm
        self.changed = False
        self.widgets = None
        self.xmlWriter = WidgetXMLWriter(self.wm)

    def loadWidgets(self):
        self.load(CONFIGPATH)
        if not self.widgets:
            self.load(DEFAULTPATH)
        if self.widgets:
            return True
        else:
            return False

    def load(self, file):
        data = None
        try:
            widgets_json_file = open(file).readlines()
            widgets_json = ''
            for line in widgets_json_file:
                widgets_json += line
            data = json.loads(widgets_json)
        except Exception:
            self.widgets = None
        self.widgets = data

    def hasChanged(self):
        self.changed = True
    
    def reset(self):
        xbmcvfs.delete(CONFIGPATH)
        self.widgets = None
        self.changed = True
        self.loadWidgets()

    def saveWidgets(self):
        if not self.changed: return
        self.saveJson()
        self.xmlWriter.save(self.widgets)

    def setSkinStrings(self):
        xbmc.executebuiltin('Skin.Reset(runningat_name_0)')
        xbmc.executebuiltin('Skin.Reset(runningat_path_0)')
        xbmc.executebuiltin('Skin.Reset(runningat_name_1)')
        xbmc.executebuiltin('Skin.Reset(runningat_path_1)')
        xbmc.executebuiltin('Skin.Reset(runningat_name_2)')
        xbmc.executebuiltin('Skin.Reset(runningat_path_2)')
        runningat_found = 0
        for widget in self.widgets:
            if not widget['visible']: 
                continue
            if widget['category'] == 0 and widget['type'] == 3:
                #write skinstring for runningat widget
                name = widget['header']
                base_path = self.wm.getPath(0, 3)
                path = base_path + '&pointintime=' + widget['pointintime']
                path += '&channels='
                channels = '%s' % widget['channels']
                channels = channels.replace(' ', '')
                channels = channels.replace(',', '-')
                path += channels
                str_name = 'runningat_name_' + str(runningat_found)
                str_path = 'runningat_path_' + str(runningat_found)
                xbmc.executebuiltin('Skin.SetString(' + str_name + ',' + name.encode('utf-8') + ')')
                xbmc.executebuiltin('Skin.SetString(' + str_path + ',' + path.encode('utf-8') + ')')
                runningat_found += 1
            if runningat_found == 3:
                break

    def saveJson(self):
        base_path = os.path.dirname(CONFIGPATH)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        widgets_json_file = open(CONFIGPATH, 'w+')
        json.dump(self.widgets, widgets_json_file)

    def checkXMLIncludes(self):
        if xbmcvfs.exists(SKININCLUDEPATH):
            return False
        self.loadWidgets()
        self.changed = True
        self.saveWidgets()
        return True

    def getWidgetId(self, cat, type):
        widget_id = 500
        for widget in self.widgets:
            if not widget['visible']: 
                continue
            if widget['category'] == cat and widget['type'] == type:
                return widget_id
            widget_id += 1
        return -1

    def getValue(self, index_widget, item):
        if not item in self.widgets[index_widget]:
            return
        return self.widgets[index_widget][item]

    def getHeader(self, index_widget):
        header = self.widgets[index_widget]['header']
        if header.isdigit():
            header = ADDON.getLocalizedString(int(header))
        return header

    def setValue(self, index_widget, item, value):
        if not item in self.widgets[index_widget]:
            return
        self.changed = True
        self.widgets[index_widget][item] = value

    def switchElements(self, index_widget, up):
        self.changed = True
        index_new = -1
        if up:
            if index_widget == 0: return
            index_new = index_widget - 1
        else:
            if index_widget == len( self.widgets ) - 1 : return
            index_new = index_widget + 1
        tmp = self.widgets[index_widget]
        self.widgets[index_widget] = self.widgets[index_new]
        self.widgets[index_new] = tmp
        return index_new

    def newElement(self, index_widget):
        self.changed = True
        new_widget = {
            'header': ADDON.getLocalizedString(30033),
            'category': -1,
            'type': -1,
            'style': -1,
            'limit': 20,
            'sortby': 0,
            'visible': True
        }
        self.widgets.insert(index_widget+1, new_widget)

    def addValue(self, index_widget, item, value):
        self.widgets[index_widget][item] = value

    def addArray(self, index_widget, item):
        self.widgets[index_widget][item] = []
    
    def deleteElement(self, index_widget):
        self.changed = True
        del self.widgets[index_widget]

class WidgetXMLWriter:

    def __init__(self, wm):
        self.wm = wm

    def save(self, widgets):
        #root element 'includes'
        root = xml.Element('includes')
        #include home_widget_content
        include_widget_content = xml.SubElement(root, 'include')
        include_widget_content.set('name', 'home_widget_content')
        include_widget_anchor = xml.SubElement(root, 'include')
        include_widget_anchor.set('name', 'home_widget_anchors')
        widget_id = 500
        num_widgets = len(widgets)
        for widget in widgets:
            if not widget['visible']: 
                continue
            self.widgetItem(include_widget_content, widget, widget_id)
            self.widgetAnchor(include_widget_anchor, widget, widget_id, num_widgets)
            if self.wm.isAddonWidget(widget['category'], widget['type']):
                self.writeStaticContent(root, widget, widget_id)
            widget_id += 1
        self.createWidgetHeaderCond(root, widgets)
        indent(root)
        #log("xml: \n%s" % xml.tostring(root))
        #log("write to %s" % SKININCLUDEPATH)
        tree = xml.ElementTree(root)
        tree.write(SKININCLUDEPATH, xml_declaration=True, encoding='utf-8', method="xml")

    def widgetItem(self, parent, widget, id):
        widget_item = xml.SubElement(parent, 'include')
        widget_item.set('content', 'widget_mainmenu')
        self.setParam(widget_item, 'id', id)
        header = widget['header']
        if header.isdigit():
            header = ADDON.getLocalizedString(int(header))
        self.setParam(widget_item, 'header', header)
        if self.wm.setLimit(widget['category'], widget['type']):
            self.setParam(widget_item, 'limit', widget['limit'])
        self.setParam(widget_item, 'type', self.wm.getStyleWidget(widget['category'], widget['type'], widget['style']))
        self.setParam(widget_item, 'itemwidth', self.wm.getWidth(widget['category'], widget['type'], widget['style']))
        self.setParam(widget_item, 'height', self.wm.getHeight(widget['category'], widget['type'], widget['style']))
        path = self.getPath(widget)
        if self.wm.isAddonWidget(widget['category'], widget['type']):
            path += '-' + str(id)
        self.setParam(widget_item, 'path', path)
        if self.wm.staticContent(widget['category'], widget['type']):
            self.setParam(widget_item, 'static_content', 'true')
        if self.wm.hasOnClick(widget['category'], widget['type']):
            self.setParam(widget_item, 'onclick', self.wm.getOnClick(widget['category'], widget['type']))
            self.setParam(widget_item, 'useonclick', 'true')
        if self.wm.isOrderableWidget(widget['category'], widget['type']):
            self.setParam(widget_item, 'sortby', self.wm.getSortbyDynamic(widget['sortby']))
        else:
            self.setParam(widget_item, 'sortby', self.wm.getSortby(widget['category'], widget['type']))
        self.setParam(widget_item, 'sortorder', self.wm.getSortorder(widget['category'], widget['type']))
        if self.wm.hasTarget(widget['category'], widget['type']):
            self.setParam(widget_item, 'target', self.wm.getTarget(widget['category'], widget['type']))
        if self.wm.showPlayStatus(widget['category'], widget['type']):
            self.setParam(widget_item, 'showplaystatus', 'true')

    def widgetAnchor(self, parent, widget, id, num_widgets):
        anchor = xml.SubElement(parent, 'control')
        anchor.set('type', 'button')
        anchor.set('id', str(id) + '777')
        visible = xml.SubElement(anchor, 'visible')
        visible.set('allowhiddenfocus', 'true')
        visible.text = 'false'
        onright = xml.SubElement(anchor, 'onright')
        onright.text = 'SetProperty(active_channel,' + str(id) + ')'
        onright2 = xml.SubElement(anchor, 'onright')
        onright2.text = str(id)
        onleft = xml.SubElement(anchor, 'onleft')
        onleft.text = '9001'
        onup = xml.SubElement(anchor, 'onup')
        if id == 500:
            onup.text = '9001'
        else:
            onup.text = 'SetFocus(' + str(id-1) + ')'
        ondown = xml.SubElement(anchor, 'ondown')
        if id == (500 + num_widgets - 1):
            ondown.text = 'SetFocus(500)'
        else:
            ondown.text = 'SetFocus(' + str(id+1) + ')'
        onclick = xml.SubElement(anchor, 'onclick')
        onclick.text = self.getOnClick(widget)

    def getOnClick(self, widget):
        cat = widget['category']
        type = widget['type']
        onclick = ''
        if (cat == 1 and type == 2) or (cat == 2 and (type == 2 or type == 3)) or (cat == 4 and type == 2):
            onclick = 'ActivateWindow(Videos,special://profile/playlists/video/%s,return)' % widget['playlist']
        elif cat == 3 and (type == 3 or type == 4 or type == 5):
            onclick = 'ActivateWindow(Music,special://profile/playlists/music/%s,return)' % widget['playlist']
        elif cat == 5 and type == 1:
            addonpath = widget['addonpath']['path']
            first_slash = addonpath.find('/',10)
            plugin_id = addonpath[9:first_slash]
            onclick = 'RunAddon(' + plugin_id + ')' 
        else:
            onclick = self.wm.getHeaderAction(widget['category'], widget['type'])
        return onclick

    def getPath(self, widget):
        path = ''
        if widget['category'] == 0 and  widget['type'] == 3:
            base_path = self.wm.getPath(widget['category'], widget['type'])
            path = base_path + '&pointintime=' + widget['pointintime']
            path += '&channels='
            path = '%s%s' % (path, widget['channels'])
        elif ((widget['category'] == 1 and  widget['type'] == 2) or 
              (widget['category'] == 2 and  widget['type'] == 2) or 
              (widget['category'] == 2 and  widget['type'] == 3) or
              (widget['category'] == 3 and  widget['type'] == 3) or
              (widget['category'] == 3 and  widget['type'] == 4) or
              (widget['category'] == 3 and  widget['type'] == 5) or
              (widget['category'] == 4 and  widget['type'] == 2)):
            base_path = self.wm.getPath(widget['category'], widget['type'])
            if widget['playlist'] != '':
                path = base_path + '/' + widget['playlist']
        elif widget['category'] == 5 and  widget['type'] == 1:
            path = widget['addonpath']['path']
        else:
            path = self.wm.getPath(widget['category'], widget['type'])
        return path

    def setParam(self, parent, name, value):
        param = xml.SubElement(parent, 'param')
        param.set('name', name)
        param.text = encode4XML(value)

    def writeStaticContent(self, parent, widget, widget_id):
        include_item = xml.SubElement(parent, 'include')
        include_item.set('name', self.getPath(widget) + '-' + str(widget_id))
        content_item = xml.SubElement(include_item, 'content')
        for addon in widget['addons']:
            item = xml.SubElement(content_item, 'item')
            label = xml.SubElement(item, 'label')
            label.text = encode4XML(addon['name'])
            thumb = xml.SubElement(item, 'thumb')
            thumb.text = encode4XML(addon['thumb'])
            onclick = xml.SubElement(item, 'onclick')
            onclick.text = encode4XML('RunAddon(' + addon['id'] + ')')

    def createWidgetHeaderCond(self, parent, widgets):
        id = 500
        num_widgets = len(widgets)
        cond = 'ControlGroup(9002).HasFocus'
        if num_widgets > 0:
            cond += ' | '
        for widget in widgets:
            if not widget['visible']: 
                continue
            cond += 'Control.HasFocus(' + str(id) + '777)'
            if id < (500 + num_widgets - 1):
                cond += ' | '
            id += 1
        include_item = xml.SubElement(parent, 'include')
        include_item.set('name', 'cond_show_updown_arrows')
        visible_item = xml.SubElement(include_item, 'visible')
        visible_item.text = cond
