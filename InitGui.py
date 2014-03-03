#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2014                                                    *  
#*   Thomas Gundermann <thomas@freecadbuch.de>                             * 
#*   this file is based on the code and the ideas                          *   
#*   of the freecad arch module developed by Yorik van Havre               *
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

#
#  anpassung fuer schule, 28.02.2014 th. gundermann
#

class SchoolWorkbench(Workbench):
    "Student workbench object"
    Icon = """
/* XPM */
static char * school_xpm[] = {
"16 16 211 2",
"  	c #EE1D1C",
". 	c #ED1919",
"+ 	c #EE1C1B",
"@ 	c #ED2221",
"# 	c #EC2C28",
"$ 	c #E93A32",
"% 	c #DF5341",
"& 	c #CB774F",
"* 	c #AC9A52",
"= 	c #87BB4F",
"- 	c #66D447",
"; 	c #48EE41",
"> 	c #39F339",
", 	c #38F338",
"' 	c #37F337",
") 	c #40F440",
"! 	c #ED1716",
"~ 	c #ED1817",
"{ 	c #ED1A19",
"] 	c #EC2320",
"^ 	c #E92D26",
"/ 	c #E04232",
"( 	c #CD603C",
"_ 	c #AE8945",
": 	c #8BAC44",
"< 	c #64CB3D",
"[ 	c #4AE239",
"} 	c #38EE33",
"| 	c #32F332",
"1 	c #34F334",
"2 	c #3DF43D",
"3 	c #ED1615",
"4 	c #EC1E1C",
"5 	c #E92923",
"6 	c #E23A2C",
"7 	c #D15535",
"8 	c #B47B3E",
"9 	c #8FA03E",
"0 	c #6AC33A",
"a 	c #4DDE37",
"b 	c #38ED33",
"c 	c #33F333",
"d 	c #36F336",
"e 	c #ED1B1A",
"f 	c #EC1D1B",
"g 	c #E92721",
"h 	c #E3372A",
"i 	c #D35234",
"j 	c #B9733B",
"k 	c #969B3F",
"l 	c #74BF40",
"m 	c #54D93A",
"n 	c #40EB38",
"o 	c #3DF13A",
"p 	c #47F447",
"q 	c #EE2120",
"r 	c #EC201D",
"s 	c #E4392D",
"t 	c #D75339",
"u 	c #BF7542",
"v 	c #A19846",
"w 	c #7EBD48",
"x 	c #61D947",
"y 	c #4DEC45",
"z 	c #48F145",
"A 	c #4BF44B",
"B 	c #57F557",
"C 	c #ED2D2A",
"D 	c #EC2522",
"E 	c #EC221F",
"F 	c #EB231F",
"G 	c #EA2823",
"H 	c #E8312A",
"I 	c #E34336",
"J 	c #D85E44",
"K 	c #C47F50",
"L 	c #AAA056",
"M 	c #8BC45B",
"N 	c #72DC59",
"O 	c #62ED5A",
"P 	c #5FF35C",
"Q 	c #61F661",
"R 	c #71F771",
"S 	c #E93F38",
"T 	c #E8342D",
"U 	c #E82F28",
"V 	c #E83129",
"W 	c #E7352C",
"X 	c #E54034",
"Y 	c #DF5442",
"Z 	c #DA6D54",
"` 	c #CC8D65",
" .	c #B8AD6F",
"..	c #9ECE75",
"+.	c #8AE376",
"@.	c #7EEF76",
"#.	c #7BF479",
"$.	c #84F884",
"%.	c #90F990",
"&.	c #DF604C",
"*.	c #DE4F3D",
"=.	c #DE4734",
"-.	c #DD4632",
";.	c #DC4D38",
">.	c #DB5740",
",.	c #D86B50",
"'.	c #D38664",
").	c #CBA076",
"!.	c #C1BF89",
"~.	c #B4D994",
"{.	c #A7EB98",
"].	c #A0F39A",
"^.	c #A0F9A0",
"/.	c #A8FAA8",
"(.	c #B1FAB1",
"_.	c #CB845C",
":.	c #C97349",
"<.	c #C7683E",
"[.	c #C9673E",
"}.	c #C76D43",
"|.	c #C8784D",
"1.	c #CA885E",
"2.	c #CD9E75",
"3.	c #CCB78C",
"4.	c #C8D2A2",
"5.	c #C5E6B1",
"6.	c #C7F1BD",
"7.	c #C5F7C0",
"8.	c #C1FBC1",
"9.	c #C6FCC6",
"0.	c #CEFCCE",
"a.	c #AAAA5F",
"b.	c #A69A4D",
"c.	c #A59143",
"d.	c #A78D41",
"e.	c #A99046",
"f.	c #B1AB67",
"g.	c #BCBC81",
"h.	c #C5D09D",
"i.	c #CDE3B6",
"j.	c #D1EEC3",
"k.	c #D6F7D0",
"l.	c #DAFDDA",
"m.	c #E3FDE3",
"n.	c #E7FEE7",
"o.	c #84C858",
"p.	c #7CC049",
"q.	c #7DB741",
"r.	c #82B141",
"s.	c #85B245",
"t.	c #8BBA51",
"u.	c #94C867",
"v.	c #A7D484",
"w.	c #BCE5A7",
"x.	c #CFEDC1",
"y.	c #D8F3D0",
"z.	c #E8FAE5",
"A.	c #F1FEF1",
"B.	c #F0FEF0",
"C.	c #F5FEF5",
"D.	c #F9FFF9",
"E.	c #64E151",
"F.	c #5CDA43",
"G.	c #5BD43C",
"H.	c #5ECF3A",
"I.	c #65CF41",
"J.	c #6CD44D",
"K.	c #7ADC61",
"L.	c #92E681",
"M.	c #ABEFA0",
"N.	c #C7F6C2",
"O.	c #DFFADC",
"P.	c #FAFFFA",
"Q.	c #FFFFFF",
"R.	c #4EF14B",
"S.	c #45EC3D",
"T.	c #42E838",
"U.	c #44E537",
"V.	c #49E73D",
"W.	c #57EA4D",
"X.	c #6BEB61",
"Y.	c #83F27D",
"Z.	c #A2F49E",
"`.	c #C2FBC2",
" +	c #DCFDDC",
".+	c #EFFEEF",
"++	c #45F445",
"@+	c #3BF33B",
"#+	c #35F335",
"$+	c #3AEE35",
"%+	c #40EF3C",
"&+	c #4FEF4B",
"*+	c #65F362",
"=+	c #80F880",
"-+	c #DBFDDB",
";+	c #44F444",
">+	c #3AF33A",
",+	c #41F441",
"'+	c #50F550",
")+	c #65F665",
"!+	c #83F883",
"~+	c #A6FAA6",
"{+	c #C9FCC9",
"]+	c #FBFFFB",
"^+	c #4AF44A",
"/+	c #3FF43F",
"(+	c #5AF55A",
"_+	c #73F773",
":+	c #90F890",
"<+	c #AEFAAE",
"[+	c #F4FEF4",
"  . + @ # $ % & * = - ; > , ' ) ",
". ! ~ { ] ^ / ( _ : < [ } | 1 2 ",
"~ 3 ! ! 4 5 6 7 8 9 0 a b c d ) ",
"e ~ 3 3 f g h i j k l m n o 2 p ",
"q e { e r 5 s t u v w x y z A B ",
"C D E F G H I J K L M N O P Q R ",
"S T U V W X Y Z `  ...+.@.#.$.%.",
"&.*.=.-.;.>.,.'.).!.~.{.].^./.(.",
"_.:.<.[.}.|.1.2.3.4.5.6.7.8.9.0.",
"a.b.c.d.e.* f.g.h.i.j.k.l.l.m.n.",
"o.p.q.r.s.t.u.v.w.x.y.z.A.B.C.D.",
"E.F.G.H.I.J.K.L.M.N.O.B.P.Q.Q.Q.",
"R.S.T.U.V.W.X.Y.Z.`. +.+D.Q.Q.Q.",
"++@+#+$+%+&+*+=+^.`.-+.+D.Q.Q.Q.",
";+>+' , ,+'+)+!+~+{+ +B.]+Q.Q.Q.",
"^+,+/+) A (+_+:+<+0.n.[+Q.Q.Q.Q."};"""


    MenuText = "School"
    ToolTip = "School workbench"

    def Initialize(self):
        import DraftTools,DraftGui,Arch_rc,Arch,Draft_rc
        from DraftTools import translate
	import School

        # school tools
        self.schooltools = [ 	
				"School_Pyramid", 

			]
        self.utilities = [
			
				"School_Prism"
			]

        # draft tools
        self.drafttools = ["Draft_Line","Draft_Wire","Draft_Circle","Draft_Arc","Draft_Ellipse",
                        "Draft_Polygon","Draft_Rectangle", "Draft_Text",
                        "Draft_Dimension", "Draft_BSpline","Draft_Point","Draft_ShapeString",
                        "Draft_Facebinder"]
        self.draftmodtools = ["Draft_Move","Draft_Rotate","Draft_Offset",
                        "Draft_Trimex", "Draft_Upgrade", "Draft_Downgrade", "Draft_Scale",
                        "Draft_Drawing","Draft_Shape2DView","Draft_Draft2Sketch","Draft_Array",
                        "Draft_PathArray","Draft_Clone"]
        self.extramodtools = ["Draft_WireToBSpline","Draft_AddPoint","Draft_DelPoint"]
        self.draftcontexttools = ["Draft_ApplyStyle","Draft_ToggleDisplayMode","Draft_AddToGroup",
                            "Draft_SelectGroup","Draft_SelectPlane",
                            "Draft_ShowSnapBar","Draft_ToggleGrid","Draft_UndoLine",
                            "Draft_FinishLine","Draft_CloseLine"]
        self.draftutils = ["Draft_Heal","Draft_FlipDimension"]
        self.snapList = ['Draft_Snap_Lock','Draft_Snap_Midpoint','Draft_Snap_Perpendicular',
                         'Draft_Snap_Grid','Draft_Snap_Intersection','Draft_Snap_Parallel',
                         'Draft_Snap_Endpoint','Draft_Snap_Angle','Draft_Snap_Center',
                         'Draft_Snap_Extension','Draft_Snap_Near','Draft_Snap_Ortho',
                         'Draft_Snap_Dimensions']

        self.appendToolbar("Schul Werkzeuge",self.schooltools)
        self.appendMenu("&Schule1",self.utilities)
        self.appendMenu(["Schule2"],self.schooltools)
        self.appendToolbar(translate("arch","Draft tools"),self.drafttools)
