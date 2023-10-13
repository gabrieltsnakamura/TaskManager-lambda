import unittest
from unittest.mock import patch, MagicMock

from task_manager_lambda.app import get_tasks, create_task, update_task, delete_task, build_response

class TestApp(unittest.TestCase):
    @patch('app.get_mysql_connection')
    def test_get_tasks(self, mock_get_mysql_connection):
        # Create a mock cursor and set its execute method to return the expected result
        mock_cursor = MagicMock()
        expected_result = [("1", "1", "description1", False, "2023-01-01 00:00:00"), ("2", "1", "description1", True, "2023-01-01 00:00:00")]
        mock_cursor.fetchall.return_value = expected_result

        # Create a mock connection and set its cursor method to return the mock cursor
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Set the mock get_mysql_connection method to return the mock connection
        mock_get_mysql_connection.return_value = mock_conn

        # Call the get_tasks function
        event = {"httpMethod": "GET", "path": "/user_tasks"}
        result = get_tasks(event)

        # Verify that the mock pymysql methods were called with the expected arguments
        mock_get_mysql_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM user_tasks')
        mock_cursor.fetchall.assert_called_once()

        # Verify that the result is as expected
        expected_response = build_response(200, expected_result)
        self.assertEqual(result, expected_response)