import unittest
from parse_chinese.parse_ocr import get_attachment_url


class TestGetAttachmentURL(unittest.TestCase):

    def test_get_attachment_url(self):
        # A mock data dictionary for testing
        data = [
            {'attachment': '', 'other_key': 'some_value'},
            {'attachment': 'https://example.com',
             'other_key': 'another_value'},
            {'attachment': '', 'other_key': 'yet_another_value'}
        ]

        result = get_attachment_url(data)
        expected = 'https://example.com'
        self.assertEqual(result, expected)

        # Test with no attachment
        data_no_attachment = [
            {'other_key': 'some_value'},
            {'other_key': 'another_value'},
            {'other_key': 'yet_another_value'}
        ]
        result = get_attachment_url(data_no_attachment)
        expected = None
        self.assertEqual(result, expected)

        # Test with all attachments empty
        data_empty_attachment = [
            {'attachment': '', 'other_key': 'some_value'},
            {'attachment': '', 'other_key': 'another_value'},
            {'attachment': '', 'other_key': 'yet_another_value'}
        ]
        result = get_attachment_url(data_empty_attachment)
        expected = None
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
