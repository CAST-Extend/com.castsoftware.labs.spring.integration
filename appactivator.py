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
        self.Createchannellink(application,'SpringIntegrationInputChannel')
        self.Createchannellink(application,'SpringIntegrationOutputChannel')
        self.Createxmlchannellink(application,'SpringIntegrationInputChannel')
        self.Createxmlchannellink(application,'SpringIntegrationOutputChannel')
        
    def Createchannellink(self,application,channeltext):
        channelObjectReferences = list(application.search_objects(category=channeltext, load_properties=False))
        javaMethodObjectReferences = list(application.search_objects(category='JV_METHOD', load_properties=False))
        if len(channelObjectReferences)>0:
            for channelObject in channelObjectReferences : 
                method_name = channelObject.get_name()
                #logging.info('method_name --> '+method_name)
                for javaObject in javaMethodObjectReferences : 
                    javamethod_name = javaObject.get_name()
                    if javamethod_name ==  method_name:
                        #logging.info('method_name --> '+javamethod_name)
                        cast.application.create_link("callLink", channelObject, javaObject, bookmark=None)
                        #logging.debug("link created-->" + method_name)
        return self.Createchannellink; 
    #need modification
    def Createxmlchannellink(self,application,channeltext):
        channelObjectReferences = list(application.search_objects(category=channeltext, load_properties= True))
        javaMethodObjectReferences = list(application.search_objects(category='JV_METHOD', load_properties=False))
        javaMethodclassReferences = list(application.search_objects(category='JV_CLASS', load_properties=False))
        if len(channelObjectReferences)>0:
            for channelObject in channelObjectReferences :
                    logging.info('method_name --> ' + channelObject.get_name())
                    method_name = channelObject.get_property('ChannelProperties.method')
                    for javaObject in javaMethodObjectReferences : 
                        javamethod_name = javaObject.get_name()
                        if javamethod_name ==  method_name:
                            #logging.info('method_name --> '+javamethod_name)
                            cast.application.create_link("callLink", channelObject, javaObject, bookmark=None)
                            logging.debug("link created-->" + method_name)
                            for javaclassObject in javaMethodclassReferences : 
                                javaclassmethod_name = javaclassObject.get_name()
                                classmethod_name = channelObject.get_property('ChannelProperties.ref')
                                if javaclassmethod_name ==  classmethod_name:
                                    #logging.info('method_name --> '+javaclassmethod_name)
                                    cast.application.create_link("callLink", channelObject, javaclassObject, bookmark=None)
                                    logging.debug("link created-->" + classmethod_name)       
                            
                        