'''
Created on Nov 25, 2017

@author: NNA
'''

import cast.analysers.jee
import cast.application
import cast.analysers.log as LOG
import os
from cast.analysers import Member,Bookmark
from setuptools.sandbox import _file
import xml.etree.ElementTree as ET


def get_overriden(_type, member):
    """
    Get the ancestor's member this member overrides
    """
    member_name = member.get_name()
    
    result = []
    
    for parent in _type.get_inherited_types():
        
        for child in parent.get_children():
            if child.get_name() == member_name:
                result.append(child)
        
        result += get_overriden(parent, member)
        
    return result

class sactivator(cast.analysers.jee.Extension):
    def __init__(self):
        self.fielPath = ""
        self.ref = None
        self.sactivatorName = None
        self.annsactivator = None
        self.typeList = []
        self.endPointNameList = []
        self.elementNameList = {}
        self.method = None
        self.inputchannel = None
        self.outputchannel = None
        self.output = []
        self.activatorid = None
        self.result = None
        self.channelmetamodeltext =""
        self.channeltext=""
        self.channelxmltext=""
        self.count = 1
        
               
    def start_analysis(self,options):
        LOG.info('Successfully service activator analyzer Started')
        options.add_classpath('jars')
        options.handle_xml_with_xpath('/beans')
      
               
     
       
    # receive a java parser from platform
    @cast.Event('com.castsoftware.internal.platform', 'jee.java_parser')
    def receive_java_parser(self, parser):
        self.java_parser = parser
        LOG.info('Successfully receive_java_parser')
        pass
        #service_object = cast.analysers.CustomObject()
        #service_object.set_name('test activator')
        #service_object.set_type('SpringServiceactivator')
        #service_object.set_parent()
        #service_object.save()
        #LOG.info('SActivatorinside object done')
       
   
        
            #if root.tag == 'sqlMap' or root.tag == '{http://www.springframework.org/schema/integration/jms}sqlMap' :
                #Log.info('Scanning iBatis.NET file: %s' % file.get_name())   
    
    def createactivatorObject(self,typ,annoValue):
        if annoValue['ServiceActivator'] == None:
            annoValue['ServiceActivator'] = str(typ.get_name()) + 'ServiceActivator'
        self.sactivatorName = str(typ.get_name()) + 'ServiceActivator'
        service_object = cast.analysers.CustomObject()
        service_object.set_name(self.sactivatorName)
        service_object.set_type('Spring_Service_activator')
        parentFile = typ.get_position().get_file() 
        service_object.set_parent(parentFile)
        self.fielPath = parentFile.get_fullname()
        service_object.set_fullname(annoValue['ServiceActivator']) #Same as name as per legacy c++
        service_object.set_guid(self.fielPath+self.sactivatorName)
        service_object.save()
        service_object.save_position(typ.get_position())
        #LOG.info('Spring_Service_activator object created with name '+self.serviceName)
        pass
    
    
    def start_xml_file(self, file):
        LOG.info('Scanning XML test file :' )
        if file.get_name().endswith('.xml'):
            tree = ET.parse(file.get_path(), ET.XMLParser(encoding="UTF-8"))
            root=tree.getroot()
            for a in root.iter():
                if a.tag == '{http://www.springframework.org/schema/integration}service-activator':
                    if a.get('input-channel') is not None:
                        self.channelxmltext ='input-channel'
                        self.channeltext='SpringIntegrationInputChannel'
                        self.CreateaXMLactivator(file,a)
                        if a.get('output-channel') is not None:
                            self.channelxmltext ='output-channel'
                            self.count= self.count +1 
                            self.channeltext ='SpringIntegrationOutputChannel'
                            self.CreateaXMLactivator(file,a)
           
    @staticmethod
    def add_property(obj, node, prop ):
        if prop in node.attrib:
            if node.attrib[prop] in node:
                #LOG.info(' - %s: %s' % (prop, node[node.attrib[prop]]))
                obj.save_property('ChannelProperties.%s' % prop, node[node.attrib[prop]])
                      
                               
                    
                            
    def start_member(self, member):
        for anno in member.get_annotations():
            self.channeltext=""
            if anno[0].get_fullname() == 'org.springframework.integration.annotation.ServiceActivator':
                #LOG.info('anno'+ str(anno[1]))
                annvalue=anno[1]
                if annvalue['inputChannel'] is not None:
                    self.channeltext='inputChannel'
                    self.channelmetamodeltext= 'SpringIntegrationInputChannel'
                    #LOG.info('channel'+ str(annvalue['inputChannel']))
                    self.Createannsactivator(member,anno[1])
                    if annvalue['outputChannel'] is not None:
                        self.channeltext='outputChannel' 
                        self.channelmetamodeltext= 'SpringIntegrationOutputChannel'
                        self.Createannsactivator(member,anno[1])
                    
                #LOG.info('SActivatoranno'+ anno[0].get_fullname())
     
                  
                                 
    
    def end_analysis(self):
        self.result
        self.endPointNameList = []
        self.elementNameList = []
        #LOG.info("SActivator Analyzer Analyzer Ended")
        
    def Createannsactivator(self,typ,annoValue):
        annsactivator = cast.analysers.CustomObject()
        annsactivator.set_name(annoValue[self.channeltext])
        annsactivator.set_type(self.channelmetamodeltext)
        parentFile = typ.get_position().get_file() 
        annsactivator.set_parent(parentFile)
        annsactivator.set_fullname(typ.get_fullname())  
        self.fielPath = parentFile.get_fullname()
        annsactivator.set_guid(self.fielPath+annoValue[self.channeltext])
        annsactivator.save()
        annsactivator.save_position(typ.get_position())
        cast.analysers.create_link('callLink',annsactivator,typ)
        LOG.info('Spring_Service_activator object is created with name '+ annoValue[self.channeltext])
        return self.annsactivator; 
    
    def CreateaXMLactivator(self,file, a):
        try :
            if a.tag == '{http://www.springframework.org/schema/integration}service-activator':
                #LOG.info(str(a.attrib))
                #LOG.info(a.get(self.channelxmltext))
                self.count= self.count+1
                channelObj = cast.analysers.CustomObject()
                channelObj.set_name(a.get(self.channelxmltext))
                channelObj.set_type(self.channeltext)
                channelObj.set_parent(file)
                parentFile = file.get_position().get_file() 
                self.fielPath = parentFile.get_fullname()
                channelObj.set_guid(self.fielPath+a.get(self.channelxmltext)+str(self.count))
                channelObj.save()
                channelObj.save_position(file.get_position())
                xmlParsing.add_property(channelObj, a, 'ref')
                xmlParsing.add_property(channelObj, a, 'method')
                #channelObj.save_position(Bookmark(file,1,1,-1,-1))
                LOG.info("Creating xml JMS service activator object "+ a.get(self.channelxmltext))  
               
        except:
            return 
         
class xmlParsing():  
    
    @staticmethod
    def add_property(obj, ele, prop ):
        if ele.get(prop) is not None:
            LOG.debug(' - %s: %s' % (prop, ele.get(prop)))
            obj.save_property('ChannelProperties.%s' % prop, ele.get(prop))
        else:
            obj.save_property('ChannelProperties.%s' % prop, "None")
        
                      
    
