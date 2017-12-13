'''
Created on Nov 25, 2017

@author: NNA
'''
import xml.etree.ElementTree as ET
import re
import hashlib
import cast.analysers.log as CAST
from cast.analysers import Bookmark
class castxmlhelper():
    
    def __init__(self):
        self.tag_names = []
        self.att_names = []
       
    def defineTagNames(self):
        self.tag_names = ["beans","service-activator"]
        self.att_names =["id", "input-channel","output-channel","ref", "Method", "expression"]
        
    
   
if __name__ == "__main__":
    pass
        