#!/usr/local/bin/python
#######################################################
#            File description
#######################################################
#
#######################################################
#    Date        Author        Comment
#  28-Nov-2017   Jiamin Xu     Initial creation
#  03-Dec-2017   Jiamin Xu     Add Validate()
#  09-Dec-2017   Jiamin Xu     Report object name if there is an error
#######################################################
#            Import modules
#######################################################
import collections
from geomelement import Point
from geomelement import Curve
from geomelement import Surface
#######################################################
#            Constants
#######################################################

#######################################################
#            Class
#######################################################
class IcemGeom:
    def __init__ (self, name, part):
        self.name = name
        self.part = part
        pass

    def GetName(self):
        return self.name

    def GetPart(self):
        return self.part

    
class IcemPoint(Point, IcemGeom):
    def __init__ (self, name, part, pointFile = None, x = 0.0, y = 0.0, z = 0.0):
        IcemGeom.__init__(self, name, part)
        Point.__init__(self, x, y, z)

        self.fromTinFile = pointFile
        if self.fromTinFile:
            self.__Parse()
        pass

    def __Parse(self):
        status = self.__Validate()
        if not status:
            return status
        
        tinFile = open(self.fromTinFile)
        lines = tinFile.readlines()

        for line in lines:
            if "prescribed_point" in line:
                self.x = line.split()[1]
                self.y = line.split()[2]
                self.z = line.split()[3]
                
        return True

    def __Validate(self):
        tinFile = open(self.fromTinFile)
        texts = tinFile.read().split()
        count = collections.Counter(texts)["prescribed_point"]

        if count != 1:
            return False
        
        return True

    def AddToTetin(self, tinTexts):
        text = "prescribed_point "
        text += str(self.x) + " " + str(self.y) + " " + str(self.z)
        text += " family " + self.part
        text += " name " + self.name
        tinTexts.append(text + "\n")
        return True

    
class IcemCurve(Curve, IcemGeom):
    def __init__(self, name, part, curveFile):
        IcemGeom.__init__(self, name, part)
        Curve.__init__(self)
        
        self.bsplineType = -1
        self.staPoint = None
        self.endPoint = None

        self.fromTinFile = curveFile
        if self.fromTinFile:
            if not self.__Parse():
                print (self.name + ": Fail read icemcfd bspline!!!")
        else:
            print "Tin File not found!!!"
            
        pass
    
    def __Parse(self):
        status = self.__Validate()
        if not status:
            return status

        curveTinFile = open(self.fromTinFile)
        lines = curveTinFile.readlines()

        for i in range(len(lines)):
            line = lines[i]
            if "bspline" in line:
                self.numPoints   = int(lines[i+1].split(",")[0])
                self.order       = int(lines[i+1].split(",")[1])
                self.bsplineType = int(lines[i+1].split(",")[2])

                numLines = 0
                if (self.numPoints+self.order)%5 > 0:
                    numLines = int((self.numPoints+self.order)/5) + 1
                else:
                    numLines = int((self.numPoints+self.order)/5)

                for j in range(numLines):
                    line = lines[i+2+j]
                    #print line
                    if j < numLines-1:
                        for k in range(5):
                            self.knots.append(float(line.split(",")[k]))
                    else:
                        for k in range((self.numPoints+self.order)%5):
                            self.knots.append(float(line.split(",")[k]))
                            
                for j in range(self.numPoints):
                    line = lines[i+1+numLines+1+j]
                    #print line
                    point = []
                    point.append(float(line.split(",")[0]))  ## x value
                    point.append(float(line.split(",")[1]))  ## y value
                    point.append(float(line.split(",")[2]))  ## z value
                    if self.bsplineType == 1:
                        point.append(float(line.split(",")[3]))  ## 

                    self.points.append(point)

        if not len(self.points) == self.numPoints:
            return False

        return True

    def __Validate(self):
        tinFile = open(self.fromTinFile)
        texts = tinFile.read().split()
        count = collections.Counter(texts)["define_curve"]

        if count != 1:
            return False

        return True

    def AddToTetin(self, tinTexts):
        ## add basic info of the curve
        text = "define_curve "
        text += "family " + self.part
        text += " name " + self.name
        if self.staPoint != None and self.endPoint != None:
            text += " vertex1 " + self.point1.GetName()
            text += " vertex2 " + self.point2.GetName()
        text += "\n"
        tinTexts.append(text)
        ## Add bspline
        tinTexts.append("bspline \n")
        tinTexts.append(str(self.numPoints) + "," + str(self.order) + "," + str(self.bsplineType) + "\n")
        ## Add knots of the bspline (5 values for each line)
        numLines = 0
        if (self.numPoints+self.order)%5 > 0:
            numLines = int((self.numPoints+self.order)/5) + 1
        else:
            numLines = int((self.numPoints+self.order)/5)

        for i in range(numLines):
            if i < numLines-1:
                line = ""
                for j in range(5):
                    line+=(str(self.knots[i*5+j]))
                    if j < 4:
                        line += ","
                    else:
                        line += "\n"
                
            else:
                line = ""
                for j in range((self.numPoints+self.order)%5):
                    line += str(self.knots[i*5+j])
                    if j < (self.numPoints+self.order)%5-1:
                        line += ","
                    else:
                        line += "\n"

            tinTexts.append(line)

        ## Add points into texts
        for i in range(self.numPoints):
            line = str(self.points[i][0]) + "," + str(self.points[i][1]) + "," + str(self.points[i][2])
            if self.bsplineType == 1:
                line += "," + str(self.points[i][3])
            line += "\n"

            tinTexts.append(line)

        return True

    
