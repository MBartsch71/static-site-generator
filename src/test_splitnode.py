import unittest

from textnode import TextNode, TextType
from splitnode import split_nodes_at_delimiter, split_nodes_links, split_nodes_images, text_to_textnodes

class TestSplitNode(unittest.TestCase):
    def test_split_node_bold(self):
        text = TextNode("This is a text with a **bold** phrase in the middle.", TextType.TEXT)
        expected_result = [TextNode("This is a text with a ", TextType.TEXT),
                           TextNode("bold", TextType.BOLD),
                           TextNode(" phrase in the middle.", TextType.TEXT)]
        self.assertEqual(
            split_nodes_at_delimiter(text, "**", TextType.BOLD),
            expected_result
        ) 

    def test_split_node_italic(self):
        text = TextNode("This is _italic_ text.", TextType.TEXT)
        expected_result = [TextNode("This is ", TextType.TEXT),
                           TextNode("italic", TextType.ITALIC),
                           TextNode(" text.", TextType.TEXT)]
        self.assertEqual(
            split_nodes_at_delimiter(text, "_", TextType.ITALIC),
            expected_result
        )

    def test_split_node_code(self):
        text = TextNode("Here is some `code` in the text.", TextType.TEXT)
        expected_result = [TextNode("Here is some ", TextType.TEXT),
                           TextNode("code", TextType.CODE),
                           TextNode(" in the text.", TextType.TEXT)]
        self.assertEqual(
            split_nodes_at_delimiter(text, "`", TextType.CODE),
            expected_result
        )
    
    def test_split_node_no_delimiter(self):
        text = TextNode("This is plain text.", TextType.TEXT)
        expected_result = [TextNode("This is plain text.", TextType.TEXT)]
        self.assertEqual(
            split_nodes_at_delimiter(text, "**", TextType.BOLD),
            expected_result
        )
    
    def test_split_node_unmatched_delimiter(self):
        text = TextNode("This is **bold text with no end.", TextType.TEXT)
        expected_result = [TextNode("This is **bold text with no end.", TextType.TEXT)]
        self.assertEqual(
                split_nodes_at_delimiter(text, "**", TextType.BOLD), 
                expected_result)

    def test_split_node_non_text_node(self):
        text = TextNode("This is a link", TextType.LINK, "http://example.com")
        expected_result = [TextNode("This is a link", TextType.LINK, "http://example.com")]
        self.assertEqual(
            split_nodes_at_delimiter(text, "**", TextType.BOLD),
            expected_result
        )

    def test_split_multiple_nodes(self):
        text = TextNode("This is **bold** and another **bold** part.", TextType.TEXT)
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" part.", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_at_delimiter(text, "**", TextType.BOLD),
            expected_result
        )

    def test_split_node_links(self):
        text = TextNode("This is a text with a link [to boot dev](https://www.boot.dev) and another [to youtube](https://www.youtube.com) in it.", TextType.TEXT)
        expected_result = [
            TextNode("This is a text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_links(text), expected_result)
        
    def test_split_node_links_no_links(self):
        text = TextNode("This is a text with no links.", TextType.TEXT)
        expected_result = [TextNode("This is a text with no links.", TextType.TEXT)]
        self.assertEqual(
            split_nodes_links(text), expected_result)
        
    def test_split_node_images(self):
        text = TextNode("This is a text with an image ![alt text](https://www.example.com/image.png) in it.", TextType.TEXT)
        expected_result = [
            TextNode("This is a text with an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://www.example.com/image.png"),
            TextNode(" in it.", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_images(text), expected_result)
        
    def test_split_node_images_no_images(self):
        text = TextNode("This is a text with no images.", TextType.TEXT)
        expected_result = [TextNode("This is a text with no images.", TextType.TEXT)]
        self.assertEqual(
            split_nodes_images(text), expected_result)
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_result = [
                            TextNode("This is ", TextType.TEXT),
                            TextNode("text", TextType.BOLD),
                            TextNode(" with an ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word and a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" and an ", TextType.TEXT),
                            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                            TextNode(" and a ", TextType.TEXT),
                            TextNode("link", TextType.LINK, "https://boot.dev")
                            ]
        self.assertEqual( text_to_textnodes(text), expected_result)
    
    def test_text_to_textnodes_2(self):
        text = "This is _italic_ text with an image ![picture](https://image.url) a `code block`, some **bold** text and a [link](https://www.boot.dev)."
        expected_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with an image ", TextType.TEXT),
            TextNode("picture", TextType.IMAGE, "https://image.url"),
            TextNode(" a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(", some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(".", TextType.TEXT)
        ]
        self.assertEqual( text_to_textnodes(text), expected_result)
        
    