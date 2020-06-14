import unittest
from unittest.mock import patch
from .context import common


class DatabaseTestCase(unittest.TestCase):
    @patch('common.psycopg2')
    def test_database_insert(self, mock_db):
        db_uri = "mock_db"
        with common.Database(db_uri) as db:
            db.insert_event({'url': '', 'code': 0, 'response_time': 0, 'content_ok': False, 'timestamp': 0})
        mock_db.connect.assert_called_once()

    @patch('common.psycopg2')
    def test_database_invalid_input(self, mock_db):
        db_uri = "mock_db"
        with self.assertRaises(KeyError):
            with common.Database(db_uri) as db:
                db.insert_event(({'url': ''}))


if __name__ == '__main__':
    unittest.main()
