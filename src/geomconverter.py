#!/usr/local/bin/python
#######################################################
#            File description
#######################################################
#
# 1. inputFile/tinFile here are all in absolute path
#######################################################
#    Date        Author        Comment
#  16-Dec-2017   Jiamin Xu     Initial creation
#######################################################
#            Import modules
#######################################################
import os

#######################################################
#            Constants
#######################################################
icemcfd_version = "160"

#######################################################
#            Class
#######################################################
class TinConverter:
    def __init__(self, inputFile, tinFile = None):
        self.inputFile = inputFile
        ##print(self.inputFile)
        
        if tinFile == None:
            self.tinFile = inputFile.split(".")[-2] + ".tin"
        else:
            self.tinFile = tinFile
        ##print(self.tinFile)
        
        ## Find icemcfd igestotin converter
        icemcfd_root = "ICEMCFD_ROOT" + icemcfd_version
        envs = os.environ

        if envs.get(icemcfd_root) == None:
            print("icemcfd" + icemcfd_version + " not found!!! Please check icemcfd version or env variables!!!")
            return False
        
        self.converter = envs.get(icemcfd_root) + "\\win64_amd\\dif\\iges\\igestotin"
        ##print(self.converter)
        ##
    
        pass

    def Convert(self):
        status = True
        doConvertion = "\"" + self.converter + "\""+ " {} " + self.inputFile + " " + self.tinFile
        print(doConvertion)
        status = os.system(doConvertion)
        return status

#######################################################
#            Main
#######################################################
if __name__ == '__main__':
    converter = TinConverter("test.stp")
    converter.Convert()
    
