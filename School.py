#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2014                                                    *  
#*   Thomas Gundermann <thomas@freecadbuch.de>                             * 
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

__title__="FreeCAD School API"
__author__ = "Thomas Gundermann"
__url__ = "http://www.freecadbuch.de"

import FreeCAD
if FreeCAD.GuiUp:
	import FreeCADGui
	FreeCADGui.updateLocale()

from SchoolPyramid import *
from SchoolPrism import *

