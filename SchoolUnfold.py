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
import Draft, Part, FreeCAD, math, PartGui, FreeCADGui, PyQt4
from math import sqrt, pi, sin, cos, asin
from FreeCAD import Base

if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
else:
    def translate(ctxt,txt):
        return txt

__title__="FreeCAD Unfold"
__author__ = "thomas gundermann"
__url__ = "http://www.freecadbuch.de"

#---------------------

def say(s):
		FreeCAD.Console.PrintMessage(str(s)+"\n")

#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2013 - DoNovae/Herve BAILLY <hbl13@donovae.com>         *
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

#####################################
# Macro unfoldBox
#     Unroll of a ruled surface
#####################################
import FreeCAD , FreeCADGui , Part, Draft, math, Drawing , PyQt4, os
from PyQt4 import QtGui,QtCore
from FreeCAD import Base
fields_l = [] 
unroll_l = [] 

#####################################
#####################################
# Functions 
#####################################
#####################################

#####################################
# Function errorDialog 
#####################################
def errorDialog(msg):
    diag = QtGui.QMessageBox(QtGui.QMessageBox.Critical,u"Error Message",msg )
    diag.setWindowFlags(PyQt4.QtCore.Qt.WindowStaysOnTopHint)
    diag.exec_()


#####################################
# Function proceed 
#####################################
def proceed():
   QtGui.qApp.setOverrideCursor(QtCore.Qt.WaitCursor)

   FreeCAD.Console.PrintMessage("===========================================\n")
   FreeCAD.Console.PrintMessage("unfoldBox: start.\n")
  
   #
   # Get selection
   #
   
   sel=FreeCADGui.Selection.getSelection()
   # FreeCAD.sel=sel
 #  try: 
 #  	FreeCAD.sel
 #  except NameError:
 #       FreeCAD.Console.PrintMessage( "well, it WASN'T defined after all!")
#
 #       FreeCAD.sel=sel
  # else:
  #	FreeCAD.Console.PrintMessage( "sure, it was defined.")
   #     sel=FreeCAD.sel           	
   
   
   faceid=0
   objnames_l=[]
   tree_l=[]
   
   grp=FreeCAD.activeDocument().addObject("App::DocumentObjectGroup", "unfold") 
   
   for objid in range( sel.__len__() ):
     obj=Draft.clone(sel[objid])
     grp.addObject(obj)
     objnames_l.append( [ obj , sel[objid].Name ] )

   unfold=unfoldBox()
   sewed=True
   scale=1
   if sewed : 
        	 
       FreeCAD.Console.PrintMessage( "unfold .." + str(objnames_l))
       objnames_l=unfold.done(objnames_l)
       grp.addObject(objnames_l[0][0])
   else:
       for objid in range( objnames_l.__len__() ):
         unfold.moveXY(objnames_l[objid][0])
 

#   id=0
#   while objnames_l.__len__() > 0:
#       draw=Drawing2d( scale, scale_auto , a3 , cartridge , onedrawing , FreeCAD.activeDocument().Name , "Page"+str(id) ) 
#       objnames_l=draw.all( objnames_l )
#       id=id+1
#       FreeCAD.Console.PrintMessage("unfoldBox: obj_l= "+str(objnames_l.__len__())+"\n")

   FreeCAD.Console.PrintMessage("unfoldBox: end.\n")
   FreeCAD.Console.PrintMessage("===========================================\n")


#####################################
# Function close 
#####################################
def close():
   DialogBox.hide()

