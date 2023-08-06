import unittest
from test import *
from dripy.dripy import PasonData

class Test_PasonData(unittest.TestCase):

    def setUp(self):
        self.pason_data = PasonData(TEST_PASON_DATA)        

    def test_pason_time(self):
        """Tests that the time attribute returns expected values.
        
        """
        time = self.pason_data.time[0:10]
        self.assertListEqual(time, TEST_EXPECTED_PASON_TIME)
    
    def test_pason_rpm_attr(self):
        """Tests that the rpm attribute returns expected values.
        
        """
        rpm = self.pason_data.rpm[2000:2010]
        self.assertListEqual(rpm, TEST_EXPECTED_PASON_RPM)
    
    def test_pason_rpm_data(self):
        """Tests that the 'rpm' entry in the `data` dictionary returns expected values.
        
        """
        rpm = self.pason_data.data['rpm'][2000:2010].values
        self.assertListEqual(list(rpm), TEST_EXPECTED_PASON_RPM)
    
    def test_pason_rpm_data_csv_name(self):
        """Tests that the 'rotary_rpm' entry in the `data` returns expected values.
        
        """
        rpm = self.pason_data.data['rotary_rpm'][2000:2010].values
        self.assertListEqual(list(rpm), TEST_EXPECTED_PASON_RPM)
        
    def tearDown(self):
        return
    
if __name__ == '__main__':
    unittest.main()
