import json


class SaveManager:
    profiles = {}

    @staticmethod
    def add_profile(name, init_dict=None):
        SaveManager.profiles[name] = {} if init_dict is None else init_dict
        return SaveManager.profiles[name]

    @staticmethod
    def get_profile(name):
        return SaveManager.profiles[name]

    @staticmethod
    def remove_profile(name):
        del SaveManager.profiles[name]

    @staticmethod
    def save_profile(name, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(SaveManager.profiles.get(name), f, indent=4)

    @staticmethod
    def load_profile(name, path):
        with open(path, encoding='utf-8') as f:
            SaveManager.profiles[name] = json.load(f)
        return SaveManager.profiles[name]

    @staticmethod
    def set_entry(profile_name, entry_name, value):
        SaveManager.profiles[profile_name][entry_name] = value
        return value

    @staticmethod
    def get_entry(profile_name, entry_name):
        return SaveManager.profiles[profile_name][entry_name]

    @staticmethod
    def remove_entry(profile_name, entry_name):
        del SaveManager.profiles[profile_name][entry_name]