#        self.appendToolbar(translate("arch","Draft mod tools"),self.draftmodtools)
	if 0:
		self.appendMenu(translate("arch","&Draft"),self.drafttools+self.draftmodtools+self.extramodtools)
		self.appendMenu([translate("arch","&Draft"),translate("arch","Context Tools")],self.draftcontexttools)
		self.appendMenu([translate("arch","&Draft"),translate("arch","Utilities")],self.draftutils)
		## self.appendMenu([translate("arch","&Draft"),translate("arch","Snapping")],self.snapList)
		FreeCADGui.addIconPath(":/icons")
		FreeCADGui.addLanguagePath(":/translations")
		FreeCADGui.addPreferencePage(":/ui/archprefs-base.ui","Arch")
		FreeCADGui.addPreferencePage(":/ui/archprefs-import.ui","Arch")
		if hasattr(FreeCADGui,"draftToolBar"):
		    if not hasattr(FreeCADGui.draftToolBar,"loadedPreferences"):
		        FreeCADGui.addPreferencePage(":/ui/userprefs-base.ui","Draft")
		        FreeCADGui.addPreferencePage(":/ui/userprefs-visual.ui","Draft")
		        FreeCADGui.addPreferencePage(":/ui/userprefs-import.ui","Draft")
		        FreeCADGui.draftToolBar.loadedPreferences = True
        Log ('Loading School module... done\n')

    def Activated(self):
        if hasattr(FreeCADGui,"draftToolBar"):
            FreeCADGui.draftToolBar.Activated()
        if hasattr(FreeCADGui,"Snapper"):
            # FreeCADGui.Snapper.show()
	    pass
        Msg("School workbench activated\n")
                
    def Deactivated(self):
        if hasattr(FreeCADGui,"draftToolBar"):
            FreeCADGui.draftToolBar.Deactivated()
        if hasattr(FreeCADGui,"Snapper"):
            # FreeCADGui.Snapper.hide()
            pass
        Msg("School workbench deactivated\n")

    def ContextMenu(self, recipient):
        self.appendContextMenu("Draft context tools",self.draftcontexttools)

    def GetClassName(self): 
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(SchoolWorkbench)


