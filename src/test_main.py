import unittest
from main import extract_title

class TestMainFunctionality(unittest.TestCase):
    def test_title_case(self):
        markdown = """
            # hello world
            This is a sample markdown document.
        """

        self.assertEqual(extract_title(markdown), "hello world")

    def test_no_heading(self):
        markdown = """
            This is a sample markdown document without a heading.
        """

        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        
        self.assertTrue("No heading found in markdown." in str(context.exception))
    
    def test_no_h1_heading(self):
        markdown = """
            ## Subheading
            This is a sample markdown document.
        """

        with self.assertRaises(Exception) as context:
            extract_title(markdown)

        self.assertTrue("No first level heading found in markdown." in str(context.exception))

if __name__ == '__main__':
    unittest.main()