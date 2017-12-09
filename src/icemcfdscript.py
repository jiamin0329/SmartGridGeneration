#!/usr/local/bin/python
#######################################################
#            File description
#######################################################
# This is the main object to write icemcfd script file
# automatically. 
#######################################################
#    Date        Author        Comment
#  09-Nov-2017   Jiamin Xu     Initial creation
#######################################################
#            Import modules
#######################################################


#######################################################
#            Constants
#######################################################


#######################################################
#            Class
#######################################################
class IcemcfdWriter:
    def __init__ (self, tetinFile, blkFile, rplFile):
        self.rplTexts = []
        self.tetinFile = tetinFile
        self.blkFile = blkFile
        self.rplFile = rplFile

        self.allParts = ["OUTER", "INNER", "SOLID"]
        pass

    def WriteRplFile(self):
        rplFile = open(self.rplFile, "w")
        for i in range(len(self.rplTexts)):
            rplFile.write(self.rplTexts[i])
        rplFile.close()

        
    def LoadTetin(self):
        self.rplTexts.append("##Load tetin file \n")
        self.rplTexts.append("ic_load_tetin " + self.tetinFile + "\n")

        
    def LoadBlk(self):
        self.rplTexts.append("##Load blk file \n")
        self.rplTexts.append("ic_hex_restore_blocking " + self.blkFile + "\n")
        self.rplTexts.append("ic_hex_switch_blocking root \n")
        ##self.rplTexts..append("ic_hex_compute_mesh_size INNER OUTER SOLID \n")
        self.rplTexts.append("ic_hex_error_messages off_minor \n")


    def DoProjectionVertex(self, vertex, point):
        self.rplTexts.append("## project " + vertex + " to " + point + "\n")
        self.rplTexts.append("ic_hex_move_node " + vertex + " " + point + "\n")

        
    def DoProjectionEdge(self, edge, curve):
        self.rplTexts.append("## project " + edge + " to " + curve + "\n")
        self.rplTexts.append("ic_hex_set_edge_projection " + edge + " " + curve + "\n")

        
    def DoProjectionFace(self, face, surface):

        pass

    def ComputeMesh(self):
        text = "ic_hex_create_mesh "
        for part in self.allParts:
            text += part + " "
        text += "proj 2 dim_to_mesh 3 \n"

        self.rplTexts.append(text)

#######################################################
#            Main
#######################################################
if __name__ == '__main__':

    pass
