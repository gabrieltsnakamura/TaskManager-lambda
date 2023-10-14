import unittest
from unittest.mock import patch, MagicMock

from src import task_manager_lambda

class TestApp(unittest.TestCase):
    @patch('src.task_manager_lambda.get_mysql_connection')
    def test_get_tasks(self, mock_get_mysql_connection):
        # Create a mock cursor and set its execute method to return the expected result
        mock_cursor = MagicMock()
        mocked_data = [("1", "1", "description1", False, "2023-01-01 00:00:00"), ("2", "1", "description1", True, "2023-01-01 00:00:00")]
        mock_cursor.fetchall.return_value = mocked_data

        # Create a mock connection and set its cursor method to return the mock cursor
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Set the mock get_mysql_connection method to return the mock connection
        mock_get_mysql_connection.return_value = mock_conn

        # Call the get_tasks function
        event = {"httpMethod": "GET", "path": "/user_tasks"}
        result = task_manager_lambda.get_tasks(event)

        # Verify that the mock pymysql methods were called with the expected arguments
        mock_get_mysql_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('SELECT * FROM user_tasks')
        mock_cursor.fetchall.assert_called_once()

        # Verify that the result is as expected
        body = [{
            'id': mocked_data[0][0],
            'user_id': mocked_data[0][1],
            'description': mocked_data[0][2],
            'status': mocked_data[0][3],
            'date': mocked_data[0][4]
        },
        {
            'id': mocked_data[1][0],
            'user_id': mocked_data[1][1],
            'description': mocked_data[1][2],
            'status': mocked_data[1][3],
            'date': mocked_data[1][4]
        }]
        expected_response = task_manager_lambda.build_response(200, body)
        self.assertEqual(result['statusCode'], expected_response['statusCode'])
        self.assertEqual(result['body'], expected_response['body'])

    @patch('src.task_manager_lambda.get_mysql_connection')
    def test_create_task(self, mock_get_mysql_connection):
        # Create a mock cursor and set its execute method to return the expected result
        mock_cursor = MagicMock()

        # Create a mock connection and set its cursor method to return the mock cursor
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Set the mock get_mysql_connection method to return the mock connection
        mock_get_mysql_connection.return_value = mock_conn

        # Call the create_task function
        event = {"httpMethod": "POST", "path": "/user_tasks", "body": "{\"description\": \"description1\", \"status\": false, \"date\": \"2023-01-01 00:00:00\"}", "pathParameters": {"user_id": "1"}}
        result = task_manager_lambda.create_task(event)

        # Verify that the mock pymysql methods were called with the expected arguments
        mock_get_mysql_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('INSERT INTO user_tasks (user_id, description, status, date) VALUES (%s, %s, %s, %s)', ("1", "description1", False, "2023-01-01 00:00:00"))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

        # Verify that the result is as expected
        expected_response = task_manager_lambda.build_response(200, "Task created successfully")
        self.assertEqual(result['statusCode'], expected_response['statusCode'])
        self.assertEqual(result['body'], expected_response['body'])

    @patch('src.task_manager_lambda.get_mysql_connection')
    def test_update_task(self, mock_get_mysql_connection):
        # Create a mock cursor and set its execute method to return the expected result
        mock_cursor = MagicMock()

        # Create a mock connection and set its cursor method to return the mock cursor
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Set the mock get_mysql_connection method to return the mock connection
        mock_get_mysql_connection.return_value = mock_conn

        # Call the update_task function
        event = {"httpMethod": "PUT", "path": "/user_tasks", "body": "{\"description\": \"description1\", \"status\": false, \"date\": \"2023-01-01 00:00:00\"}", "pathParameters": {"user_id": "1"}}
        result = task_manager_lambda.update_task(event)

        # Verify that the mock pymysql methods were called with the expected arguments
        mock_get_mysql_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('UPDATE user_tasks SET description = %s, status = %s, date = %s WHERE user_id = %s', ("description1", False, "2023-01-01 00:00:00", "1"))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

        # Verify that the result is as expected
        expected_response = task_manager_lambda.build_response(200, "Task updated successfully")
        self.assertEqual(result['statusCode'], expected_response['statusCode'])
        self.assertEqual(result['body'], expected_response['body'])

    @patch('src.task_manager_lambda.get_mysql_connection')
    def test_delete_task(self, mock_get_mysql_connection):
        # Create a mock cursor and set its execute method to return the expected result
        mock_cursor = MagicMock()

        # Create a mock connection and set its cursor method to return the mock cursor
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Set the mock get_mysql_connection method to return the mock connection
        mock_get_mysql_connection.return_value = mock_conn

        # Call the delete_task function
        event = {"httpMethod": "DELETE", "path": "/user_tasks", "pathParameters": {"user_id": "1"}}
        result = task_manager_lambda.delete_task(event)

        # Verify that the mock pymysql methods were called with the expected arguments
        mock_get_mysql_connection.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with('DELETE FROM user_tasks WHERE user_id = %s', ("1"))
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

        # Verify that the result is as expected
        expected_response = task_manager_lambda.build_response(200, "Task deleted successfully")
        self.assertEqual(result['statusCode'], expected_response['statusCode'])
        self.assertEqual(result['body'], expected_response['body'])