#####################################
# Class unfoldBox 
#####################################
class unfoldBox:
  #####################################
  # Function __init__ 
  #####################################
  def __init__(self):
     FreeCAD.Console.PrintMessage("unfoldBox.unfoldBox\n")
     self.LIMIT=0.0001


  #####################################
  # Function done 
  #####################################
  def done(self,objnames_l):
       tree_l=self.makeTree(objnames_l)
       ##FreeCAD.Console.PrintMessage(str(tree_l))
       FreeCAD.tt=tree_l;
       for id in range( objnames_l.__len__() ): 
         face=objnames_l[id]
         self.moveXY(face[0])
       self.sew( objnames_l , tree_l )
   
	
       return self.fusion(objnames_l)

    
  #####################################
  # Function makeTree 
  #####################################
  def makeTree(self,objnames_l):
     #
     # Initialisation of tree_l
     #
     tree_l=[]
     for k in range( objnames_l.__len__() ):
        facek=objnames_l[k][0]
        FreeCAD.Console.PrintMessage("Untersuche HAUPT--------------Flaeche " + str(k) + " "+ objnames_l[k][1] + "\n")
	facek_l=[]
	for i in range( facek.Shape.Edges.__len__() ):
	   FreeCAD.Console.PrintMessage("Untersuche kante " + str(i) + "\n")
	   if False and type(facek.Shape.Edges[i].Curve).__name__ != 'GeomLineSegment':
             facek_l.append([-2,-2])
	   else:
	     #
	     # Search face link to the ith edge
	     #
	     vki0=facek.Shape.Edges[i].Curve.StartPoint
	     vki1=facek.Shape.Edges[i].Curve.EndPoint
	     found=False
	     sameFace=False
