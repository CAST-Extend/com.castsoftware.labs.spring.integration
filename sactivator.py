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
from Cython.Compiler.Options import annotate


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
        self.annocount = 0
        
               
    def start_analysis(self,options):
        LOG.info('Successfully service activator analyzer Started')
        options.add_classpath('jars')
        options.handle_xml_with_xpath('/beans')
        options.handle_xml_with_xpath('/')
        
      
               
     
       
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
                #LOG.info(str(a.tag))
                #service activator
                self.findXMLInputOutput(a, '{http://www.springframework.org/schema/integration}service-activator', file)
                self.findXMLInputOutput(a, '{http://www.springframework.org/schema/integration}transformer', file)
                self.findXMLInputOutput(a, '{http://www.springframework.org/schema/integration}filter', file)
                self.findXMLInputOutput(a, '{http://www.springframework.org/schema/integration}splitter', file)           
                self.findgatewayXMLInputOutput(a, '{http://www.springframework.org/schema/integration}gateway', file)
                self.findXMLInputOutput(a, '{http://www.springframework.org/schema/integration}router', file) 
                self.findXMLInputOutput(a, '{http://www.springframework.org/schema/integration}aggregator', file) 
                self.findXMLchannel(a, '{http://www.springframework.org/schema/integration}inbound-channel-adapter', file) 
                self.findXMLchannel(a, '{http://www.springframework.org/schema/integration}publisher', file) 
                                    
                            
    def start_member(self, member):
        for anno in member.get_annotations():
            self.findannotation(anno, 'org.springframework.integration.annotation.ServiceActivator', member)
            self.findannotation(anno, 'org.springframework.integration.annotation.Transformer', member)
            self.findannotation(anno, 'org.springframework.integration.annotation.Filter', member)
            self.findrouterannotation(anno, 'org.springframework.integration.annotation.Router', member)
            self.findannotation(anno, 'org.springframework.integration.annotation.Splitter', member)
            self.findaggregatorannotation(anno, 'org.springframework.integration.annotation.Aggregator', member)
            self.findgatewayannotation(anno, 'org.springframework.integration.annotation.Gateway', member)
            self.findmsggatewayannotation(anno, 'org.springframework.integration.annotation.MessagingGateway', member)
            self.findinboundpublisherannotation(anno, 'org.springframework.integration.annotation.InboundChannelAdapter', member)
            self.findinboundpublisherannotation(anno, 'org.springframework.integration.annotation.Publisher', member)
                      
                #LOG.info('SActivatoranno'+ anno[0].get_fullname())
                                   
    
    def end_analysis(self):
        self.result
        self.endPointNameList = []
        self.elementNameList = []
        #LOG.info("SActivator Analyzer Analyzer Ended")
        
    def Createannsactivator(self,typ,annoValue, annotext):
        annsactivator = cast.analysers.CustomObject()
        annsactivator.set_name(annoValue[self.channeltext])
        annsactivator.set_type(self.channelmetamodeltext)
        parentFile = typ.get_position().get_file() 
        annsactivator.set_parent(parentFile)
        annsactivator.set_fullname(typ.get_fullname())  
        self.fielPath = parentFile.get_fullname()
        self.count= self.count+1
        annsactivator.set_guid(self.fielPath+annoValue[self.channeltext] +str(self.count))
        annsactivator.save()
        annsactivator.save_position(typ.get_position())
        if self.channeltext =='outputChannel' or self.channeltext =='defaultReplyChannel':
            cast.analysers.create_link('callLink',typ, annsactivator)
        else:
            cast.analysers.create_link('callLink', annsactivator, typ )
        LOG.info(annotext+  '   object is created with name '+ annoValue[self.channeltext])
        if self.channelmetamodeltext != 'SpringIntegrationrequestChannel' and self.channelmetamodeltext != 'SpringIntegrationreplyChannel':  
            Bean= typ.get_fullname()
            xmlParsing.addtype_property(annsactivator, 'ref', 'Annotation')
            xmlParsing.addtype_property(annsactivator, 'method', Bean)
            xmlParsing.addtype_property(annsactivator, 'sourcetype', annotext.rsplit('.', 1)[-1])
            xmlParsing.addtype_property(annsactivator, 'sourcefile', 'java')
        return self.annsactivator; 
    
    def findannotation(self, anno, annotext, member):
        if anno[0].get_fullname() == annotext:
           # LOG.info('anno'+ str(anno[1]))
            annvalue=anno[1]
            if annvalue['inputChannel'] is not None:
                self.channeltext='inputChannel'
                self.channelmetamodeltext= 'SpringIntegrationInputChannel'
                LOG.info('channel'+ str(annvalue['inputChannel']))
                self.Createannsactivator(member,anno[1],  annotext)
                if annvalue['outputChannel'] is not None:
                    self.channeltext='outputChannel' 
                    self.channelmetamodeltext= 'SpringIntegrationOutputChannel'
                    self.Createannsactivator(member,anno[1],  annotext) 
                    
    def findinboundpublisherannotation(self, anno, annotext, member):
        if anno[0].get_fullname() == annotext:
           # LOG.info('anno'+ str(anno[1]))
            annvalue=anno[1]
            if annvalue['Channel'] is not None:
                self.channeltext='Channel'
                self.channelmetamodeltext= 'SpringIntegrationChannel'  
                self.Createannsactivator(member,anno[1],  annotext)  
                
                           
    def findrouterannotation(self, anno, annotext, member):
        if anno[0].get_fullname() == annotext:
           # LOG.info('anno'+ str(anno[1]))
            annvalue=anno[1]
            if annvalue['inputChannel'] is not None:
                self.channeltext='inputChannel'
                self.channelmetamodeltext= 'SpringIntegrationInputChannel'
                LOG.info('channel'+ str(annvalue['inputChannel']))
                self.Createannsactivator(member,anno[1],  annotext)
                if annvalue['defaultOutputChannel'] is not None:
                    self.channeltext='defaultOutputChannel' 
                    self.channelmetamodeltext= 'SpringIntegrationOutputChannel'
                    self.Createannsactivator(member,anno[1],  annotext)    
                      
    def findaggregatorannotation(self, anno, annotext, member):
        if anno[0].get_fullname() == annotext:
            #LOG.info('anno'+ str(anno[1]))
            annvalue=anno[1]
            if annvalue['inputChannel'] is not None:
                self.channeltext='inputChannel'
                self.channelmetamodeltext= 'SpringIntegrationInputChannel'
                LOG.info('channel'+ str(annvalue['inputChannel']))
                self.Createannsactivator(member,anno[1],  annotext)
                if annvalue['outputChannel'] is not None:
                    self.channeltext='outputChannel' 
                    self.channelmetamodeltext= 'SpringIntegrationOutputChannel'
                    self.Createannsactivator(member,anno[1],  annotext) 
                    if annvalue['discardChannel'] is not None:
                        self.channeltext='discardChannel' 
                        self.channelmetamodeltext= 'SpringIntegrationDiscardChannel'
                        self.Createannsactivator(member,anno[1],  annotext) 
                        
    def findgatewayannotation(self, anno, annotext, member):
        if anno[0].get_fullname() == annotext:
           # LOG.info('anno'+ str(anno[1]))
            annvalue=anno[1]
            if annvalue['requestChannel'] is not None:
                self.channeltext='requestChannel'
                self.channelmetamodeltext= 'SpringIntegrationrequestChannel'
                LOG.info('channel'+ str(annvalue['requestChannel']))
                self.Createannsactivator(member,anno[1],  annotext)
                if annvalue['replyChannel'] is not None:
                    self.channeltext='replyChannel' 
                    self.channelmetamodeltext= 'SpringIntegrationreplyChannel'
                    self.Createannsactivator(member,anno[1],  annotext) 
                    
    def findmsggatewayannotation(self, anno, annotext, member):
        if anno[0].get_fullname() == annotext:
           # LOG.info('anno'+ str(anno[1]))
            annvalue=anno[1]
            if annvalue['defaultRequestChannel'] is not None:
                self.channeltext='defaultRequestChannel'
                self.channelmetamodeltext= 'SpringIntegrationrequestChannel'
                LOG.info('channel'+ str(annvalue['defaultRequestChannel']))
                self.Createannsactivator(member,anno[1],  annotext)
                if annvalue['defaultReplyChannel'] is not None:
                    self.channeltext='defaultReplyChannel' 
                    self.channelmetamodeltext= 'SpringIntegrationreplyChannel'
                    self.Createannsactivator(member,anno[1],  annotext) 
                    
    def findXMLInputOutput(self, a, annotext, file):  
        #LOG.info('xml '+ str(a.tag))              
        if a.tag == annotext:
            if a.get('input-channel') is not None:
                self.channelxmltext ='input-channel'
                self.channeltext='SpringIntegrationInputChannel'
                self.CreateaXMLactivator(file,a, annotext)
                if a.get('output-channel') is not None:
                    self.channelxmltext ='output-channel'
                    self.count= self.count +1 
                    self.channeltext ='SpringIntegrationOutputChannel'
                    self.CreateaXMLactivator(file,a,annotext)
                 
           
                            
    def findgatewayXMLInputOutput(self, a, annotext, file):  
        #LOG.info('xml'+ str(a.tag))              
        if a.tag == annotext:
            for node in a.getiterator():
                if node.tag=='bean':
                    LOG.info("inside beans child")
                                
            if a.get('default-request-channel') is not None:
                self.channelxmltext ='default-request-channel'
                self.channeltext='SpringIntegrationrequestChannel'
                self.CreateagatewayXML(file,a, annotext)
                if a.get('default-reply-channel') is not None:
                    self.channelxmltext ='default-reply-channel'
                    self.count= self.count +1 
                    self.channeltext ='SpringIntegrationreplyChannel'
                    self.CreateagatewayXML(file,a,annotext) 
            
    def findXMLchannel(self, a, annotext, file):  
        #LOG.info('xml'+ str(a.tag))              
        if a.tag == annotext:
            if a.get('channel') is not None:
                self.channelxmltext ='channel'
                self.channeltext='SpringIntegrationChannel'
                self.CreateaXMLactivator(file,a, annotext)
               
                                          
    def CreateaXMLactivator(self,file, a, xsdtext):
        try :
            if a.tag == xsdtext:
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
                xmlParsing.addtype_property(channelObj, 'sourcetype',  xsdtext.rsplit('}', 1)[-1])
                xmlParsing.addtype_property(channelObj, 'sourcefile', 'XML')
                #channelObj.save_position(Bookmark(file,1,1,-1,-1))
                LOG.info('Creating xml JMS '+ xsdtext + ' object '+ a.get(self.channelxmltext))  
               
        except:
            return 
    def CreateagatewayXML(self,file, a, xsdtext):
        try :
            if a.tag == xsdtext:
                #LOG.info('inside  gateway  '+ str(a.attrib))
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
                LOG.info('Creating xml gateway JMS '+ xsdtext + ' object '+ a.get(self.channelxmltext)) 
                xmlParsing.addgatewaytype_property(channelObj, 'sourcetype',  xsdtext.rsplit('}', 1)[-1])
                xmlParsing.addgatewaytype_property(channelObj, 'sourcefile', 'XML')
                xmlParsing.add_gatewayproperty(channelObj, a, 'id','id')
                xmlParsing.add_gatewayproperty(channelObj, a, 'serviceinterface', 'service-interface')
                if a.find('{http://www.springframework.org/schema/integration}method') is not None:
                    node=a.find('{http://www.springframework.org/schema/integration}method')
                    xmlParsing.add_gatewayproperty(channelObj, node, 'methodname','name')
                    if node.find('{http://www.springframework.org/schema/integration}header') is not None:
                        head= node.find('{http://www.springframework.org/schema/integration}header')
                        xmlParsing.add_gatewayproperty(channelObj, head, 'headername','name')
                        xmlParsing.add_gatewayproperty(channelObj, head, 'headervalue','value')
                else:
                    xmlParsing.addgatewaytype_property(channelObj, 'methodname','None')
                    xmlParsing.addgatewaytype_property(channelObj, 'headername','None')
                    xmlParsing.addgatewaytype_property(channelObj, 'headervalue','None')
                    
                LOG.info('Creating xml gateway JMS prop '+ xsdtext + ' object '+ a.get(self.channelxmltext)) 
               
                            
                
                
                #if  ET.SubElement(a, 'method') is not None:
                    #LOG.info ('inside method ' + str(ET.SubElement(a, 'method')))
                    #b= ET.SubElement(a, 'method')
                    #LOG.info ('inside method gateway')
                    #channelObj.save_position(Bookmark(file,1,1,-1,-1))
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
            
    @staticmethod
    def add_gatewayproperty(obj, ele, prop, proptext ):
        if ele.get(proptext) is not None:
            LOG.debug(' - %s: %s' % (prop, ele.get(proptext)))
            obj.save_property('gatewayProperties.%s' % prop, ele.get(proptext) )
        else:
            obj.save_property('gatewayProperties.%s' % prop, "None")       

    @staticmethod
    def addtype_property(obj,  prop, proptext):
        if proptext is not None:
            obj.save_property('ChannelProperties.%s' % prop, proptext)
        else:
            obj.save_property('ChannelProperties.%s' % prop, "None") 
            
    @staticmethod
    def addgatewaytype_property(obj,  prop, proptext):
        if proptext is not None:
            obj.save_property('gatewayProperties.%s' % prop, proptext)
        else:
            obj.save_property('gatewayProperties.%s' % prop, "None") 

