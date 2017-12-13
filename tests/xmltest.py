
import unittest
from cast.analysers.test import JEETestAnalysis

class Test(unittest.TestCase):


    def test_xml(self):     
        analysis = JEETestAnalysis()       
        analysis.add_selection('ServiceactivatorTest/src/package1')
        analysis.add_dependency('com.castsoftware.internal.platform')
        analysis.set_verbose()
        analysis.run()
        
if __name__ == "__main__":
    unittest.main()