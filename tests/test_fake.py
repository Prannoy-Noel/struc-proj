from .context import sample

import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        source = r'./data/source/' + doc_ID + '/'
        destination = r'./data/destination/' + doc_ID + '/'

        #calling the function
        sample.extract_key_value_pairs('6', 'yes', source, destination)
        assert True


if __name__ == '__main__':
    unittest.main()
