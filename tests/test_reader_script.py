#!/usr/bin/python3
"""
This is unit test script for csv_json_reader
"""
__author__ = "Manveer Singh"

import sys
import os.path
sys.path.append('{}/../'.format(os.path.dirname((os.path.abspath(__file__)))))
import pandas
import csv_json_reader as cjr
import unittest
from pandas.testing import assert_frame_equal
from unittest.mock import Mock


class TestReaderScript(unittest.TestCase):
    """
    This class with cover testing of all the methods of csv json reader script
    """
    def __init__(self, *args, **kwargs):
        super(TestReaderScript, self).__init__(*args, **kwargs)
        self.expected_data1 = {'first_name': {0: 'DELIA', 1: 'EUGENE', 2: 'BERNARDINA', 3: 'BELINDA', 4: 'REUBEN',
                                              5: 'NUMBERS', 6: 'CONCETTA', 7: 'MORTON', 8: 'SAMMIE', 9: 'CECIL'},
                               'last_name': {0: 'MCCRAE', 1: 'VANDERSTEEN', 2: 'STWART', 3: 'BRIERE', 4: 'BUROKER',
                                             5: 'KNAUB', 6: 'PALONE', 7: 'SANTILLO', 8: 'BARTELS', 9: 'SANLUIS'},
                               'siblings': {0: 5, 1: 2, 2: 1, 3: 1, 4: 1, 5: 3, 6: 1, 7: 1, 8: 1, 9: 3},
                               'favourite_food': {0: 'chicken', 1: 'Yogurt', 2: 'Mozzarella cheese', 3: 'Peanut Butter',
                                                  4: 'steak', 5: 'ice cream', 6: 'grapes', 7: 'Grapes',
                                                  8: 'Ice Cream', 9: 'Mozzarella cheese'},
                               'birth_timezone': {0: '-08:00', 1: '+01:00', 2: '+10:30', 3: '-08:00', 4: '-04:00',
                                                  5: '-09:00', 6: '+13:00', 7: '+01:00', 8: '-02:00', 9: '-08:00'},
                               'birth_timestamp': {0: 602000000000.0, 1: 853000000000.0, 2: 286000000000.0,
                                                   3: 507000000000.0, 4: 474000000000.0, 5: 190000000000.0,
                                                   6: 160000000000.0, 7: 833000000000.0, 8: 536000000000.0,
                                                   9: 223000000000.0}}
        self.expected_data2 = {'first_name': {0: 'BLAKE', 1: 'DELORIS', 2: 'CONCEPTION', 3: 'TAMMIE', 4: 'ANGELES'},
                               'last_name': {0: 'MCCLOSKY', 1: 'SKOWRON', 2: 'KOSAKOWSKI', 3: 'GUERRIER', 4: 'UREN'},
                               'siblings': {0: 3, 1: 3, 2: 1, 3: 1, 4: 7},
                               'favourite_food': {0: 'Banana', 1: 'Pizza', 2: 'pizza', 3: 'Cashew nuts',
                                                  4: 'Cashew nuts'},
                               'birth_timezone': {0: '+06:00', 1: '-04:00', 2: '-07:00', 3: '+06:00', 4: '-05:00'},
                               'birth_timestamp': {0: 223598517000, 1: 915739620000, 2: 601102620000, 3: 726219060000,
                                                   4: 442609740000}}
        self.expected_data_frame1 = pandas.DataFrame(self.expected_data1)
        self.expected_data_frame2 = pandas.DataFrame(self.expected_data2)
        self.file1 = r"sample.csv"
        self.file2 = r"sample.json"
        self.file3 = r"sample.JSON"
        self.file4 = r"sample"

    def test_file_extension(self):
        """
        Method get_file_extension() will be tested with different file extensions
        """
        # Test for .csv file
        data = cjr.get_file_extension(self.file1)
        self.assertEqual('csv', data)

        # Test for .json file
        data = cjr.get_file_extension(self.file2)
        self.assertEqual('json', data)

        # Test to cover upper case extension
        data = cjr.get_file_extension(self.file3)
        self.assertEqual('json', data)

        # Test for files without any extension
        data = cjr.get_file_extension(self.file4)
        self.assertEqual('', data)

    def test_file_reader(self):
        """
        Method test_file_reader() will be tested with different files
        """
        # Test for .csv file
        actual_data1 = cjr.file_reader(self.file1)
        assert_frame_equal(self.expected_data_frame1, actual_data1)

        # Test for .json file
        actual_data2 = cjr.file_reader(self.file2)
        assert_frame_equal(self.expected_data_frame2, actual_data2)

        # Test for extension not supported
        cjr.get_file_extension = Mock()
        cjr.get_file_extension.return_value = 'jpg'
        with self.assertRaises(NotImplementedError):
            cjr.file_reader(self.file1)

    def test_avg_sibling(self):
        """
        Method get_avg_siblings() will be tested with 2 different data frames
        """
        # Test with data frame 1
        actual_output1 = cjr.get_avg_siblings(self.expected_data_frame1)
        self.assertEqual(2, actual_output1)

        # Test with data frame 2
        actual_output2 = cjr.get_avg_siblings(self.expected_data_frame2)
        self.assertEqual(3, actual_output2)

    def test_top_food(self):
        """
        Method get_top_food() will be tested with 2 different data frames
        """
        # Test with data frame 1
        actual_output1 = cjr.get_top_food(self.expected_data_frame1)
        self.assertDictEqual({'Ice Cream': 2, 'Mozzarella Cheese': 2, 'Grapes': 2}, actual_output1.to_dict())

        # Test with data frame 2
        actual_output2 = cjr.get_top_food(self.expected_data_frame2)
        self.assertDictEqual({'Pizza': 2, 'Cashew Nuts': 2, 'Banana': 1}, actual_output2.to_dict())

    def test_convert_time(self):
        """
        Method convert_time() will be tested with 4 different data sets
        """
        # Test with small positive value
        sec_output1 = cjr.convert_time("2:30")
        self.assertEqual(9000, sec_output1)

        # Test with big positive value
        sec_output1 = cjr.convert_time("14:30")
        self.assertNotEqual(20000, sec_output1)

        # Test with small negative value
        sec_output1 = cjr.convert_time("-3:30")
        self.assertEqual(-12600, sec_output1)

        # Test with big negative value
        sec_output1 = cjr.convert_time("-13:30")
        self.assertEqual(-48600, sec_output1)

    def test_birthday_months(self):
        """
        Method get_birthday_mnths() will be tested with 2 different data frames
        """
        # Test with data frame 1
        actual_output1 = cjr.get_birthday_mnths(self.expected_data_frame1)
        self.assertDictEqual({'January': 8, 'February': 0, 'March': 0, 'April': 0, 'May': 1, 'June': 0, 'July': 0,
                              'August': 0, 'September': 0, 'October': 0, 'November': 0, 'December': 1}, actual_output1)

        # Test with data frame 2
        actual_output2 = cjr.get_birthday_mnths(self.expected_data_frame2)
        self.assertDictEqual({'January': 4, 'February': 1, 'March': 0, 'April': 0, 'May': 0, 'June': 0, 'July': 0,
                              'August': 0, 'September': 0, 'October': 0, 'November': 0, 'December': 0}, actual_output2)


if __name__ == '__main__':
    unittest.main()

