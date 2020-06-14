import unittest
from unittest.mock import patch
from requests.exceptions import Timeout
from .context import common


class WebsiteCheckerTestCase(unittest.TestCase):
    @patch('common.requests')
    def test_website_checker(self, mock_requests):
        url = "http://www.example.com"
        checker = common.WebsiteChecker(url)
        checker.get_status()
        mock_requests.get.assert_called_once()

    @patch('common.requests')
    def test_website_checker_timeout(self, mock_requests):
        mock_requests.get.side_effect = Timeout
        url = "http://www.example.com"
        checker = common.WebsiteChecker(url)
        result = checker.get_status()
        self.assertEqual(result.code, 0)

    @patch('common.requests')
    def test_website_checker_regex_ok(self, mock_requests):
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.text = 'test return'
        url = "http://www.example.com"
        checker = common.WebsiteChecker(url, regex='test')
        result = checker.get_status()
        self.assertEqual(result.content_ok, True)

    @patch('common.requests')
    def test_website_checker_regex_not_ok(self, mock_requests):
        mock_requests.get.return_value.status_code = 200
        mock_requests.get.return_value.text = 'nothing'
        url = "http://www.example.com"
        checker = common.WebsiteChecker(url, regex='test')
        result = checker.get_status()
        self.assertEqual(result.content_ok, False)


if __name__ == '__main__':
    unittest.main()
