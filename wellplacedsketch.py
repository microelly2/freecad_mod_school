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

import FreeCAD
import FreeCADGui
import Part
from PySide import QtGui, QtCore

from numpy import *
from math import sqrt

def Dprint(arg):
	DEBUG=0
	if DEBUG:
		FreeCAD.Console.PrintMessage(str(arg)+ "\n")

class wellPlacedSketch:
	
	def IsActive(self):
		MouseSel = FreeCADGui.Selection.getSelectionEx()
		Selected_Points = []
		for i in range(len(MouseSel)):
			Sel_i_Object = MouseSel[i]
			SubObjects_Inside = Sel_i_Object.SubObjects
			for n in range(len(SubObjects_Inside)):
				SubObject = SubObjects_Inside[n]
				if SubObject.ShapeType == "Vertex":
					Selected_Points.append(SubObject)
		Number_of_Points = len(Selected_Points)
		if Number_of_Points == 3:
			return True
		else:
			return False

	def Activated(self):
		TEST=0
		if TEST:
			v1=FreeCAD.Vector (20, 10, 10.0)
			v2=FreeCAD.Vector (30, 10 ,10 )
			v3=FreeCAD.Vector (25,15, 10)
			ps=[v1,v2,v1,v3,v2,v3]
			p=Part.makePolygon(ps)
			Part.show(p)
			self.ff(v1,v2,v3)
		else:
			self.main()  

	def GetResources(self): 
		return {'Pixmap' : '/home/tog/freecad_buch/45_MOD_Freek/icons/wellplacedsketch.png', 'MenuText': 'Well placed Sketch', 'ToolTip': 'Sketch angeordnet'} 

	def ff(self,p1,p2,p3):
		base=FreeCAD.Vector(p1)
		a=p2.sub(p1)
		Dprint(a)
		la=FreeCAD.Vector(a).Length
		
		Dprint("la " + str(la) )
		b=p3.sub(p1)
		lb=FreeCAD.Vector(b).Length
		a.normalize()
		Dprint ("a " + str(a))

		b.normalize()
		Dprint ("b " + str(b))

		wb=arccos(a.dot(b))

		c=b.cross(a).normalize()

		Dprint ("c " + str(c))

		gier1=arctan2(a.y,a.x)
		gier=gier1*180/3.14
		Dprint("gier:");Dprint(gier)

		r=sqrt(a.x*a.x + a.y*a.y)
		steig1=arctan2(a.z,r)
		steig=-steig1*180/3.14
		Dprint("steig");Dprint(steig)

		gier1=-gier1
		b2=FreeCAD.Vector(b.x*cos(gier1)-b.y*sin(gier1), b.x*sin(gier1)+b.y*cos(gier1),b.z)
		Dprint("b2");	Dprint(b2)

		steig1=-steig1
		b3=FreeCAD.Vector(b2.x*cos(steig1)-b2.z*sin(steig1), b2.y,b2.x*sin(steig1)+b2.z*cos(steig1))
		Dprint("b3");	Dprint(b3)

		roll1=arctan2(b3.z,b3.y)
		roll=-roll1*180/3.14
		Dprint("roll"); 	Dprint(roll)

		rot=FreeCAD.Rotation(gier,steig,-roll)
		App=FreeCAD
		Dprint("wb") ;Dprint(wb)
		sk=FreeCAD.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		sk.addGeometry(Part.Line(App.Vector(0.000000,0.000000,0),App.Vector(la,0.000000,0)))
	#	sk.addGeometry(Part.Line(App.Vector(0.000000,lb,0),App.Vector(0.000000,0.000000,0)))
		sk.addGeometry(Part.Line(App.Vector(lb*cos(wb),lb*sin(wb),0),App.Vector(0.000000,0.000000,0)))
		sk.Placement=FreeCAD.Placement(base,rot)
		App.ActiveDocument.recompute()

	def main(self):
	   MouseSel = FreeCADGui.Selection.getSelectionEx()
	   Selected_Points = []
	   Selected_Edges = []
	   Selected_Planes = []
	   for i in range(len(MouseSel)):
		  Sel_i_Object = MouseSel[i]
		  SubObjects_Inside = Sel_i_Object.SubObjects
		  for n in range(len(SubObjects_Inside)):
			SubObject = SubObjects_Inside[n]
			if SubObject.ShapeType == "Vertex":
			  Selected_Points.append(SubObject)
	   Number_of_Points = len(Selected_Points)
	   print Number_of_Points
	   if Number_of_Points == 3:
		  self.ff(Selected_Points[0].Point,Selected_Points[1].Point,Selected_Points[2].Point)
	   else:
		  Dprint ("Geht nicht")


FreeCADGui.addCommand(' wellPlacedSketch',  wellPlacedSketch())