##	     for l in range( k+1 , objnames_l.__len__() ):
	     for l in range( 0 , objnames_l.__len__() ):
               facel=objnames_l[l][0]
               FreeCAD.Console.PrintMessage("Untersuche flaeche " + str(l) + "  "+ objnames_l[l][1] + "\n")
               if l == k:
                    FreeCAD.Console.PrintMessage(str(l) +" " +str(k) + " l == k abbruch\n")
                    sameFace=True
                    continue	
               FreeCAD.Console.PrintMessage(str(l) +" " +str(k) + " weiter ..\n")     
	       for j in range( facel.Shape.Edges.__len__() ):
	            vlj0=facel.Shape.Edges[j].Curve.StartPoint
	            vlj1=facel.Shape.Edges[j].Curve.EndPoint
	            if vki0.__eq__(vlj0) and vki1.__eq__(vlj1): 
	                arelinked=False
	                isfacek=False
	                isfacel=False
	                for kk in range( k-1 ):
	                   for ii in range( tree_l[kk].__len__() ):
		              if tree_l[kk][ii][0]==k: isfacek=True
		              if tree_l[kk][ii][0]==l: isfacel=True
		           if isfacek and isfacel: 
		              arelinked=True 
		              FreeCAD.Console.PrintMessage("Verbinde nichmal mit " + str(l) +" " + str(j) +"\n")
                              facek_l.append([l,j])
                              FreeCAD.Console.PrintMessage("Ergebnis1  facek_l " + str(facek_l) +"\n")
                              found=True
		              break
			if not arelinked:
			  FreeCAD.Console.PrintMessage("Verbinde mit " + str(l) +" " + str(j) +"\n")
                          facek_l.append([l,j])
                          FreeCAD.Console.PrintMessage("Ergebnis2  facek_l " + str(facek_l) +"\n")
			  found=True
			  break
	            if found: break
	   if not found : 
	       facek_l.append([-1,-1])
	       FreeCAD.Console.PrintMessage("Hanege an ----------  -1-1 fuer  k=" +str(k) +"  l=" +str(k)      +"\n")  
	   FreeCAD.Console.PrintMessage("BIG Ergebnis  facek_l " + str(facek_l) +"\n")
        tree_l.append(facek_l) 
     FreeCAD.Console.PrintMessage("Ergebnis  tree_l " + str(tree_l) +"\n")
     return tree_l


  #####################################
  # Function sew 
  #####################################
  def sew( self,objnames_l , tree_l ):
   #
    for k in range( tree_l.__len__() ):
	for l in range( tree_l[k].__len__() ):
		if tree_l[k][l][0] != k+1 :
			tree_l[k][l] = [-1,-1]
  #
    FreeCAD.Console.PrintMessage("Ergebnis  tree_l in sew " + str(tree_l) +"\n")
    placed_l=[]
    for k in range( tree_l.__len__() ):
      FreeCAD.Console.PrintMessage("platziere " + str(k) + "\n")
      iskplaced=False
      for p in range( placed_l.__len__() ):
         if placed_l[p] == k:
            iskplaced=True 
      if not iskplaced:placed_l.append(k)
      facek=tree_l[k]
      objk=objnames_l[k][0]
      for i in range( facek.__len__() ):
        edgeki=facek[i]
        l=edgeki[0]
        j=edgeki[1]
	islplaced=False
	for p in range( placed_l.__len__() ):
	     if placed_l[p] == l: 
	        islplaced=True 
		break
	if not islplaced: placed_l.append(l)
        if l >= 0 and not ( islplaced and iskplaced ):
	  iskplaced=True
          #
  	  # Move facel.edgelj to facek.edgeki
  	  #
  	  FreeCAD.Console.PrintMessage("Move facel.edgelj to facek.edgeki  k:" + str(k) + " l:" +  str(l) + "\n")
  	  FreeCAD.Console.PrintMessage("Move facel.edgelj to facek.edgeki  k:" + str(objnames_l[k][1]) + " l:" +  str(objnames_l[l][1]) + "\n")
         
          objl=objnames_l[l][0]
          vki0=objk.Shape.Edges[i].Curve.StartPoint
          vki1=objk.Shape.Edges[i].Curve.EndPoint
	  vlj0=objl.Shape.Edges[j].Curve.StartPoint
	  vlj1=objl.Shape.Edges[j].Curve.EndPoint
	  vk=vki1.sub(vki0)
	  vl=vlj1.sub(vlj0)
	  alpk=vk.getAngle(vl)*180/math.pi
	  alpl=vl.getAngle(vk)*180/math.pi
          self.isPlanZ(objk)
	  if islplaced:
            Draft.move( objk , vlj0.sub(vki0) )
            FreeCAD.Console.PrintMessage("mvoe EEE"  + "\n")
	  else:
	    #if l == 4:   
	        	#objh1=Draft.clone(objl)
	        	#FreeCAD.Console.PrintMessage("First clone  " + str(objl.Name) + " -->"   +str(objh1.Name) + "\n")

            Draft.move( objl , vki0.sub(vlj0) )
            FreeCAD.Console.PrintMessage("mvoe FFF"  + "\n")

          self.isPlanZ(objk)

	  if math.fabs( vk.dot(FreeCAD.Base.Vector(-vl.y,vl.x,0))) > self.LIMIT:
	     if islplaced:
               Draft.rotate( objk , -alpl , vlj0 , self.vecto( vl , vk ))
               FreeCAD.Console.PrintMessage("rotate AAA"  + "\n")
	     else:
		#if l == 4:   
	        	#objh1=Draft.clone(objl)
	        	#FreeCAD.Console.PrintMessage("clone " + str(objl.Name) + " -->"   +str(objh1.Name) + "\n")	     
                Draft.rotate( objl , -alpk , vki0 , self.vecto( vk , vl ))
               	FreeCAD.Console.PrintMessage("rotate BBB"  + "\n")
	  elif vk.dot(vl)<0:
	     if islplaced:
               Draft.rotate( objk , 180 , vlj0 , self.vecto( vl , FreeCAD.Base.Vector(-vl.y,vl.x,0) ))
               FreeCAD.Console.PrintMessage("rotate CCC"  + "\n")
	     else:
               Draft.rotate( objl , 180 , vki0 , self.vecto( vk , FreeCAD.Base.Vector(-vk.y,vk.x,0)))
               FreeCAD.Console.PrintMessage("rotate DDD"  + "\n")
          #
	  # Verifications
	  #
          vki0=objk.Shape.Edges[i].Curve.StartPoint
          vki1=objk.Shape.Edges[i].Curve.EndPoint
	  vlj0=objl.Shape.Edges[j].Curve.StartPoint
	  vlj1=objl.Shape.Edges[j].Curve.EndPoint
	  vk=vki1.sub(vki0)
	  vl=vlj1.sub(vlj0)
          self.isPlanZ(objk)

	  #
	  # Flip or not
	  #
          L=max(objl.Shape.BoundBox.XMax,objk.Shape.BoundBox.XMax) - min( objl.Shape.BoundBox.XMin,objk.Shape.BoundBox.XMin) 
          W=max(objl.Shape.BoundBox.YMax,objk.Shape.BoundBox.YMax) - min( objl.Shape.BoundBox.YMin,objk.Shape.BoundBox.YMin) 
	  S1=L*W
	  if islplaced:
	    dum=0
            Draft.rotate( objk , 180 , vlj0 ,vl)
            FreeCAD.Console.PrintMessage("rotate GGGG"  + "\n")
	  else:
	    dum=0
	    #if l == 4:   
	    #    	objh1=Draft.clone(objl)
	    #    	FreeCAD.Console.PrintMessage("clone " + str(objl.Name) + " -->"   +str(objh1.Name) + "\n")	    
            Draft.rotate( objl , 180 , vki0 ,vk)
            FreeCAD.Console.PrintMessage("rotate HHHH"  + "\n")
          L=max(objl.Shape.BoundBox.XMax,objk.Shape.BoundBox.XMax) - min( objl.Shape.BoundBox.XMin,objk.Shape.BoundBox.XMin) 
          W=max(objl.Shape.BoundBox.YMax,objk.Shape.BoundBox.YMax) - min( objl.Shape.BoundBox.YMin,objk.Shape.BoundBox.YMin) 
	  S2=L*W
	  if (S2<=S1):
	     if islplaced:
	        dum=0
                Draft.rotate( objk , 180 , vlj0 ,vl)
                FreeCAD.Console.PrintMessage("rotate KKKKKK"  + "\n")
	     else:
	        dum=0
	        #if l == l:   
	        #	objh1=Draft.clone(objl)
	        #	FreeCAD.Console.PrintMessage("clone " + str(objl) + " -->"   +str(objh1) + "\n")
                Draft.rotate( objl , 180 , vki0 ,vk)
                FreeCAD.Console.PrintMessage("rotate LLLLLLL l="  + str(l)+ "\n")
          self.isPlanZ(objk)

  #####################################
  # Function isPlanZ 
  #####################################
  def isPlanZ(self,obj):
     L=obj.Shape.BoundBox.XMax - obj.Shape.BoundBox.XMin
     W=obj.Shape.BoundBox.YMax - obj.Shape.BoundBox.YMin
     H=obj.Shape.BoundBox.ZMax - obj.Shape.BoundBox.ZMin
     if H < self.LIMIT:
       return True
     else:
       return False


  #####################################
  # Function fusion 
  #####################################
  def fusion(self,objnames_l):
     #
     # Init
     #
     obj_l=[]
     objna_l=[]
     obj0=objnames_l[0][0];name=objnames_l[0][1]
     objfuse=FreeCAD.activeDocument().addObject("Part::MultiFuse","Unfolding")
     for k in range( objnames_l.__len__() ):
       objk=objnames_l[k][0]
       obj_l.append(objk)
     objfuse.Shapes=obj_l
     FreeCAD.activeDocument().recompute()
     objna_l.append([objfuse,name])
     return objna_l 

  #####################################
  # Function get2Vectors 
  #####################################
  def get2Vectors(self,shape):
    v0=FreeCAD.Base.Vector(0,0,0) 
    v1=FreeCAD.Base.Vector(0,0,0) 

    edges= shape.Edges
    for id in range( edges.__len__()-1):
       va=edges[id].Curve.EndPoint.sub(edges[id].Curve.StartPoint)
       vb=edges[id+1].Curve.EndPoint.sub(edges[id+1].Curve.StartPoint)
       if vb.sub(va).Length > v1.sub(v0).Length:
         v0=self.vect_copy(va);v1=self.vect_copy(vb)
    #FreeCAD.Console.PrintMessage("unfoldBox.get2Vectors: v0= {:s}, v1= {:s}\n".format(str(v0),str(v1)))
    return [ v0 , v1 ]

  #####################################
  # Function vecto 
  #   - vect1,2:  
  #   - return abs(sin) angle between 
  #     2 vectors 
  #####################################
  def vecto( self,vect1, vect2 ):
     v= FreeCAD.Base.Vector(0,0,0)
     v.x=vect1.y*vect2.z-vect1.z*vect2.y
     v.y=vect1.z*vect2.x-vect1.x*vect2.z
     v.z=vect1.x*vect2.y-vect1.y*vect2.x
     return v 


  #####################################
  # Function vect_copy 
  #   - vect:  
  #   - return copy of vector
  #####################################
  def vect_copy( self,vect):
     v= vect.add( FreeCAD.Base.Vector(0,0,0) )
     return v 


  #####################################
  # Function movexy 
  #####################################
  def moveXY( self,obj ):
     #
     # Move to origin
     #
     Draft.move( obj , FreeCAD.Base.Vector( -obj.Shape.BoundBox.XMin , -obj.Shape.BoundBox.YMin , -obj.Shape.BoundBox.ZMin ))
     #
     # Find 2 vectors defining the plan of surface
     #
     tab=self.get2Vectors( obj.Shape )
     v0=tab[0];v1=tab[1]
     norm=self.vecto(v0,v1)
     norm.normalize()
     #FreeCAD.Console.PrintMessage("unfoldBox.moveXY: norm= {:s}\n".format(str(norm)))

     #
     # Rotate
     #
     if math.fabs(norm.x) < self.LIMIT and math.fabs(norm.y) < self.LIMIT:
        dum=0
     elif math.fabs(norm.x) < self.LIMIT and math.fabs(norm.z) < self.LIMIT:
        Draft.rotate( obj , 90 , FreeCAD.Base.Vector(0,0,0) , FreeCAD.Base.Vector(1,0,0) )
     elif math.fabs(norm.y) < self.LIMIT and math.fabs(norm.z) < self.LIMIT:
        Draft.rotate( obj , 90 , FreeCAD.Base.Vector(0,0,0) , FreeCAD.Base.Vector(0,1,0) )
     else:
	#
	# Rotate following the angle to the normal direction of the plan
	#
        oz= FreeCAD.Base.Vector(0,0,1)
	alp=oz.getAngle(norm)*180/math.pi
        #FreeCAD.Console.PrintMessage("unfoldBox.moveXY: alp= "+str(alp)+"\n")
        #FreeCAD.Console.PrintMessage("unfoldBox.moveXY: vecto= {:s}\n".format(str(self.vecto(oz,norm))))
        Draft.rotate( obj , -alp , FreeCAD.Base.Vector(0,0,0) , self.vecto( oz, norm ))
     #
     # Move to z=0
     #
     Draft.move( obj , FreeCAD.Base.Vector( 0 , 0 , -obj.Shape.BoundBox.ZMin ))
     L=obj.Shape.BoundBox.XMax - obj.Shape.BoundBox.XMin
     W=obj.Shape.BoundBox.YMax - obj.Shape.BoundBox.YMin
     H=obj.Shape.BoundBox.ZMax - obj.Shape.BoundBox.ZMin


