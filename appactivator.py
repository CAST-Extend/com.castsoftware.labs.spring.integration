'''
Created on Dec 1, 2017

@author: NNA
'''

import cast.application
import logging
import ast
import re

class ExtensionApplication(cast.application.ApplicationLevelExtension):

    def end_application(self, application):
        logging.info("Running code at the end of an Application")
        self.CreateInputoutputlink(application)
        #self.Createchannellink(application,'SpringIntegrationrequestChannel')
        #self.Createchannellink(application,'SpringIntegrationreplyChannel')
        self.Createxmlchannellink(application,'SpringIntegrationInputChannel')
        self.Createxmlchannellink(application,'SpringIntegrationOutputChannel')
        self.Creategatewayxmlchannellink(application,'SpringIntegrationrequestChannel')
        self.Creategatewayxmlchannellink(application,'SpringIntegrationreplyChannel')
        self.Createxmlchannellink(application,'SpringIntegrationChannel')
        
    def Createchannellink(self,application,channeltext):
        channelObjectReferences = list(application.search_objects(category=channeltext, load_properties=False))
        if len(channelObjectReferences)>0:
           
            for channelObject in channelObjectReferences : 
                method_name = channelObject.get_name()
                javaMethodObjectReferences = list(application.search_objects(category='JV_METHOD', name=method_name, load_properties=False))
                #logging.info('method_name --> '+method_name)
                if len(javaMethodObjectReferences)>0:
                    for javaObject in javaMethodObjectReferences : 
                        javamethod_name = javaObject.get_name()
                        if javamethod_name ==  method_name:
                            #logging.info('method_name --> '+javamethod_name)
                            cast.application.create_link("callLink", channelObject, javaObject, bookmark=None)
                            logging.debug("link created-->" + method_name)
        return self.Createchannellink; 
    #need modification
    def Createxmlchannellink(self,application,channeltext):
        channelObjectReferences = list(application.search_objects(category=channeltext, load_properties= True))
        if len(channelObjectReferences)>0:
            #javaMethodObjectReferences = list(application.search_objects(category='JV_METHOD', load_properties=False))
            #javaMethodclassReferences = list(application.search_objects(category='JV_CLASS', load_properties=False))
            for channelObject in channelObjectReferences :
                    #logging.info('method_name --> ' + channelObject.get_name())
                    xml_type = channelObject.get_property('ChannelProperties.sourcefile')
                    if xml_type != None:
                        if xml_type.lower() == 'xml':
                            method_name = channelObject.get_property('ChannelProperties.method')
                            javaMethodObjectReferences = list(application.search_objects(category='JV_METHOD', name=method_name,  load_properties=False))
                            if len(javaMethodObjectReferences)>0:
                                for javaObject in javaMethodObjectReferences : 
                                    javamethod_name = javaObject.get_name()
                                    if javamethod_name ==  method_name:
                                        #logging.info('method_name --> '+javamethod_name)
                                        if channeltext == 'SpringIntegrationOutputChannel' :
                                            cast.application.create_link("callLink",javaObject,  channelObject, bookmark=None)
                                        else:
                                            cast.application.create_link("callLink", channelObject, javaObject, bookmark=None) 
                                        logging.debug("link created-->" + method_name)
                                        classmethod_name = channelObject.get_property('ChannelProperties.ref')
                                        javaMethodclassReferences = list(application.search_objects(category='JV_CLASS', name=classmethod_name, load_properties=False))
                                        if len(javaMethodclassReferences)>0:
                                            for javaclassObject in javaMethodclassReferences : 
                                                #logging.info('class_name --> ' + javaclassObject.get_name())
                                                javaclassmethod_name = javaclassObject.get_name()
                                                if javaclassmethod_name ==  classmethod_name:
                                                    #logging.info('method_name --> '+javaclassmethod_name)
                                                    if channeltext == 'SpringIntegrationOutputChannel' :
                                                        cast.application.create_link("callLink",  javaclassObject,channelObject, bookmark=None)
                                                    else:
                                                        cast.application.create_link("callLink", channelObject, javaclassObject, bookmark=None)
                                                    logging.debug("link created-->" + classmethod_name) 
                                        
    def CreateInputoutputlink(self,application):
        channelObjectReferences = list(application.search_objects(category='SpringIntegrationInputChannel', load_properties= True))
        inpMethodObjectReferences = list(application.search_objects(category='SpringIntegrationOutputChannel', load_properties= True))
        if len(channelObjectReferences)>0:
            for channelObject in channelObjectReferences :
                    #logging.info('method_name --> ' + channelObject.get_name())
                    input_type = channelObject.get_property('ChannelProperties.sourcetype')
                    input_name = channelObject.get_name()
                    if input_type.lower() == 'aggregator' : 
                        for outputObject in inpMethodObjectReferences : 
                            output_type = outputObject.get_property('ChannelProperties.sourcetype')
                            output_name = outputObject.get_name()
                            if (output_name ==  input_name and output_type == 'ServiceActivator') :
                            #logging.info('method_name --> '+javamethod_name)
                                    cast.application.create_link("callLink",outputObject,  channelObject, bookmark=None)
                                    logging.debug("inputoutput annotation  link created-->" + output_name)
                            if (output_name ==  input_name and output_type == 'service-activator'):
                                    cast.application.create_link("callLink",outputObject,  channelObject, bookmark=None)
                                    logging.debug("inputoutput xml link created-->" + output_name)                               
                                    
    def Creategatewayxmlchannellink(self,application,channeltext):
        channelObjectReferences = list(application.search_objects(category=channeltext, load_properties= True))
        if len(channelObjectReferences)>0:
                #javaMethodclassReferences = list(application.search_objects(category='JV_METHOD', load_properties=False))
                #javainterfaceclassReferences = list(application.search_objects(category='JV_INTERFACE', load_properties=False))
                for channelObject in channelObjectReferences :
                        xml_type = channelObject.get_property('gatewayProperties.sourcefile')
                        #logging.info('xmltype   '+ xml_type)
                        gateway_type = channelObject.get_property('gatewayProperties.sourcetype')
                        #logging.info('gateway '+ gateway_type)
                        if xml_type != None and gateway_type !=None:
                            if xml_type.lower() == 'xml' and (gateway_type.lower() == 'gateway' or gateway_type.lower() == 'jms'):
                                interface_name = channelObject.get_property('gatewayProperties.serviceinterface')
                                javainterfaceclassReferences = list(application.search_objects(category='JV_INTERFACE', name=interface_name,  load_properties=False))
                                if len(javainterfaceclassReferences)>0:
                                    for jinterface in javainterfaceclassReferences :
                                        #interface_name = channelObject.get_property('gatewayProperties.serviceinterface')
                                        jinterfacename =jinterface.get_fullname()
                                        if interface_name ==  jinterfacename :
                                            #logging.info('jmsgatewaymethod_name --> '+jinterfacename)
                                            if channeltext == 'SpringIntegrationreplyChannel' :
                                                cast.application.create_link("callLink",  jinterface,channelObject, bookmark=None)
                                            else:
                                                cast.application.create_link("callLink", channelObject, jinterface, bookmark=None)
                                            #logging.debug("link created-->" + interface_name)        
                                            #logging.info('java interface    '+ str(jinterface.get_fullname()))
                                fullclassmethod_name = channelObject.get_property('gatewayProperties.methodname')
                                javaMethodclassReferences = list(application.search_objects(category='JV_METHOD', name=fullclassmethod_name,  load_properties=False))
                                if len(javaMethodclassReferences)>0:
                                    for javaclassObject in javaMethodclassReferences : 
                                        #logging.info('class_name --> ' + javaclassObject.get_name())
                                        javaclassmethod_name = javaclassObject.get_name()
                                        
                                        if javaclassmethod_name ==  fullclassmethod_name:
                                            #logging.info('method_name --> '+javaclassmethod_name)
                                            if channeltext == 'SpringIntegrationreplyChannel' :
                                                cast.application.create_link("callLink",  javaclassObject,channelObject, bookmark=None)
                                            else:
                                                cast.application.create_link("callLink", channelObject, javaclassObject, bookmark=None)
                                            logging.debug("link created last gateway -->" + fullclassmethod_name)        
                                
                        