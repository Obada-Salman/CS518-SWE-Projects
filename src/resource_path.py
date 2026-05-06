import sys
import os
import platform

def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS)
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(relative_path):
    return os.path.join(get_base_path(), relative_path)


def _get_platform_data_root():
    system = platform.system()
    home = os.path.expanduser("~")

    if system == "Windows":
        # Preferred Windows writable app-data root.
        return os.environ.get("LOCALAPPDATA") or os.path.join(home, "AppData", "Local")

    if system == "Darwin":  # macOS
        return os.path.join(home, "Library", "Application Support")

    # Linux and WSL follow XDG with a common fallback.
    return os.environ.get("XDG_DATA_HOME") or os.path.join(home, ".local", "share")

def get_user_data_path(app_name="vegtable_wars"):
    path = os.path.join(_get_platform_data_root(), app_name)

    os.makedirs(path, exist_ok=True)
    return path

def get_community_level_path(app_name="vegtable_wars"):
    path = os.path.join(get_user_data_path(app_name), "levels", "community")

    os.makedirs(path, exist_ok=True)
    return path

def get_leaderboard_database(app_name="vegtable_wars"):
    if hasattr(sys, '_MEIPASS'):
        db_path =  os.path.join(get_user_data_path(app_name), "data", "leaderboard.db")
    else:
        db_path =  os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "leaderboard.db")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    return db_path