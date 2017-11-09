from unittest import TestCase
from functions import *
import pathlib

current_dir = pathlib.Path(__file__).parent

# print(current_dir)


class TestReadsecrets(TestCase):
    def test_readsecrets(self):

        mock_input_val = str(current_dir) + "/test-files/secret_test.json"

        expected_positive_return_val = 'secret/path'

        self.assertEqual(readsecrets(mock_input_val)['secrets'][0]['path'],
                         expected_positive_return_val)

