import unittest

from regexer import extract_markdown_images, extract_markdown_links

class TestRegexer(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKa=qIh.gif) and ![obi wan](https://i.imgur.com/obiwan.jpg) images."
        expected_result = [("rick roll", "https://i.imgur.com/aKa=qIh.gif"),
                           ("obi wan", "https://i.imgur.com/obiwan.jpg")]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_no_images(self):
        text = "This is text with no images."
        expected_result = []
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_single_image(self):
        text = "Here is an image: ![sample](http://example.com/sample.png)"
        expected_result = [("sample", "http://example.com/sample.png")]
        self.assertEqual(extract_markdown_images(text), expected_result)

    def test_extract_markdown_links(self):
        text = "This is text with a [Google](https://www.google.com) link and a [GitHub](https://www.github.com) link."
        expected_result = [("Google", "https://www.google.com"),
                           ("GitHub", "https://www.github.com")]
        self.assertEqual(extract_markdown_links(text), expected_result) 

    def test_no_links(self):
        text = "This is text with no links."
        expected_result = []
        self.assertEqual(extract_markdown_links(text), expected_result) 

    def test_single_link(self):
        text = "Here is a link to [OpenAI](https://www.openai.com)."
        expected_result = [("OpenAI", "https://www.openai.com")]
        self.assertEqual(extract_markdown_links(text), expected_result)

    