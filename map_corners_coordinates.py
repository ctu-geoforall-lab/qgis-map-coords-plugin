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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *
from qgis.utils import *


# Initialize Qt resources from file resources.py
import resources
import os
    
#import corners_tool
# Import the code for the dialog
from map_corners_coordinates_dialog import Map_Corners_CoordinatesDialog
import os.path


class Map_Corners_Coordinates():
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

        # Create the dialog (after translation) and keep reference
        self.dlg = Map_Corners_CoordinatesDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Map_Corners_Coordinates')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Map_Corners_Coordinates')
        self.toolbar.setObjectName(u'Map_Corners_Coordinates')

        self.dlg.pushButton.clicked.connect(self.read_coor)        
        
        # add plugin icon into plugin toolbar
        self.toolButton = QToolButton()
        self.iface.addToolBarWidget(self.toolButton)
        
        #save        
        self.dlg.dir_toolbutton.clicked.connect(self.dir_button)

   

    def tr(self, message):

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
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Map_Corners_Coordinates'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar
    

    def dir_button(self):
        self.namedir = QFileDialog.getExistingDirectory(self.dlg, "Select directory")
        self.dlg.dir_name.setText(self.namedir)


    def read_coor(self):
        e = self.iface.mapCanvas().extent()
        
        self.dlg.coor_NEX.setText(str(e.xMaximum()))
        self.dlg.coor_NEY.setText(str(e.yMaximum()))
        self.dlg.coor_NWX.setText(str(e.xMinimum()))
        self.dlg.coor_NWY.setText(str(e.yMaximum()))
        self.dlg.coor_SEX.setText(str(e.xMaximum()))
        self.dlg.coor_SEY.setText(str(e.yMinimum()))
        self.dlg.coor_SWX.setText(str(e.xMinimum()))
        self.dlg.coor_SWY.setText(str(e.yMinimum()))
        
        #save to txt
        text = self.dlg.coor_NEX.text()
        
        
      #  text = dlg.ui.coor_NEX.text()
        f = open("file.txt", 'w')
        print >>f, text
        f.close()
        
                
                
        canvas = self.iface.mapCanvas()
        mapRenderer = canvas.mapRenderer()
        srs=mapRenderer.destinationCrs()
        current_system = srs.authid()
        
        
 #       new_crs = QgsCoordinateReferenceSystem(4209)
 #       transform = QgsCoordinateTransform(current_system, new_crs)
 #       transform_points = transform.transform(QgsPoint(27.04892, -13.30552))        
        
        
        #save to txt
        text_NEX = self.dlg.coor_NEX.text()
        text_NEY = self.dlg.coor_NEY.text()        
        text_NWX = self.dlg.coor_NWX.text()
        text_NWY = self.dlg.coor_NWY.text()
        text_SEX = self.dlg.coor_SEX.text()
        text_SEY = self.dlg.coor_SEY.text()
        text_SWX = self.dlg.coor_SWX.text()
        text_SWY = self.dlg.coor_SWY.text()


  #      sel_dir = self.namedir + "/Map_Corners_Coordinates.txt"
        f = open("Map_Corners_Coordinates", 'w')
        print >>f, "Map Corners Coordinates\n-------------------------------------------\nCRS:",current_system,"\n-------------------------------------------"
        print >>f, "NW: X:",text_NWX,"  NE: X:",text_NEX,"\n","    Y:",text_NWY,"      Y:",text_NEY,"\nSW: X:",text_SWX,"  SE: X:",text_SEX,"\n","    Y:",text_SWY,"      Y:",text_SEY 
        f.close()
        
#        self.mapTool = RectangleMapTool(self.iface.mapCanvas())  

#        self.iface.mapCanvas().setMapTool(self.mapTool)   

    def dir_button(self):
        self.dirname = QFileDialog.getExistingDirectory(self.dlg, "Select directory ")
        self.dlg.dir_name.setText(self.dirname)
    
    def run(self):
        
        self.dlg.coor_NEX.clear()
        self.dlg.coor_NEY.clear()
        self.dlg.coor_NWX.clear()
        self.dlg.coor_NWY.clear()
        self.dlg.coor_SEX.clear()
        self.dlg.coor_SEY.clear()
        self.dlg.coor_SWX.clear()
        self.dlg.coor_SWY.clear()
        
        self.dlg.dir_name.clear()


        
        canvas = self.iface.mapCanvas()
        mapRenderer = canvas.mapRenderer()
        srs=mapRenderer.destinationCrs()
        current_system = str(srs.authid())
        
        self.dlg.system_box.clear()
        self.dlg.system_box.addItems([current_system,"EPSG:4326"])
        
        self.dlg.system_box.addItems([current_system])





        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        
        
        
        
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
#