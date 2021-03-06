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

__title__="FreeCAD School tools"
__author__ = "thomas gundermann"
__url__ = "http://www.freecadbuch.de"

#---------------------


from PySide import QtCore, QtGui

def errorDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Information,"Fehler ",msg )
    diag.exec_()


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

def gen_Prismenstumpf(count=8,size_bottom = 60,  height=60):

	list1=vieleck(count,size_bottom,0)
	list2=vieleck(count,size_bottom,height)
	
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
def makePrism(count=8,size_bottom = 60, height=60,name=translate("Arch","Prism")):
    '''makePrism(baseobj,[facenr],[angle],[name]) : Makes a Prism based on a
    regular polygon with count(8) vertexes face and a name (default
    = Prism).'''
    obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",name)
    _Prism(obj)
    _ViewProviderPrism(obj.ViewObject)
    obj.count=count
    obj.size_bottom=size_bottom
    obj.height=height
    return obj

class _CommandPrism:
    "the School Prism command definition"
    def GetResources(self): 

		return {'Pixmap' :  'Mod/School/icons/prism.svg', 'MenuText': 'Prisme', 'ToolTip': 'Erzeugt eine Prisme fuer eine Grundflaeche'} 

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


    def Activated(self):
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction(translate("Arch","Create Prism"))
			FreeCADGui.doCommand("import School")
			FreeCADGui.doCommand("School.makePrism()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			say("Erst Arbeitsbereich oeffnen")
		return
       
class _Prism(ArchComponent.Component):
    "The Prism object"

    def __init__(self,obj):
        ArchComponent.Component.__init__(self,obj)
        obj.addProperty("App::PropertyInteger","count","Base",
                        translate("Arch","Anzahl Ecken"))
        obj.addProperty("App::PropertyInteger","size_bottom","Base",
                        translate("Arch","Bodenmas"))
        obj.addProperty("App::PropertyInteger","height","Base",
                        translate("Arch","hoch"))
        self.Type = "Prism"


    def execute(self,obj):
	obj.Shape=gen_Prismenstumpf(obj.count,obj.size_bottom,obj.height)

#---------------------------------- wozu dies #+#
    def getSubVolume(self,obj,extension=10000):
        "returns a volume to be subtracted"
        if hasattr(self,"baseface"):
            if self.baseface:
                norm = self.baseface.normalAt(0,0)
                norm = DraftVecUtils.scaleTo(norm,extension)
                return self.baseface.extrude(norm)
        return None
        

class _ViewProviderPrism(ArchComponent.ViewProviderComponent):
    "A View Provider for the Prism object"

    def __init__(self,vobj):
#	say("__init")
#	say(self)
#	say(vobj)
# 		
        ArchComponent.ViewProviderComponent.__init__(self,vobj)

#    def getIcon(self):
#        import Arch_rc
#        return ":/icons/Arch_Prism_Tree.svg"
#        #return  App.getHomePath() +"Mod/icons/Prism.svg'
#	#return {'Pixmap' :  App.getHomePath() +'/Mod/icons/Prism.svg', 'MenuText': 'Line', 'ToolTip': 'Creates a line by clicking 2 points on the screen'} 



class _CommandModTool:
    "the School Modify Tool command definition"
    def GetResources(self): 
		return {'Pixmap' :  'Mod/School/icons/mod_tool.svg', 'MenuText': 'Mod Tool', 'ToolTip': 'Aendert Tool eines Cut'} 


    def IsActive(self):
        return True
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


    def Activated(self):

		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction(translate("Arch","Create Prism"))

			t=FreeCADGui.Selection.getSelection()
			if len(t)<>2:
				errorDialog("Zwei Objekte auswaehlen!")
				raise NameError("Anzahl selektierter Objekte muss 2 sein"  )	
			try:
				b=t[0].Tool
				g=FreeCADGui.ActiveDocument
				tt=g.getObject(b.Name)
				##tt.Visibility=True
				t[0].Tool=t[1]
			except:
			#	try:
				if 1:
					h=t[0].Shapes
					b=h.pop(1)
					FreeCAD.t=b
					say(b.Label)
					g=FreeCADGui.ActiveDocument
					tt=g.getObject(b.Name)
					##tt.Visibility=True
					h.append(t[1])
					t[0].Shapes=h

			#	except:
			#		errorDialog("Erstes Objekt muss ein  Cut, Intersection-Objekt mit Base-Attribut sein ")
			#		raise NameError("Erstes Objekt muss ein Fusion, Cut, Intersection-Objekt mit Base-Attribut sein ")


			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			pass
			#say("Erst Arbeitsbereich oeffnen")
		return

class _CommandModBase:
    "the School Modify Tool command definition"
    def GetResources(self): 
		return {'Pixmap' :  '/Mod/School/icons/mod_base.svg', 'MenuText': 'Mod Base', 'ToolTip': 'Aendert Base bei Cut-Objekt'} 


    def IsActive(self):
        return True
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


    def Activated(self):

		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction(translate("Arch","Create Prism"))
#			FreeCADGui.doCommand("import School")
#			FreeCADGui.doCommand("School.makePrism()")
#----------------------------

			t=FreeCADGui.Selection.getSelection()
			if len(t)<>2:
				errorDialog("Zwei Objekte auswaehlen!")
				raise NameError("Anzahl selektierter Objekte muss 2 sein"  )

			try:
				b=t[0].Base
				g=FreeCADGui.ActiveDocument
				tt=g.getObject(b.Name)
				##tt.Visibility=True
				t[0].Base=t[1]
			except:
				try:
					h=t[0].Shapes
					b=h.pop(0)
					say(b.Label)
					g=FreeCADGui.ActiveDocument
					tt=g.getObject(b.Name)
					##tt.Visibility=True
					h.append(t[1])
					t[0].Shapes=h
				except:
					errorDialog("Erstes Objekt muss ein  Cut, Intersection-Objekt mit Base-Attribut sein ")
					raise NameError("Erstes Objekt muss ein Fusion, Cut, Intersection-Objekt mit Base-Attribut sein ")


#-------------------------------

			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			pass
			say("Erst Arbeitsbereich oeffnen")
		return


class _CommandModMembers:
    "the School Modify Tool command definition"
    def GetResources(self): 
	App=FreeCAD
	return {'Pixmap' :  App.getHomePath() +'/Mod/School/icons/mod_members.svg', 'MenuText': 'Mod Members', 'ToolTip': 'Aendert Mitglieder eines Fuse oder Common'} 

    def IsActive(self):
        return True
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


    def Activated(self):
		say("sorry, not implemented yet")
		if FreeCADGui.ActiveDocument:
			FreeCAD.ActiveDocument.openTransaction(translate("Arch","Create Prism"))
#			FreeCADGui.doCommand("import School")
#			FreeCADGui.doCommand("School.makePrism()")
			FreeCAD.ActiveDocument.commitTransaction()
			FreeCAD.ActiveDocument.recompute()
		else:
			pass
#			say("Erst Arbeitsbereich oeffnen")
		return










if FreeCAD.GuiUp:
   FreeCADGui.addCommand('School_Mod_Base',_CommandModBase())
   # FreeCADGui.addCommand('School_Mod_Tool',_CommandModTool())
   # FreeCADGui.addCommand('School_Mod_Members',_CommandModMembers())
   pass
