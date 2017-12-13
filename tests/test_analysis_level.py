import unittest
import cast.analysers.test
from cast.analysers import filter
import cast.analysers.log 



class Test(unittest.TestCase):


     def testName(self):
        analysis = cast.analysers.test.JEETestAnalysis()
        
        analysis.add_selection('ServiceactivatorTest/src/package1')
        analysis.add_dependency('com.castsoftware.internal.platform')
        analysis.set_verbose()
        analysis.run()
        
        
       # application = cast.analysers.test.JEETestAnalysis()
        
        '''ServiceClassFile = analysis.get_object_by_name('SAjms.java','JV_FILE')
        self.assertTrue(ServiceClassFile)
        print("found file" +str(ServiceClassFile))
        
        activator= analysis.get_object_by_name('FulfillmentOrderInboundJmsEndpoint','JV_CLASS')
        self.assertTrue(activator)
        print("found class" +str(activator))
        
        annactivator= analysis.get_object_by_name('consumeAndProcessFulfillment','JV_METHOD')
        self.assertTrue(annactivator)
        print("found method" +str(annactivator))
        '''
        
     
        
       
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

