__license__ = 'GNU Public License Version 3, https://www.gnu.org/licenses/gpl-3.0.en.html'
__copyright__ = "Copyright (C) 2020, Dev@BernCodes.com - Released under terms of the GPLv3 License"

from bitstring import BitArray
from random import shuffle
from pyDominoValueGenerator import Valid_Dominos
from datetime import datetime
from math import floor
import pyx
import logging


class Margin():
    Top = 0.0
    Left = 0.0
    Right = 0.0
    Bottom = 0.0

class Paper():
    Height = 0.0
    Width = 0.0
    Margin = Margin()
    Count = 0
    Center_Vertical = False
    Center_Horizontal = False
    X_ScaleFactor = 1.0
    Y_ScaleFactor = 1.0

class pyDominoPDF:
    MarginBorder = False

    RowSpacing = 3.0
    Page = Paper()
    VerificationScale = False
    Randomize = True
    PrintValues = False
    MarginBorder = False
    DebugFile = True
    RadiusCorners = False

    #__pyx_d = None
    _units = "inch"
    _unit_scale = 1.0

    @property
    def Units(self):
        #Unit Property Get
        return self._units

    @Units.setter
    def Units(self, value):
        #Unit Property Set
        if (value == "inch"):
            self._unit_scale = 1.0
        elif (value == "mm"):
            self._unit_scale = 25.4
        elif (value == "cm"):
            self._unit_scale = 2.54
        else:
            self._unit_scale = 1.0

        self._units = value
    
    @property
    def DominoPadding(self):
        return (0.125 * self._unit_scale)

    @property
    def DominoRadius(self):
        return (.0625 * self._unit_scale)
    
    @property
    def Pip_Padding(self):
        return (0.10 * self._unit_scale)
    
    @property
    def Domino_Width(self):
        return (1.7 * self._unit_scale)
    
    @property
    def Domino_Height(self):
        return (0.5 * self._unit_scale)
    @property
    def CornerRadius(self):
        return (0.10 * self._unit_scale)
    
    @property
    def Pip_Diameter(self):
        return (0.10 * self._unit_scale)

    @property
    def Pip_Radius(self):
        return (0.05 * self._unit_scale)

    def __place_domino(self, x,y, value, canvas):
        #Paints Domino, X,Y @ Left Corner of Domino

        #PYX Library
        if (self.RadiusCorners == True):
            w = self.Domino_Width
            h = self.Domino_Height
            r = self.CornerRadius

            pyx_circle = pyx.path.circle(x+r, y+r, r)
            canvas.fill(pyx_circle, [pyx.color.rgb.black])

            pyx_circle = pyx.path.circle((x+w)-r, y+r, r)
            canvas.fill(pyx_circle, [pyx.color.rgb.black])

            pyx_circle = pyx.path.circle(x+r, (y+h)-r, r)
            canvas.fill(pyx_circle, [pyx.color.rgb.black])

            pyx_circle = pyx.path.circle((x+w)-r, (y+h)-r, r)
            canvas.fill(pyx_circle, [pyx.color.rgb.black])

            pyx_rec = pyx.path.rect (x, y+r, w, h-(2*r))
            canvas.fill(pyx_rec, [pyx.color.rgb.black])

            pyx_rec = pyx.path.rect (x+r, y, w-(2*r), h)
            canvas.fill(pyx_rec, [pyx.color.rgb.black])

        else:
            pyx_rec = pyx.path.rect (x, y, self.Domino_Width, self.Domino_Height)
            canvas.fill(pyx_rec, [pyx.color.rgb.black])


        px = 0
        py = 0

        DPips = BitArray('0x000')
        DPips.uint = int(value)

        #BitArrays are big endian by default
        BitRow = [BitArray(6), BitArray(6)]

        BitRow[0] = DPips[:6] # First Row
        BitRow[1]= DPips[-6:] # Second Row
        
        for py in range(2):
            for px in range(8):
                #First and list pip are always placed
                #Pip 1-6 based on bitrow
                if (px == 0) or (px == 7) or (BitRow[py][px-1] is True):
                    YCord = y + (self.Pip_Padding+(self.Pip_Radius)+((py*2)*(self.Pip_Diameter)))
                    XCord = x + (self.Pip_Padding+(self.Pip_Radius)+((px*2)*(self.Pip_Diameter)))

                    pyx_circle = pyx.path.circle(XCord, YCord, self.Pip_Radius)
                    canvas.fill(pyx_circle, [pyx.color.rgb.white])

        return ()

    def __prepare_file(self, pyx_document):

        #ValidValues = DominoValues(0,4095)
        if (self.Randomize == True): shuffle(Valid_Dominos)

        work_width = self.Page.Width-(self.Page.Margin.Left+self.Page.Margin.Right)
        work_height = self.Page.Height-(self.Page.Margin.Top+self.Page.Margin.Bottom)

        pg_Num_Rows = 1+floor((work_height-self.Domino_Height)/(self.Domino_Height+self.RowSpacing)) # Number of Complete Rows
        pg_Num_Cols = 1+floor((work_width-self.Domino_Width)/(self.Domino_Width+self.DominoPadding))

        if (self.Page.Center_Horizontal == True):
            x_domino_space = (pg_Num_Cols*(self.Domino_Width+self.DominoPadding))-self.DominoPadding
            x_offset = round((work_width-x_domino_space)/2, 4)
        else:
            x_offset = 0

        if (self.Page.Center_Vertical  == True):
            y_domino_space =  (pg_Num_Rows*(self.Domino_Height+self.RowSpacing))-self.RowSpacing
            y_offset = round((work_height-y_domino_space)/2, 4)
        else:
            y_offset = 0
        
        xPage = 0
        ValueIndex = 0
        ValueIndexMax = len(Valid_Dominos)

        if (self.VerificationScale == True) :
            pyx_vsc = pyx.canvas.canvas()
            for v in range(5):
                vsc_r =  pyx.path.rect (0+self.Page.Margin.Left, (v*self._unit_scale)+(0.5*v*self._unit_scale)+self.Page.Margin.Bottom, (5-v)*self._unit_scale, 1*self._unit_scale)
                pyx_vsc.fill(vsc_r, [pyx.color.rgb.black])

                vert_scale_x = (self.Page.Width-self.Page.Margin.Right)-(v*self._unit_scale)-(0.5*v*self._unit_scale)-(1*self._unit_scale)
                vert_scale_y = self.Page.Height-self.Page.Margin.Top - (5-v)*self._unit_scale
                vsc_r =  pyx.path.rect (vert_scale_x, vert_scale_y, 1*self._unit_scale, (5-v)*self._unit_scale)
                logging.debug("width: {} height: {} at {},{}" . format(1*self._unit_scale, (5-v)*self._unit_scale, vert_scale_x, vert_scale_y))
                pyx_vsc.fill(vsc_r, [pyx.color.rgb.black])

            pyx_vsc_page = pyx.document.page(pyx_vsc,None, pyx.document.paperformat(self.Page.Width, self.Page.Height),0,0,0,0)
            pyx_document.append(pyx_vsc_page)


        for xPage in range(self.Page.Count):
            logging.debug("Page {}" . format(xPage))
            pyx_c = pyx.canvas.canvas()

            if (self.MarginBorder == True):
                #Margin Rectangle
                mr_x = self.Page.Margin.Left
                mr_y = self.Page.Margin.Bottom
                mr_height = self.Page.Height-(self.Page.Margin.Top+self.Page.Margin.Bottom)
                mr_width = self.Page.Width-(self.Page.Margin.Left+self.Page.Margin.Right)

                margin_rect =  pyx.path.rect (mr_x, mr_y, mr_width,mr_height)
                pyx_c.stroke(margin_rect, [pyx.color.rgb.blue])

            for py in range(pg_Num_Rows):
                for px in range(pg_Num_Cols):
                    DX = (px * self.Domino_Width) + (px * self.DominoPadding) + self.Page.Margin.Left + x_offset
                    DY = (py * self.RowSpacing) + (py * self.Domino_Height) + self.Page.Margin.Bottom + y_offset
                    
                    if (ValueIndex == ValueIndexMax):
                        ValueIndex = 0
                        if (self.Randomize == True): shuffle(Valid_Dominos)

                    self.__place_domino(DX, DY, Valid_Dominos[ValueIndex], pyx_c)
                    ValueIndex = ValueIndex+1

            pyx_sc = pyx.canvas.canvas()
            
            pyx_sc.insert(pyx_c, [pyx.trafo.scale(sx=self.Page.X_ScaleFactor, sy=self.Page.Y_ScaleFactor)]) #Scale Factor Here
            pyx_page = pyx.document.page(pyx_sc,None, pyx.document.paperformat(self.Page.Width, self.Page.Height),0,0,0,0)
            pyx_document.append(pyx_page)

        return ()

    def SavePDF(self, filepath):
        pyx.unit.set(defaultunit=self.Units)
        pyx_document = pyx.document.document()

        self.__prepare_file(pyx_document)

        pyx_document.writePDFfile(filepath)
        del pyx_document
        return ()

