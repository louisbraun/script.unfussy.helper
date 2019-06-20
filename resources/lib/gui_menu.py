#!/usr/bin/python
# coding: utf-8
import xbmc, xbmcgui, xbmcvfs
from resources.lib.helper import *
from resources.lib.menu_actionmanager import MenuActionManager
from resources.lib.menu_datastore import MenuDataStore
#######################################################################################

ADDON               = xbmcaddon.Addon()

#######################################################################################

class Gui_Menu( xbmcgui.WindowXMLDialog ):
    
    def __init__( self, *args, **kwargs ):
        self.am = MenuActionManager()
        self.menu = MenuDataStore(self.am)
        if not self.menu.loadMenu():
            log("fatal error loading menu structure")
            self.close()

    def onInit( self ):
        #positions in menu
        self.index_menu = -1
        self.index_submenu = -1
        #controls
        self.control_menu = self.getControl(100)
        self.control_submenu = self.getControl(110)
        self.control_submenu.setVisible(False)
        self.radio_visible = self.getControl(212)
        self.label_actiontype = self.getControl(215)
        self.label_action = self.getControl(219)
        self.button_new_submenu = self.getControl(222)
        self.label_thumbsize = self.getControl(232)
        #init
        self.renderMenu()
        self.setFocus(self.control_menu)
        self.setMenuIndex()
        self.setDetail()

    def onClick(self, control_id):
        self.setMenuIndex()
        if control_id == 201:
            self.moveItem(up=True)
        elif control_id == 203:
            self.moveItem(up=False)
        elif control_id == 207:
            self.editLabel()
        elif control_id == 211:
            self.editIcon()
        elif control_id == 212:
            self.setVisibility()
        elif control_id == 216:
            self.actionType(next=True)
        elif control_id == 217:
            self.actionType(next=False)
        elif control_id == 220:
            self.action()
        elif control_id == 221:
            self.newElement()
        elif control_id == 222:
            self.newSubmenu()
        elif control_id == 223:
            self.deleteElement()
        elif control_id == 224:
            self.reset2Default()
        elif control_id == 100:
            self.showSubmenu()
        elif control_id == 110:
            self.hideSubmenu()
        elif control_id == 233:
            self.thumbSize(next=True)
        elif control_id == 234:
            self.thumbSize(next=False)

    def onAction(self, action):
        self.setMenuIndex()
        if action.getId() == 92:
            #key back
            if self.control_submenu.isVisible():
                self.hideSubmenu()
            else:
                self.menu.saveMenu()
                self.close()
        elif action.getId() == 3 or action.getId() == 4:
            #key up or down
            if self.getFocusId() == 100 or self.getFocusId() == 110:
                self.setDetail()

    def hasChanged(self):
        return self.menu.changed

    def setMenuIndex(self):
        self.index_menu = self.control_menu.getSelectedPosition()
        if self.control_submenu.isVisible():
            self.index_submenu = self.control_submenu.getSelectedPosition()
        else:
            self.index_submenu = -1

    def renderMenu(self):
        self.control_menu.reset()
        for menuitem in self.menu.mainmenu():
            listitem = self.createListItem(menuitem)
            self.control_menu.addItem(listitem)

    def showSubmenu(self):
        if not self.menu.hasSubmenu(self.index_menu): return
        item = self.control_menu.getSelectedItem()
        item.setProperty('show_submenu', 'true')
        self.renderSubmenu()
        self.control_submenu.setVisible(True)
        self.setFocus(self.control_submenu)
        self.setMenuIndex()
        self.setDetail()

    def hideSubmenu(self):
        self.control_submenu.setVisible(False)
        item = self.control_menu.getSelectedItem()
        item.setProperty('show_submenu', 'false')
        self.setFocus(self.control_menu)
        self.control_submenu.reset()
        self.setMenuIndex()
        self.setDetail()

    def renderSubmenu(self):
        self.control_submenu.reset()
        for menuitem in self.menu.submenu(self.index_menu):
            listitem = self.createListItem(menuitem, True)
            self.control_submenu.addItem(listitem)
        top = self.index_menu*80
        if top > 360:
            top = 360
        self.control_submenu.setPosition(400, top)

    def reloadMenu(self, focus=-1):
        if self.index_submenu > -1:
            self.renderSubmenu()
            if focus > -1:
                self.control_submenu.selectItem(focus)
            else:
                self.control_submenu.selectItem(self.index_submenu)
        else:
            self.renderMenu()
            if focus > -1:
                self.control_menu.selectItem(focus)
            else:
                self.control_menu.selectItem(self.index_menu)

    def createListItem(self, menuitem, submenu=False):
        listitem = xbmcgui.ListItem(menuitem['label'])
        if menuitem['label'].isdigit():
            listitem.setLabel(xbmc.getLocalizedString(int(menuitem['label'])))
        listitem.setArt({ 'thumb': menuitem['thumb'] })
        if not submenu and len(menuitem['submenu']) > 0:
            listitem.setProperty('has_submenu', 'true')
        if menuitem['visible']:
            listitem.setProperty('is_visible', 'true')
        else:
            listitem.setProperty('is_visible', 'false')
        if 'thumbsize' in menuitem:
             listitem.setProperty('thumbsize', str(menuitem['thumbsize']))
        else:
             listitem.setProperty('thumbsize', '0')
        return listitem

    #Actions

    def setDetail(self):
        #radio "is visible"
        is_visible = self.menu.getValue(self.index_menu, self.index_submenu, 'visible')
        self.radio_visible.setSelected(is_visible)
        #set icon size
        thumbsize = self.menu.getValue(self.index_menu, self.index_submenu, 'thumbsize')
        self.label_thumbsize.setLabel(self.am.thumbsizes[int(thumbsize)])
        #actiontype and action
        action_type = self.menu.getValue(self.index_menu, self.index_submenu, 'actiontype')
        action = self.menu.getValue(self.index_menu, self.index_submenu, 'action')
        self.label_actiontype.setLabel(self.am.getActionType(action_type))
        self.label_action.setLabel(self.am.getActionName(action_type, action))
        #check if "new submenu" button has to be displayed
        new_submenu = False
        if self.index_submenu == -1 and not self.menu.hasSubmenu(self.index_menu):
            new_submenu = True
        self.button_new_submenu.setVisible(new_submenu)

    def moveItem(self, up=False):
        pos_new = self.menu.switchElements(self.index_menu, self.index_submenu, up)
        self.reloadMenu(pos_new)

    def editLabel(self):
        label = self.menu.getValue(self.index_menu, self.index_submenu, 'label')
        if label.isdigit():
            label = xbmc.getLocalizedString(int(label))
        dialog = xbmcgui.Dialog()
        new_label = dialog.input(ADDON.getLocalizedString(30028), type=xbmcgui.INPUT_ALPHANUM, defaultt=label)
        if new_label == '': return
        self.menu.setValue(self.index_menu, self.index_submenu, 'label', new_label)
        self.reloadMenu()

    def editIcon(self):
        dialog = xbmcgui.Dialog()
        new_thumb = dialog.browse(2, ADDON.getLocalizedString(30029), 'local', '', True)
        if new_thumb == '': return
        self.menu.setValue(self.index_menu, self.index_submenu, 'thumb', new_thumb)
        self.reloadMenu()

    def setVisibility(self):
        selected = self.radio_visible.isSelected()
        self.menu.setValue(self.index_menu, self.index_submenu, 'visible', selected)
        self.reloadMenu()

    def actionType(self, next=False):
        new_type = self.menu.getValue(self.index_menu, self.index_submenu, 'actiontype')
        if next:
            new_type = (new_type+1) % self.am.numActions()
        else:
            new_type = new_type - 1
            if new_type < 0:
                new_type = self.am.numActions() - 1
        self.menu.setValue(self.index_menu, self.index_submenu, 'actiontype', new_type)
        self.menu.setValue(self.index_menu, self.index_submenu, 'action', -1)
        self.label_actiontype.setLabel(self.am.getActionType(new_type))
        self.label_action.setLabel(self.am.getActionName(new_type, -1))

    def action(self):
        action_type = self.menu.getValue(self.index_menu, self.index_submenu, 'actiontype')
        actiontype_name = self.am.getActionType(action_type, False)
        action_items = self.am.getActionItems(action_type)
        dialog = xbmcgui.Dialog()
        action_new = dialog.select(actiontype_name, action_items, preselect=-1, useDetails=True)
        if action_new == -1:
            return
        thumb_new = self.am.getThumb(action_type, action_new)
        if action_type == 8 or action_type == 9:
            action_new = self.am.getPlaylistId(action_type, action_new)
        if action_type == 10:
            action_new = self.am.getAddonId(action_new)
        action_name = self.am.getActionName(action_type, action_new)
        self.menu.setValue(self.index_menu, self.index_submenu, 'label', action_name)
        self.menu.setValue(self.index_menu, self.index_submenu, 'action', action_new)
        self.menu.setValue(self.index_menu, self.index_submenu, 'thumb', thumb_new)
        self.reloadMenu()
        self.setDetail()

    def newElement(self):
        self.menu.newElement(self.index_menu, self.index_submenu)
        if self.index_submenu == -1:
            self.index_menu = self.index_menu + 1
        else:
            self.index_submenu = self.index_submenu + 1
        self.reloadMenu()
        self.setDetail()
        self.setFocusId(207)

    def newSubmenu(self):
        self.menu.newSubmenu(self.index_menu)
        self.reloadMenu()
        self.showSubmenu()

    def deleteElement(self):
        dialog = xbmcgui.Dialog()
        header = ADDON.getLocalizedString(30112)
        content = ADDON.getLocalizedString(30113) + '?\n"' + self.menu.getLabel(self.index_menu, self.index_submenu) + '"'
        if  self.index_submenu == -1 and self.menu.hasSubmenu(self.index_menu):
            content += '\n\n' + ADDON.getLocalizedString(30114)
        ok = dialog.yesno(header, content)
        if not ok:
            return
        self.menu.deleteElement(self.index_menu, self.index_submenu)
        if self.index_submenu > -1 and not self.menu.hasSubmenu(self.index_menu):
            self.control_submenu.reset()
            self.index_submenu = -1
        self.reloadMenu()
        self.setDetail()
    
    def reset2Default(self):
        dialog = xbmcgui.Dialog()
        header = ADDON.getLocalizedString(30112)
        content = ADDON.getLocalizedString(30115)
        ok = dialog.yesno(header, content)
        if not ok:
            return
        self.menu.reset()
        self.index_menu = 0
        self.index_submenu = -1
        self.reloadMenu()
        self.setDetail()

    def thumbSize(self, next=False):
        thumbsize = int(self.menu.getValue(self.index_menu, self.index_submenu, 'thumbsize'))
        if next:
            thumbsize = (thumbsize+1) % 3
        else:
            thumbsize = thumbsize - 1
            if thumbsize < 0:
                thumbsize = 2
        self.menu.setValue(self.index_menu, self.index_submenu, 'thumbsize', thumbsize)
        self.label_thumbsize.setLabel(self.am.thumbsizes[thumbsize])
        self.reloadMenu()
