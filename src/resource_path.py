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

def get_user_data_path(app_name="vegtable_wars"):
    home = os.path.expanduser("~")

    if platform.system() == "Windows":
        home = os.path.join(home, "Appdata/local/")
    
    elif platform.system() == "Linux":
        home = os.path.join(home, ".local/share")
    
    elif platform.system() == "Darwin": # Mac
        home = os.path.join(home, "Library/Application Support/")

    path = os.path.join(home, app_name)

    os.makedirs(path, exist_ok=True)
    return path

def get_community_level_path(app_name="vegtable_wars"):
    path = os.path.join(get_user_data_path(app_name), "levels", "community")

    os.makedirs(path, exist_ok=True)
    return path

def get_leaderboard_database(app_name="vegtable_wars"):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(get_user_data_path(app_name), "data", "leaderboard.db")
    else:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "leaderboard.db")