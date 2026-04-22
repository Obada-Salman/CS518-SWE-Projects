import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import resource_path


class ResourcePathCrossPlatformTests(unittest.TestCase):
    @patch("resource_path.os.makedirs")
    @patch("resource_path.platform.system", return_value="Linux")
    @patch.dict("resource_path.os.environ", {"XDG_DATA_HOME": "/tmp/xdg_data"}, clear=False)
    def test_linux_uses_xdg_data_home(self, _mock_system, mock_makedirs):
        path = resource_path.get_user_data_path("vegtable_wars")

        self.assertEqual(path, "/tmp/xdg_data/vegtable_wars")
        mock_makedirs.assert_called_once_with(path, exist_ok=True)

    @patch("resource_path.os.makedirs")
    @patch("resource_path.platform.system", return_value="Linux")
    @patch("resource_path.os.path.expanduser", return_value="/home/player")
    @patch.dict("resource_path.os.environ", {}, clear=True)
    def test_linux_fallback_path(self, _mock_expanduser, _mock_system, mock_makedirs):
        path = resource_path.get_user_data_path("vegtable_wars")

        self.assertEqual(path, "/home/player/.local/share/vegtable_wars")
        mock_makedirs.assert_called_once_with(path, exist_ok=True)

    @patch("resource_path.os.makedirs")
    @patch("resource_path.platform.system", return_value="Darwin")
    @patch("resource_path.os.path.expanduser", return_value="/Users/player")
    def test_macos_path(self, _mock_expanduser, _mock_system, mock_makedirs):
        path = resource_path.get_user_data_path("vegtable_wars")

        self.assertEqual(path, "/Users/player/Library/Application Support/vegtable_wars")
        mock_makedirs.assert_called_once_with(path, exist_ok=True)

    @patch("resource_path.os.makedirs")
    @patch("resource_path.platform.system", return_value="Windows")
    @patch.dict("resource_path.os.environ", {"LOCALAPPDATA": "C:/Users/player/AppData/Local"}, clear=False)
    def test_windows_prefers_localappdata(self, _mock_system, mock_makedirs):
        path = resource_path.get_user_data_path("vegtable_wars")

        self.assertEqual(path, "C:/Users/player/AppData/Local/vegtable_wars")
        mock_makedirs.assert_called_once_with(path, exist_ok=True)

    @patch("resource_path.os.makedirs")
    @patch("resource_path.platform.system", return_value="Windows")
    @patch("resource_path.os.path.expanduser", return_value="C:/Users/player")
    @patch.dict("resource_path.os.environ", {}, clear=True)
    def test_windows_fallback_path(self, _mock_expanduser, _mock_system, mock_makedirs):
        path = resource_path.get_user_data_path("vegtable_wars")

        self.assertEqual(path, "C:/Users/player/AppData/Local/vegtable_wars")
        mock_makedirs.assert_called_once_with(path, exist_ok=True)


if __name__ == "__main__":
    unittest.main()
