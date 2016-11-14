# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Map_Corners_Coordinates
                                 A QGIS plugin
 This plugin saves coordinates of corners of the selected map area.
                             -------------------
        begin                : 2016-10-12
        copyright            : (C) 2016 by Kala_Kulovana
        email                : michael.kala193@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Map_Corners_Coordinates class from file Map_Corners_Coordinates.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .map_corners_coordinates import MapCornersCoordinates
    return MapCornersCoordinates(iface)