#####################################
# Class Drawing2d 
#####################################
class Drawing2d:
  #####################################
  # Function __init__ 
  #     - Scale
  #     - scale_auto
  #     - a3
  #     - cartridge
  #     - onedrawing
  #####################################
  def __init__( self,  scale , scale_auto , a3 , cartridge , onedrawing , drawing_name , page_name ):
    self.TopX_H=0
    self.TopY_H=0
    self.TopX_V=0
    self.TopY_V=0
    self.TopX_Hmax=0
    self.TopY_Hmax=0
    self.TopX_Vmax=0
    self.TopY_Vmax=0
    self.a3=a3
    self.pts_nbr=100
    self.scale=scale
    self.scale_auto=scale_auto
    self.cartridge=cartridge
    self.onedrawing=onedrawing
    if self.a3:
      self.L=420
      self.H=297
      self.marge=6
    else:
      self.L=297
      self.H=210
      self.marge=6
    self.page_name=page_name
    self.drawing_name=drawing_name

  #####################################
  # Function newPage 
  #####################################
  def newPage( self ):
    freecad_dir=os.getenv('HOME')+"/.FreeCAD/Mod/unfoldBox"
    page = FreeCAD.activeDocument().addObject('Drawing::FeaturePage', self.page_name )
    if self.a3:
        if self.cartridge:
           page.Template = freecad_dir+'/A3_Landscape.svg'   
        else:
           page.Template = freecad_dir+'/A3_Landscape_Empty.svg'   
    else:
        if self.cartridge:
           page.Template = freecad_dir+'/A4_Landscape.svg'   
        else:
           page.Template = freecad_dir+'/A4_Landscape_Empty.svg'   
    return page

  #####################################
  # Function all 
  #####################################
  def all( self, objnames_l ):
      obj_l=[]
      for objid in range( objnames_l.__len__() ):
        if objid == 0 or not self.onedrawing:
          page = self.newPage()
        obj_l.extend( self.done( objid , objnames_l[objid] ))
      return obj_l 




  #####################################
  # Function done 
  #####################################
  def done( self, id , objname ):
    #
    # Init
    #
    obj_l=[]
    obj=objname[0]
    objname=objname[1]
    xmax=obj.Shape.BoundBox.XMax-obj.Shape.BoundBox.XMin
    ymax=obj.Shape.BoundBox.YMax-obj.Shape.BoundBox.YMin
    if ymax > xmax :
      Draft.rotate( obj , 90 )
    Draft.move( obj , FreeCAD.Base.Vector( -obj.Shape.BoundBox.XMin , -obj.Shape.BoundBox.YMin , 0))
    xmax=obj.Shape.BoundBox.XMax-obj.Shape.BoundBox.XMin
    ymax=obj.Shape.BoundBox.YMax-obj.Shape.BoundBox.YMin

    scale=min((self.L-4*self.marge)/xmax,(self.H-4*self.marge)/ymax)

    if ( not self.scale_auto ) or ( self.onedrawing ) :
       scale=self.scale


    if id == 0 or not self.onedrawing:
      #
      # Init
      #
      FreeCAD.Console.PrintMessage("Dawing2d: init\n")
      self.TopX_H=self.marge*2
      self.TopY_H=self.marge*2
      TopX=self.TopX_H
      TopY=self.TopY_H
      self.TopX_H=self.TopX_H + xmax * scale + self.marge
      self.TopY_H=self.TopY_H 
      self.TopX_Hmax=max( self.TopX_Hmax , self.TopX_H )
      self.TopY_Hmax=max( self.TopY_Hmax , self.TopY_H + ymax*scale+self.marge )
      self.TopX_Vmax=max( self.TopX_Vmax , self.TopX_Hmax )
      self.TopX_V=max(self.TopX_Vmax,self.TopX_V)
      self.TopY_V=self.marge*2
    elif self.onedrawing:
      if self.TopX_H + xmax * scale < self.L :
        if self.TopY_H + ymax * scale + self.marge*2 < self.H :
	   #
	   # H Add at right on same horizontal line
	   #
           FreeCAD.Console.PrintMessage("Dawing2d: horizontal\n")
           TopX=self.TopX_H
           TopY=self.TopY_H
           self.TopX_H=self.TopX_H + xmax * scale + self.marge
	   self.TopX_Hmax=max( self.TopX_Hmax , self.TopX_H )
	   self.TopY_Hmax=max( self.TopY_Hmax , self.TopY_H + ymax*scale+self.marge )
	   self.TopX_Vmax=max( self.TopX_Hmax , self.TopX_Vmax )
           self.TopX_Vmax=max( self.TopX_Vmax , self.TopX_Hmax  )
           self.TopX_V=max(self.TopX_Vmax,self.TopX_V)
	else:
	   #
	   # V Add at right on same horizontal line
	   #
           FreeCAD.Console.PrintMessage("Dawing2d: vertival\n")
           if self.TopX_V + ymax * scale +2* self.marge < self.L and self.TopY_V + xmax * scale + 2*self.marge < self.H :
             Draft.rotate( obj , 90 )
	     Draft.move( obj , FreeCAD.Base.Vector( -obj.BoundBox.XMin , -obj.BoundBox.YMin , 0))
             self.TopX_V=max(self.TopX_Vmax, self.TopX_V)
             TopX=self.TopX_V
             TopY=self.TopY_V
	     self.TopX_V = self.TopX_V + ymax * scale + self.marge
	     self.TopY_Vmax=max( self.TopY_Vmax , self.TopY_V + xmax * scale + self.marge )
	   else:
	     obj_l.append( [ obj , name ] )
	     return obj_l

      else:
	#
	# H Carriage return 
	#
        if ( self.TopY_Hmax + ymax * scale + self.marge*2 < self.H ):   
           FreeCAD.Console.PrintMessage("Dawing2d: carriage return: "+str(self.TopY_H + ymax * scale )+" > "+str(self.H)+"\n")
           TopX=self.marge*2
           TopY=self.TopY_Hmax
           self.TopX_H=TopX + xmax * scale + self.marge
           self.TopY_H=TopY 
	   self.TopX_Hmax=max( self.TopX_Hmax , self.TopX_H )
	   self.TopY_Hmax=self.TopY_Hmax + ymax*scale+self.marge
           self.TopX_Vmax=max( self.TopX_Vmax , self.TopX_Hmax )
           self.TopX_V=max(self.TopX_Vmax,self.TopX_V)
	else:
	   #
	   # V Add at right on same horizontal line
	   #
           FreeCAD.Console.PrintMessage("Dawing2d: vertival: "+str(self.TopX_V)+" , "+str(self.TopX_Vmax)+"\n")
           if self.TopX_V + ymax * scale + 2*self.marge < self.L and self.TopY_V + xmax * scale + 2*self.marge < self.H :
             Draft.rotate( obj , 90 )
	     Draft.move( obj , FreeCAD.Base.Vector( -obj.BoundBox.XMin , -obj.BoundBox.YMin , 0))
             TopX=self.TopX_V
             TopY=self.TopY_V
	     self.TopX_V = self.TopX_V + ymax * scale + self.marge
	     self.TopY_Vmax=max( self.TopY_Vmax , self.TopY_V + xmax * scale + self.marge )
	   else:
	     obj_l.append( [ obj , name ] )
	     return obj_l

    page=FreeCAD.activeDocument().getObject(self.page_name )

    Text=FreeCAD.activeDocument().addObject('Drawing::FeatureViewAnnotation', objname+"_txt")
    Text.Text=objname
    Text.X=TopX+xmax/2*scale
    Text.Y=TopY+ymax/2*scale
    Text.Scale=1

    TopView = FreeCAD.activeDocument().addObject('Drawing::FeatureViewPart','TopView')
    TopView.Source = obj
    TopView.Direction = (0.0,0.0,1)
    TopView.Rotation = 0 
    TopView.X = TopX 
    TopView.Y = TopY 
    TopView.ShowHiddenLines = True
    TopView.Scale = scale 
    page.addObject(TopView)
    page.addObject(Text)
    FreeCAD.activeDocument().recompute()
    
  
    
    
    return obj_l




