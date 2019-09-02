import unittest
from sensor import process_data

class TestDataProcessor(unittest.TestCase):
    def test_process_data(self):
        '''
        tests success
        '''
        data = {'content': {'temperature_f': 32}}
        new_data = process_data(data)
        self.assertEqual(0.0, new_data['content']['temperature_c'],
                         "32 F == 0 C") 

    def test_malformed_input(self):
        '''
        tests malformed input
        '''
        data = {'content': {'temper_f': 32}}
        new_data = process_data(data)
        self.assertEqual(None, new_data, 'not possible to parse data')



if __name__ == '__main__':
    unittest.main()