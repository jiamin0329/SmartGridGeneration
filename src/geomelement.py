#!/usr/local/bin/python
#######################################################
#            File description
#######################################################
#  Elementary geometry classes used in Smart Grid
#  Generation tool.
#  1. Point object
#  2. Curve object
#  3. Surface object
#
#######################################################
#    Date        Author        Comment
#  27-Nov-2017   Jiamin Xu     Initial creation
#######################################################
#            Import modules
#######################################################

#######################################################
#            Constants
#######################################################

#######################################################
#            Class
#######################################################
## Point object
class Point:
    """ Point object """
    def __init__ (self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        pass

    def GetX(self):
        return self.x

    def GetY(self):
        return self.y

    def GetZ(self):
        return self.z

    
## Curve object
class Curve:
    """ Curve object """
    def __init__ (self):
        self.numPoints = -1
        self.order     = -1           
        self.points = []
        self.knots  = []
        pass


## Surface object
class Surface:
    def __init__(self):
        self.numUPoints = -1
        self.numVPoints = -1
        
        self.uPoints = []
        self.vPoints = []

        self.uOrder = -1
        self.vOrder = -1
        
        self.uKnots = []
        self.vKnots = []
        
        pass

    
############################################
#            Main
############################################
if __name__ == '__main__':
    ## point

    ## curve

    ## surface
    
    pass