#####################################
#####################################
# Dialog Box 
#####################################
#####################################

def myunfold():
	fields = [[ "Group Name" , "Unfolding" ]]
	fields.append(["Scale","1" ])

	DialogBox = QtGui.QDialog()
	DialogBox.resize(250,250)
	DialogBox.setWindowTitle("unfoldBox")
	la = QtGui.QVBoxLayout(DialogBox)

	#
	# Input fields
	#
	for id in range(len( fields )):
	  la.addWidget(QtGui.QLabel( fields[ id ][ 0 ] ))
	  fields_l.append( QtGui.QLineEdit( fields[ id ][ 1 ] ))
	  la.addWidget( fields_l[ id ] )

	scale_check = QtGui.QCheckBox( DialogBox )
	scale_check.setObjectName("checkBox")
	scale_check.setChecked(True)
	la.addWidget(QtGui.QLabel("Scale auto"))
	la.addWidget(scale_check)

	a3_check = QtGui.QCheckBox( DialogBox )
	a3_check.setObjectName("checkBox")
	la.addWidget(QtGui.QLabel("A3 Format"))
	a3_check.setChecked(False)
	la.addWidget(a3_check)

	cartridge_check = QtGui.QCheckBox( DialogBox )
	cartridge_check.setObjectName("checkBox")
	la.addWidget(QtGui.QLabel("Cartridge"))
	cartridge_check.setChecked(False)
	la.addWidget(cartridge_check)

	onedrawing_check = QtGui.QCheckBox( DialogBox )
	onedrawing_check.setObjectName("checkBox")
	la.addWidget(QtGui.QLabel("Group drawings in page"))
	onedrawing_check.setChecked(True)
	la.addWidget(onedrawing_check)

	sewed_check = QtGui.QCheckBox( DialogBox )
	sewed_check.setObjectName("checkBox")
	la.addWidget(QtGui.QLabel("Sewed surfaces"))
	sewed_check.setChecked(True)
	la.addWidget(sewed_check)

	box = QtGui.QDialogButtonBox(DialogBox)

	box = QtGui.QDialogButtonBox(DialogBox)
	box.setOrientation(QtCore.Qt.Horizontal)
	box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
	la.addWidget(box)

	QtCore.QObject.connect(box, QtCore.SIGNAL("accepted()"), proceed )
	QtCore.QObject.connect(box, QtCore.SIGNAL("rejected()"), close )
	QtCore.QMetaObject.connectSlotsByName(DialogBox)
	DialogBox.show()






