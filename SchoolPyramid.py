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

def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")


import FreeCAD,Draft,ArchComponent, DraftVecUtils
from FreeCAD import Vector
import math
import Draft, Part, FreeCAD, math, PartGui, FreeCADGui, PySide
from math import sqrt, pi, sin, cos, asin
from FreeCAD import Base

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
else:
    def translate(ctxt,txt):
        return txt

__title__="FreeCAD Pyramid"
__author__ = "thomas gundermann"
__url__ = "http://www.freecadbuch.de"

#---------------------

def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")


def vieleck(anz,size,hoehe): # regelmaesiges vieleck berechnen
	list1=[]
	for p in range(anz):
		punkt=( size*cos(2*math.pi *p/anz),size*sin(2*math.pi*p/anz),hoehe)
		list1.append(punkt)
	#	say(punkt)
	
	p=0
	punkt=( size*cos(2*math.pi *p/anz),size*sin(2*math.pi*p/anz),hoehe)
	list1.append(punkt)
#	say(list1)
	return list1

def gen_pyramidenstumpf(count=8,size_bottom = 60, size_top=20, height=60):

	list1=vieleck(count,size_bottom,0)
	list2=vieleck(count,size_top,height)
	
	poly1 = Part.makePolygon( list1)
	poly2 = Part.makePolygon( list2)
	face1 = Part.Face(poly1)
	face2 = Part.Face(poly2)
	faceListe=[face1,face2]
	
	for i in range(len(list1)-1):
		liste3=[list1[i],list1[i+1],list2[i+1],list2[i],list1[i]]
		poly=Part.makePolygon(liste3)
		face = Part.Face(poly)
		faceListe.append(face)
	#	say(i);say(poly);say(faceListe)
	
	myShell = Part.makeShell(faceListe)   
	mySolid = Part.makeSolid(myShell)
	return mySolid

#----------------------
def makePyramid(count=6,size_bottom = 4, size_top=2, height=10,name=translate("Arch","Pyramid")):
    '''makePyramid(baseobj,[facenr],[angle],[name]) : Makes a Pyramid based on a
    regular polygon with count(8) vertexes face and a name (default
    = Pyramid).'''
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
    _Pyramid(obj)
    _ViewProviderPyramid(obj.ViewObject)
    obj.count=count
    obj.size_bottom=size_bottom
    obj.size_top=size_top
    obj.height=height
    return obj

class _CommandPyramid:
    "the School Pyramid command definition"
    def GetResources(self): 
		return {'Pixmap' :  'Mod/School/icons/pyramid.svg', 'MenuText': 'Pyramide', 'ToolTip': 'Erzeugt eine Pyramide fuer eine Grundflaeche'} 

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


    def Activated(self):
	if FreeCADGui.ActiveDocument:
		FreeCAD.ActiveDocument.openTransaction(translate("Arch","Create Pyramid"))
		FreeCADGui.doCommand("import School")
		FreeCADGui.doCommand("School.makePyramid()")
		FreeCAD.ActiveDocument.commitTransaction()
		FreeCAD.ActiveDocument.recompute()
	else:
		say("Erst Arbeitsbereich oeffnen")
	return
       
class _Pyramid(ArchComponent.Component):
    "The Pyramid object"

    def __init__(self,obj):
        ArchComponent.Component.__init__(self,obj)
        obj.addProperty("App::PropertyInteger","count","Base",
                        translate("Arch","Anzahl Ecken"))
        obj.addProperty("App::PropertyInteger","size_bottom","Base",
                        translate("Arch","Bodenmas"))
        obj.addProperty("App::PropertyInteger","size_top","Base",
                        translate("Arch","Deckelmas"))
        obj.addProperty("App::PropertyInteger","height","Base",
                        translate("Arch","hoch"))
        self.Type = "Pyramid"


    def execute(self,obj):
	obj.Shape=gen_pyramidenstumpf(obj.count,obj.size_bottom,obj.size_top,obj.height)

#---------------------------------- wozu dies #+#
    def getSubVolume(self,obj,extension=10000):
        "returns a volume to be subtracted"
        if hasattr(self,"baseface"):
            if self.baseface:
                norm = self.baseface.normalAt(0,0)
                norm = DraftVecUtils.scaleTo(norm,extension)
                return self.baseface.extrude(norm)
        return None
        

class _ViewProviderPyramid(ArchComponent.ViewProviderComponent):
    "A View Provider for the Pyramid object"

    def __init__(self,vobj):
#	say("__init")
#	say(self)
#	say(vobj)
# 		
        ArchComponent.ViewProviderComponent.__init__(self,vobj)

#    def getIcon(self):
#        import Arch_rc
#        return ":/icons/Arch_Pyramid_Tree.svg"
#        #return  App.getHomePath() +"Mod/icons/pyramid.svg'
#	#return {'Pixmap' :  App.getHomePath() +'/Mod/icons/pyramid.svg', 'MenuText': 'Line', 'ToolTip': 'Creates a line by clicking 2 points on the screen'} 



if FreeCAD.GuiUp:
    FreeCADGui.addCommand('School_Pyramid',_CommandPyramid())
