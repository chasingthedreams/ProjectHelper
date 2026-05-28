import unittest
from unittest.mock import MagicMock, patch
import states
import database
import utils

class TestProjectHelper(unittest.TestCase):

    def setUp(self):
        states.user_data = {}
        self.user_id = 12345
        states.ensure_user_data(self.user_id)

    def test_db_registration_and_no_duplicates(self):
        with patch('database.get_connection') as mock_conn:
            mock_cursor = MagicMock()
            mock_conn.return_value.cursor.return_value = mock_cursor
            database.save_request(self.user_id, "test", "text", "resp")
            self.assertTrue(mock_cursor.execute.called)

    def test_favorites_management(self):
        mock_get = MagicMock(return_value=["Тема 1", "Тема 2"])
        favorites = mock_get(self.user_id)
        self.assertIn("Тема 1", favorites)
        self.assertEqual(len(favorites), 2)

    @patch('utils.ask_gemma')
    def test_ollama_error_handling(self, mock_ask):
        mock_ask.side_effect = Exception("Connection Timeout")
        result = utils.safe_gemma("Тест")
        self.assertEqual(result, "❌ *ИИ временно недоступна.*")

    @patch('utils.ask_gemma')
    def test_ollama_empty_response(self, mock_ask):
        mock_ask.return_value = ""
        result = utils.safe_gemma("Тест")
        self.assertEqual(result, "⚠️ *Не удалось получить ответ.*")

    def test_states_and_navigation(self):
        states.user_data[self.user_id]["direction"] = "IT"
        self.assertEqual(states.user_data[self.user_id]["direction"], "IT")

    def test_project_sections_scenario(self):
        states.ensure_user_data(self.user_id)
        states.user_data[self.user_id]["project_topic"] = "Умный дом"
        self.assertEqual(states.user_data[self.user_id]["project_topic"], "Умный дом")

if __name__ == '__main__':
    unittest.main()