if __name__ == "__main__":
    print ("Domino Printed Fidicual Generator for use with Shaper Origin")
    print ("The default settings below will a US letter sized document consisting of all valid dominos in order.")
    print ("Values start over at page 12.")
    print ("Currently using a domino list of {} values." . format(len(Valid_Dominos)))


    testdoc = pyDominoPDF()
    testdoc.Units = "inch"
    testdoc.Page.Height = 11
    testdoc.Page.Width = 8.5

    testdoc.Page.Center_Vertical = True
    testdoc.Page.Center_Horizontal = True

    testdoc.Page.Margin.Top = 0.6
    testdoc.Page.Margin.Left = 0.6
    testdoc.Page.Margin.Right = 0.6
    testdoc.Page.Margin.Bottom = 0.6
    
    testdoc.Page.Count = 12

    #Page Scaling, 1 = 100%, unitless
    testdoc.Page.X_ScaleFactor = 1.0
    testdoc.Page.Y_ScaleFactor = 1.0


    #Vertical spacing of the rows, in document units
    testdoc.RowSpacing = 0.5

    #Randomize Domino Order (Or Not)
    testdoc.Randomize = False

    #Radius Corners of Domino
    testdoc.RadiusCorners = True

    #Margin Border, Useful for debugging the printable area
    testdoc.MarginBorder = False

    #Save PDF, YYYYMMDD-HHMM
    date_time = datetime.now().strftime("%Y%m%d-%H%M")
    filename = ("Output-{}.pdf" . format(date_time))	 
    testdoc.SavePDF(filename)
    print('Done.')