class IcemSurface(Surface, IcemGeom):
    def __init__(self, name, part, surfaceFile):
        IcemGeom.__init__(self, name, part)
        Surface.__init__(self)
        
        self.isTrimSurface = False
        self.fromTinFile = surfaceFile

        if self.fromTinFile:
            if not self.__Parse():
                print ("Fail read icemcfd surface!!!")
        else:
            print "Tin File not found!!!"

        pass

    def __Parse(self):
        


        
        return True

    def __Validate(self):
        

        return True

    def AddToTetin(self, tinTexts):
        return True

############################################
#            Main
############################################
if __name__ == '__main__':
    ## point
    ## point initialized with x,y,z
    print "Point initialized from xyz values."
    point = IcemPoint("PointFromValue", "PointTest", x = 1.0, y = 2.0, z = 3.0)
    print "Point x:", point.GetX()
    print "Point y:", point.GetY()
    print "Point z:", point.GetZ()

    pointTexts = []
    point.AddToTetin(pointTexts)
    
    tinFile = open("test_point_output.tin", 'w')
    for i in range(len(pointTexts)):
        tinFile.write(pointTexts[i])
    tinFile.close()
    print "********************************"

    ## point initialized from tin file
    print "Point initialized from previous tin file."
    point = IcemPoint("PointFromFile", "PointTest", "test_point.tin")
    print "Point x:", point.GetX()
    print "Point y:", point.GetY()
    print "Point z:", point.GetZ()
    print "********************************"
    
    ## curve
    ## curve object created from input tin file. 
    print "Curve initialized from tin file."
    curve = IcemCurve("CurveFromFile", "CurveTest", "test_curve.tin")
    curveTexts = []
    curve.AddToTetin(curveTexts)
    
    tinFile = open("test_curve_output.tin", 'w')
    for i in range(len(curveTexts)):
        tinFile.write(curveTexts[i])
    tinFile.close()
    print "********************************"
    
    ## surface
    print "Surface initialized from tin file. "
    surface = IcemSurface("SurfaceFromFile", "SurfaceTest", "test_surface.tin")

    surfaceTexts = []
    surface.AddToTetin(surfaceTexts)

    tinFile = open("surface_test_output.tin", 'w')
    for i in range(len(surfaceTexts)):
        tinFile.write(surfaceTexts[i])
    tinFile.close()

    """
    numLoops  = 0
    numCurves = []
    numPointsInPolyline = []
    for line in lines:
        if "trim_surface" in line:
            numLoops = line.split()[2]
    print numLoops

    for line in lines:
        if "loop n_curves" in line:
            num = line.split()[2]
            numCurves.append(num)
    print numCurves

    for line in lines:
        for indexLoops in range(numLoops):
            for indexCurves in range(numCurves[i]):
                if "polyline n_points" in line:
                    num = line.split()[2]
            



    
##
##
##
##            numLines = 1 + 
##            for j in range(numLines):
##                surfaceTexts.append(lines[i+j])
##            break
##
##                
##        if "loop n_curves" in line:
##            numCurves = line.split()[2]
##            
##        if "polyline n_points" in line:
##            numPoints = line.split()[2]
##            numPointsInPolyline.append(numPoints)
##
##        if "bspline" in line:
##            numUPoints = lines[i+1].split(",")[0]
##            numVPoints = lines[i+1].split(",")[1]
##            uOrder     = lines[i+1].split(",")[2]
##            vOrder     = lines[i+1].split(",")[3]
##
            
          
    pass
"""

