# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Map_Corners_Coordinates
                                 A QGIS plugin
 This plugin saves coordinates of corners of the selected map area.
                              -------------------
        begin                : 2016-10-12
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Kala_Kulovana
        email                : michael.kala193@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, Qt
from PyQt4.QtGui import QComboBox, QToolButton, QIcon, QAction, QFileDialog
# from qgis.gui import *
from qgis.core import QCoreApplication, QgsCoordinateTransform, QgsCoordinateReferenceSystem
from qgis.utils import QgsMessageBar


# Initialize Qt resources from file resources.py
import resources
import os
    
#import corners_tool
# Import the code for the dialog
from map_corners_coordinates_dialog import MapCornersCoordinatesDialog
import os.path
# from os.path import dirname, ...

class MapCornersCoordinates():
    
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface 
        """


        # Save reference to the QGIS interface        
        self.iface = iface
        
        self.canvas=iface.mapCanvas()

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Map_Corners_Coordinates_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the QDockWidget (after translation) and keep reference
        self.dlg = MapCornersCoordinatesDialog(self.iface.mainWindow())

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Map Corners Coordinates')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(self.tr(u'Map Corners Coordinates'))
        self.toolbar.setObjectName('MapCornersCoordinates')

        # Disable saveButton since there is no file chosen (method dirButton)
        self.dlg.saveButton.setEnabled(False)

        self.dlg.captureButton.clicked.connect(self.readCoor)
        self.dlg.saveButton.clicked.connect(self.saveCoor)
        
        # add plugin icon into plugin toolbar
        self.toolButton = QToolButton()
        self.iface.addToolBarWidget(self.toolButton)
        
        #save        
        self.dlg.dir_toolbutton.clicked.connect(self.dirButton)

    def tr(self, message):
        
        """Get the translation for a string using Qt translation API.
        
        We implement this ourselves since we do not inherit QObject.
        
        :param message: String for translation.
        :type message: str, QString
        
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Map_Corners_Coordinates', message)

    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
            
            
        """ Add a toolbar icon to the toolbar.
        
        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
            
        :type icon_path: str
        
        :param text: Text that should be shown in menu items for this action.
        
        :type text: unicode
        
        :param callback: Function to be called when the action is triggered.
        
        :type callback: function
        
        :param enabled_flag: A flag indicating if the action should be enabled
                by default. Defaults to True.
                
        :type enabled_flag: bool
        
        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
            
        :type add_to_menu: bool
        
        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
            
        :type add_to_toolbar: bool
        
        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
            
        :type status_tip: str
        
        :param parent: Parent widget for the new action. Defaults None.
        
        :type parent: QWidget
        
        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.
            
        :returns: The action that was created. Note that the action is also
            added to self.actions list.
            
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        
        self.toolButton.setDefaultAction(action)        
        
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            pass            
            #self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        
        icon_path = ':/plugins/Map_Corners_Coordinates/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Map Corners Coordinates'),
            callback=self.run,
            parent=self.iface.mainWindow())

    def unload(self):

        """Removes the plugin menu item and icon from QGIS GUI."""

        self.dlg.close()
        self.iface.removeDockWidget(self.dlg)

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Map_Corners_Coordinates'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def dirButton(self):
        
        """Gets the destination file, where captured coords are saved."""
        
        self.namedir = QFileDialog.getSaveFileName(self.dlg, self.tr(u"Select destination file"))
        self.dlg.dir_name.setText(self.namedir)
       
        # Enable the saveButton since file is chosen
        self.dlg.saveButton.setEnabled(True)        

    def readCoor(self):
        
        """Gets map canvas coords, writes them to corresponding widgets. 
           Transforms coords to EPSG:4326."""
        
        # Get map canvas extent (W, E, N, S)
        e = self.iface.mapCanvas().extent()
        
        # Transform the actual crs to EPSG:4326 if the actual crs is not EPSG:4326 itself 
        if self.dlg.system_box.currentText() == "EPSG:4326" and self.crs.authid() <> "EPSG:4326":
            crsSrc = QgsCoordinateReferenceSystem(str(self.crs.authid()))
            crsDest = QgsCoordinateReferenceSystem("EPSG:4326")
            tr = QgsCoordinateTransform(crsSrc,crsDest)
            e = tr.transform(e)
        
        self.dlg.coor_NEX.setText(str(e.xMaximum()))
        self.dlg.coor_NEY.setText(str(e.yMaximum()))
        self.dlg.coor_NWX.setText(str(e.xMinimum()))
        self.dlg.coor_NWY.setText(str(e.yMaximum()))
        self.dlg.coor_SEX.setText(str(e.xMaximum()))
        self.dlg.coor_SEY.setText(str(e.yMinimum()))
        self.dlg.coor_SWX.setText(str(e.xMinimum()))
        self.dlg.coor_SWY.setText(str(e.yMinimum()))

    def saveCoor(self):
        
        """Saves coords to file."""
        
        fileName = self.dlg.dir_name.text()
        if not fileName:
            self.iface.messageBar().pushMessage(self.tr(u"Error"),
                                                self.tr(u"No file given."),
                                                level=QgsMessageBar.CRITICAL, duration = 3)
            return
        
        try:
            f = open(fileName, 'w')
        except IOError as e:
            self.iface.messageBar().pushMessage("Error",
                                                "Unable open {} for writing. Reason: {}".format(fileName, e),
                                                level=QgsMessageBar.CRITICAL, duration = 3)
            return

        if not self.dlg.coor_NWX.text():
            self.iface.messageBar().pushMessage(self.tr(u"Error"),
                                                self.tr(u"No coordinates captured."),
                                                level=QgsMessageBar.CRITICAL, duration = 3)
            return
          
        f.write('''{title}
CRS: {crs}
NW (X): {nw_x}
NW (Y): {nw_y}
NE (X): {ne_x}
NE (Y): {ne_y}
SE (X): {se_x}
SE (Y): {se_y}
SW (X): {sw_x}
SW (Y): {sw_y}{ls}'''.format(title='Map Corners Coordinates',
                             crs=self.dlg.system_box.currentText(),
                             nw_x=self.dlg.coor_NWX.text(),
                             nw_y=self.dlg.coor_NWY.text(),
                             ne_x=self.dlg.coor_NEX.text(),
                             ne_y=self.dlg.coor_NEY.text(),
                             se_x=self.dlg.coor_SEX.text(),
                             se_y=self.dlg.coor_SEY.text(),
                             sw_x=self.dlg.coor_SWX.text(),
                             sw_y=self.dlg.coor_SWY.text(),
                             ls=os.linesep))
              
        f.close()
        self.iface.messageBar().pushMessage("Info",
                                            "File {} saved.".format(fileName),
                                            level=QgsMessageBar.INFO, duration = 3)

    def run(self):
        
        """Clears editable widgets. 
           Populates combo box with the actual crs and with EPSG:4326. """
           
        self.dlg.coor_NEX.clear()
        self.dlg.coor_NEY.clear()
        self.dlg.coor_NWX.clear()
        self.dlg.coor_NWY.clear()
        self.dlg.coor_SEX.clear()
        self.dlg.coor_SEY.clear()
        self.dlg.coor_SWX.clear()
        self.dlg.coor_SWY.clear()
        
        self.dlg.dir_name.clear()
        self.dlg.system_box.clear()
        
        # Declares the actual crs, latest versions of qgis does not support "mapRenderer()"
        try:
            self.crs = self.iface.mapCanvas().mapSettings().destinationCrs()
        except:
            self.crs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        
        if self.crs.authid() == "EPSG:4326":
            self.dlg.system_box.addItems([str(self.crs.authid())])
        else:
            self.dlg.system_box.addItems([str(self.crs.authid()),"EPSG:4326"])

        # dock dialog to the area on the left side
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dlg)

        # show the dialog
        self.dlg.show()

        # Disable saveButton for future plugin reopening
        self.dlg.saveButton.setEnabled(False)
