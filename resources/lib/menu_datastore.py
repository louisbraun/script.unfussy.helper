#!/usr/bin/python
# coding: utf-8
import os, json
import xml.etree.ElementTree as xml
import xbmc, xbmcgui, xbmcvfs
from resources.lib.helper import *
from resources.lib.menu_actionmanager import MenuActionManager

#######################################################################################

ADDON               = xbmcaddon.Addon()
ADDONID             = ADDON.getAddonInfo('id').decode( 'utf-8' )
CWD                 = ADDON.getAddonInfo('path').decode('utf-8')
DEFAULTPATH         = xbmc.translatePath( os.path.join(CWD, 'resources','menu_default.json') ).decode("utf-8")
CONFIGPATH          = os.path.join( xbmc.translatePath( "special://profile/" ).decode( 'utf-8' ), "addon_data", ADDONID, 'menu.json').decode("utf-8")
SKININCLUDEPATH     = xbmc.translatePath( os.path.join('special://skin', 'xml','Includes_Home_Menucontent.xml') ).decode("utf-8")

#######################################################################################

class MenuDataStore:

    def __init__(self, am = None):
        if not am:
            self.am = MenuActionManager()
        else:
            self.am = am
        self.changed = False
        self.menu = None
        self.xmlWriter = MenuXMLWriter(self.am)

    def loadMenu(self):
        self.load(CONFIGPATH)
        if not self.menu:
            self.load(DEFAULTPATH)
        if self.menu:
            return True
        else:
            return False

    def load(self, file):
        data = None
        try:
            menu_json_file = open(file).readlines()
            menu_json = ''
            for line in menu_json_file:
                menu_json += line
            data = json.loads(menu_json)
        except Exception:
            self.menu = None
        self.menu = data

    def reset(self):
        xbmcvfs.delete(CONFIGPATH)
        self.menu = None
        self.changed = True
        self.loadMenu()

    def saveMenu(self):
        if not self.changed: return
        self.saveJson()
        self.xmlWriter.save(self.menu)

    def saveJson(self):
        base_path = os.path.dirname(CONFIGPATH)
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        menu_json_file = open(CONFIGPATH, 'w+')
        json.dump(self.menu, menu_json_file)

    def checkXMLIncludes(self):
        if xbmcvfs.exists(SKININCLUDEPATH):
            return False
        self.loadMenu()
        self.changed = True
        self.saveMenu()
        return True

    def mainmenu(self):
        return self.menu

    def submenu(self, index):
        return self.menu[index]['submenu']

    def hasSubmenu(self, index):
        if len(self.menu[index]['submenu']) > 0:
            return True
        else:
            return False

    def getValue(self, index_menu, index_submenu, item):
        value = 0
        if index_submenu > -1:
            if item in self.menu[index_menu]['submenu'][index_submenu]:
                value = self.menu[index_menu]['submenu'][index_submenu][item]
        else:
            if item in self.menu[index_menu]:
                value = self.menu[index_menu][item]
        return value

    def getLabel(self, index_menu, index_submenu):
        label = self.menu[index_menu]['label']
        if index_submenu > -1:
            label = self.menu[index_menu]['submenu'][index_submenu]['label']
        if label.isdigit():
            label = '$LOCALIZE[' + label + ']'
        return label

    def setValue(self, index_menu, index_submenu, item, value):
        self.changed = True
        if index_submenu > -1:
            self.menu[index_menu]['submenu'][index_submenu][item] = value
        else:
            self.menu[index_menu][item] = value
            log('item changed %s' % self.menu[index_menu])

    def newElement(self, index_menu, index_submenu):
        self.changed = True
        if index_submenu == -1:
            self.menu.insert(index_menu+1, self.newMenuItem())
        else:
            self.menu[index_menu]['submenu'].insert(index_submenu+1, self.newMenuItem())

    def newSubmenu(self, index_menu):
        self.changed = True
        self.menu[index_menu]['submenu'].append(self.newMenuItem())

    def newMenuItem(self):
        new_element = {
            'label': ADDON.getLocalizedString(30022),
            'thumb': 'icons/buttons/new.png',
            'actiontype': -1,
            'action': -1,
            'visible': True,
            'submenu': []
        }
        return new_element

    def deleteElement(self, index_menu, index_submenu):
        self.changed = True
        if index_submenu == -1:
            del self.menu[index_menu]
        else:
            del self.menu[index_menu]['submenu'][index_submenu]

    def switchElements(self, index_menu, index_submenu, up):
        self.changed = True
        index_new = -1
        if index_submenu > -1:
            if up:
                if index_submenu == 0: return
                index_new = index_submenu - 1
            else:
                if index_submenu == len( self.menu[index_menu]['submenu'] ) - 1 : return
                index_new = index_submenu + 1
        else:
            if up:
                if index_menu == 0: return
                index_new = index_menu - 1
            else:
                if index_menu == len( self.menu ) - 1 : return
                index_new = index_menu + 1
        if index_submenu > -1:
            tmp = self.menu[index_menu]['submenu'][index_submenu]
            self.menu[index_menu]['submenu'][index_submenu] = self.menu[index_menu]['submenu'][index_new]
            self.menu[index_menu]['submenu'][index_new] = tmp
        else:
            tmp = self.menu[index_menu]
            self.menu[index_menu] = self.menu[index_new]
            self.menu[index_new] = tmp
        return index_new


