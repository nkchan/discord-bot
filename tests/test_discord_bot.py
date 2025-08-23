# tests/test_discord_bot.py
import sys
import unittest
from unittest.mock import patch, MagicMock
import importlib

# Mocks for libraries that discord_bot.py imports
# These will be applied only during the tests in this file
MODULE_MOCKS = {
    'discord': MagicMock(),
    'discord.app_commands': MagicMock(),
    'dotenv': MagicMock(),
    'g_sheets': MagicMock(),
}

class TestDevMode(unittest.TestCase):

    @patch.dict(sys.modules, MODULE_MOCKS)
    def test_prefix_in_dev_mode(self):
        """Tests if the command_prefix is 'dev-' when 'dev' is in sys.argv."""
        with patch.object(sys, 'argv', ['discord_bot.py', 'dev']):
            import discord_bot
            importlib.reload(discord_bot)
            self.assertEqual(discord_bot.command_prefix, "dev-")

    @patch.dict(sys.modules, MODULE_MOCKS)
    def test_prefix_not_in_dev_mode(self):
        """Tests if the command_prefix is empty when 'dev' is not in sys.argv."""
        with patch.object(sys, 'argv', ['discord_bot.py']):
            import discord_bot
            importlib.reload(discord_bot)
            self.assertEqual(discord_bot.command_prefix, "")

if __name__ == '__main__':
    unittest.main()