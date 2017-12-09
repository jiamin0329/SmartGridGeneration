#!/usr/local/bin/python
#######################################################
#            File description
#######################################################
# This is a sample file to show the most basic functions
# and also the main process of smart grid generation tool.
#
#######################################################
#    Date        Author        Comment
#  09-Dec-2017   Jiamin Xu     Initial creation
#######################################################
#            Import modules
#######################################################
import sys
sys.path.append("../../src")
from icemcfdgeom import IcemPoint
from icemcfdgeom import IcemCurve
from icemcfdgeom import IcemSurface

from icemcfdscript import IcemcfdWriter
#######################################################
#            Constants
#######################################################

#######################################################
#            Class
#######################################################
def BuildSquareTin():
    status = True
    
    geomList = []

    ## inner geometry
    square_point_inner_1 = IcemPoint("square_point_inner_1", "inner", "./InputTinFiles/square_point_inner_1.tin")
    square_point_inner_2 = IcemPoint("square_point_inner_2", "inner", "./InputTinFiles/square_point_inner_2.tin")
    square_point_inner_3 = IcemPoint("square_point_inner_3", "inner", "./InputTinFiles/square_point_inner_3.tin")
    square_point_inner_4 = IcemPoint("square_point_inner_4", "inner", "./InputTinFiles/square_point_inner_4.tin")

    square_curve_inner_1 = IcemCurve("square_curve_inner_1", "inner", "./InputTinFiles/square_curve_inner_1.tin")
    square_curve_inner_2 = IcemCurve("square_curve_inner_2", "inner", "./InputTinFiles/square_curve_inner_2.tin")
    square_curve_inner_3 = IcemCurve("square_curve_inner_3", "inner", "./InputTinFiles/square_curve_inner_3.tin")
    square_curve_inner_4 = IcemCurve("square_curve_inner_4", "inner", "./InputTinFiles/square_curve_inner_4.tin")

    geomList.append(square_point_inner_1)
    geomList.append(square_point_inner_2)
    geomList.append(square_point_inner_3)
    geomList.append(square_point_inner_4)
    geomList.append(square_curve_inner_1)
    geomList.append(square_curve_inner_2)
    geomList.append(square_curve_inner_3)
    geomList.append(square_curve_inner_4)

    ## outer geometry
    square_point_outer_1 = IcemPoint("square_point_outer_1", "outer", "./InputTinFiles/square_point_outer_1.tin")
    square_point_outer_2 = IcemPoint("square_point_outer_2", "outer", "./InputTinFiles/square_point_outer_2.tin")
    square_point_outer_3 = IcemPoint("square_point_outer_3", "outer", "./InputTinFiles/square_point_outer_3.tin")
    square_point_outer_4 = IcemPoint("square_point_outer_4", "outer", "./InputTinFiles/square_point_outer_4.tin")

    square_curve_outer_1 = IcemCurve("square_curve_outer_1", "outer", "./InputTinFiles/square_curve_outer_1.tin")
    square_curve_outer_2 = IcemCurve("square_curve_outer_2", "outer", "./InputTinFiles/square_curve_outer_2.tin")
    square_curve_outer_3 = IcemCurve("square_curve_outer_3", "outer", "./InputTinFiles/square_curve_outer_3.tin")
    square_curve_outer_4 = IcemCurve("square_curve_outer_4", "outer", "./InputTinFiles/square_curve_outer_4.tin")

    geomList.append(square_point_outer_1)
    geomList.append(square_point_outer_2)
    geomList.append(square_point_outer_3)
    geomList.append(square_point_outer_4)
    geomList.append(square_curve_outer_1)
    geomList.append(square_curve_outer_2)
    geomList.append(square_curve_outer_3)
    geomList.append(square_curve_outer_4)

    ## write final tin file
    texts = []
    for geom in geomList:
        geom.AddToTetin(texts)

    tinFile = open("square_final.tin", 'w')
    for i in range(len(texts)):
        tinFile.write(texts[i])
    tinFile.close()

    ## initialize a icemcfd script writer object
    writer = IcemcfdWriter("square_final.tin", "square.blk", "icemcfd_script_square.rpl")

    writer.LoadTetin()
    writer.LoadBlk()
    
    writer.DoProjectionVertex("11", "square_point_outer_1")
    writer.DoProjectionVertex("19", "square_point_outer_2")
    writer.DoProjectionVertex("21", "square_point_outer_3")
    writer.DoProjectionVertex("13", "square_point_outer_4")
    
    writer.DoProjectionVertex("32", "square_point_inner_1")
    writer.DoProjectionVertex("34", "square_point_inner_2")
    writer.DoProjectionVertex("35", "square_point_inner_3")
    writer.DoProjectionVertex("33", "square_point_inner_4")

    writer.DoProjectionEdge("11 19 0 1", "square_curve_outer_1")
    writer.DoProjectionEdge("19 21 0 1", "square_curve_outer_2")
    writer.DoProjectionEdge("13 21 0 1", "square_curve_outer_3")
    writer.DoProjectionEdge("11 13 0 1", "square_curve_outer_4")
    
    writer.DoProjectionEdge("32 34 0 1", "square_curve_inner_1")
    writer.DoProjectionEdge("34 35 0 1", "square_curve_inner_2")
    writer.DoProjectionEdge("33 35 0 1", "square_curve_inner_3")
    writer.DoProjectionEdge("32 33 0 1", "square_curve_inner_4")

    writer.ComputeMesh()
    writer.WriteRplFile()

    return status
    
#######################################################
#            Main
#######################################################
if __name__ == '__main__':
    BuildSquareTin()
    pass