class MenuXMLWriter:

    def __init__(self, am):
        self.am = am
    
    def save(self, menu):
        #root element 'includes'
        root = xml.Element('includes')
        #include home_mainmenu_content
        include_mainmenu_content = xml.SubElement(root, 'include')
        include_mainmenu_content.set('name', 'home_mainmenu_content')
        #content element in main menu content
        item_content = xml.SubElement(include_mainmenu_content, 'content')
        #include home_mainmenu_submenus
        include_mainmenu_submenus = xml.SubElement(root, 'include')
        include_mainmenu_submenus.set('name', 'home_mainmenu_submenus')
        #build tree
        submenu_id = 10        
        for item in menu:
            if not item['visible']: 
                continue
            if len(item['submenu']) == 0:
                self.mainMenuItem(item_content, item)
            else:
                self.mainMenuItem(item_content, item, submenu_id)
                self.submenusItem(include_mainmenu_submenus, submenu_id)
                self.submenuContent(root, item['submenu'], submenu_id)
                submenu_id += 10
        
        indent(root)
#        log("xml: \n%s" % xml.tostring(root))
#        log("write to %s" % SKININCLUDEPATH)
        tree = xml.ElementTree(root)
        tree.write(SKININCLUDEPATH, xml_declaration=True, encoding='utf-8', method="xml")

    def mainMenuItem(self, parent, item, sub_id = 0):
        label = self.getLabel(item['label'])
        thumbsize = self.getThumbsize(item)
        self.menuItem(parent, label, item['thumb'], thumbsize, item['actiontype'], item['action'], sub_id)

    def submenusItem(self, parent, sub_id):
        include_submenu = xml.SubElement(parent, 'include')
        include_submenu.set('content', 'home_submenu')
        param = xml.SubElement(include_submenu, 'param')
        param.set('name', 'id')
        param.text = str(sub_id)

    def submenuContent(self, parent, submenu, sub_id):
        include_submenu = xml.SubElement(parent, 'include')
        include_submenu.set('name', 'home_submenu_content_id_' + str(sub_id))
        item_content = xml.SubElement(include_submenu, 'content')
        for item in submenu:
            if not item['visible']: 
                continue
            label = self.getLabel(item['label'])
            thumbsize = self.getThumbsize(item)
            self.menuItem(item_content, label, item['thumb'], thumbsize, item['actiontype'], item['action'], -1)

    def menuItem(self, parent, label, thumb, thumbsize, actiontype, action, sub_id):
        xml_item = xml.SubElement(parent, 'item')
        xml_label = xml.SubElement(xml_item, 'label')
        xml_label.text = encode4XML(label)
        xml_thumb = xml.SubElement(xml_item, 'thumb')
        xml_thumb.text = thumb
        if actiontype > 3:
            xml_onclick = xml.SubElement(xml_item, 'onclick')
            xml_onclick.text = self.am.getOnClick(actiontype, action)
        else:
            xml_onclick1 = xml.SubElement(xml_item, 'onclick')
            xml_onclick1.set('condition', self.am.getOnClickCond(actiontype))
            xml_onclick1.text = self.am.getOnClick(actiontype, action)
            xml_onclick2 = xml.SubElement(xml_item, 'onclick')
            xml_onclick2.set('condition', '!' + self.am.getOnClickCond(actiontype))
            xml_onclick2.text = self.am.getOnClickAlt(actiontype)

        xml_thumbsize = xml.SubElement(xml_item, 'property')
        xml_thumbsize.set('name', 'thumbsize')
        xml_thumbsize.text = '$NUMBER[' + str(thumbsize) + ']'
        if sub_id == -1:
            return
        submenu_id = xml.SubElement(xml_item, 'property')
        submenu_id.set('name', 'submenu_id')
        submenu_id.text = '$NUMBER[' + str(sub_id) + ']'

    def getLabel(self, label):
        if label.isdigit():
            label = '$LOCALIZE[' + label + ']'
        return label

    def getThumbsize(self, item):
        if 'thumbsize' in item:
            return item['thumbsize']
        else:
            return 0