#---------------------

class _CommandUnfold:
    "the School Unfold command definition"
    def GetResources(self): 
	App=FreeCAD
	return {'Pixmap' :  App.getHomePath() +'/Mod/School/icons/unfold.svg', 'MenuText': 'Unfold', 'ToolTip': 'Erzeugt Abwicklung fuer Flaechen'} 

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


    def Activated(self):
	if FreeCADGui.ActiveDocument:
		FreeCAD.ActiveDocument.openTransaction(translate("Arch","Create Unfold"))
		FreeCADGui.doCommand("import School")
#		FreeCADGui.doCommand("School.makeUnfold()")


# 		myunfold()
		proceed()




#
		FreeCAD.ActiveDocument.commitTransaction()
		FreeCAD.ActiveDocument.recompute()
	else:
		say("Erst Arbeitsbereich oeffnen")
	return
       
class _Unfold(ArchComponent.Component):
    "The Unfold object"

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
        self.Type = "Unfold"


    def execute(self,obj):
	obj.Shape=gen_Unfoldenstumpf(obj.count,obj.size_bottom,obj.size_top,obj.height)

#---------------------------------- wozu dies #+#
    def getSubVolume(self,obj,extension=10000):
        "returns a volume to be subtracted"
        if hasattr(self,"baseface"):
            if self.baseface:
                norm = self.baseface.normalAt(0,0)
                norm = DraftVecUtils.scaleTo(norm,extension)
                return self.baseface.extrude(norm)
        return None
        

class _ViewProviderUnfold(ArchComponent.ViewProviderComponent):
    "A View Provider for the Unfold object"

    def __init__(self,vobj):
#	say("__init")
#	say(self)
#	say(vobj)
# 		
        ArchComponent.ViewProviderComponent.__init__(self,vobj)

#    def getIcon(self):
#        import Arch_rc
#        return ":/icons/Arch_Unfold_Tree.svg"
#        #return  App.getHomePath() +"Mod/icons/Unfold.svg'
#	#return {'Pixmap' :  App.getHomePath() +'/Mod/icons/Unfold.svg', 'MenuText': 'Line', 'ToolTip': 'Creates a line by clicking 2 points on the screen'} 



if FreeCAD.GuiUp:
    FreeCADGui.addCommand('School_Unfold',_CommandUnfold())
