# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Removed SDHandler dependency, we check for SD remount, just before entering
# the settings view
# from .sd_card import SDHandler

try:
    import ujson as json
except ImportError:
    import json

import os

# Settings storage
SETTINGS_FILENAME = "settings.json"
SD_PATH = "sd"
FLASH_PATH = "flash"

# Network settings
MAIN_TXT = "main"
TEST_TXT = "test"

# Policy types
NAME_SINGLE_SIG = "Single-sig"
NAME_MULTISIG = "Multisig"
NAME_MINISCRIPT = "Miniscript"

# Policy types names
POLICY_TYPE_NAMES = [
    NAME_SINGLE_SIG,
    NAME_MULTISIG,
    NAME_MINISCRIPT,
]

THIN_SPACE = " "


class SettingsNamespace:
    """Represents a settings namespace containing settings and child namespaces"""

    def label(self, attr):
        """Returns a label for UI when given a setting name or namespace"""
        raise NotImplementedError()

    def namespace_list(self):
        """Returns the list of child SettingsNamespace objects"""
        namespaces = [
            ns for ns in self.__dict__.values() if isinstance(ns, SettingsNamespace)
        ]
        namespaces.sort(key=lambda ns: str(ns.__class__.__name__))
        return namespaces

    def setting_list(self):
        """Returns the list of child Setting objects"""
        settings = [
            getattr(self.__class__, setting)
            for setting in dir(self.__class__)
            if isinstance(getattr(self.__class__, setting), Setting)
        ]
        settings.sort(key=lambda s: s.attr)
        return settings


class Setting:
    """Implements the descriptor protocol for reading and writing a single setting"""

    def __init__(self, attr, default_value):
        self.attr = attr
        self.default_value = default_value

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return store.get(obj.namespace, self.attr, self.default_value)

    def __set__(self, obj, value):
        if self.attr == "location":
            store.update_file_location(value)
        if value == self.default_value:
            store.delete(obj.namespace, self.attr)  # do not store defaults
        else:
            store.set(obj.namespace, self.attr, value)  # do store custom settings


class CategorySetting(Setting):
    """Setting that can be one of N categories"""

    def __init__(self, attr, default_value, categories):
        super().__init__(attr, default_value)
        self.categories = categories

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        stored_val = store.get(obj.namespace, self.attr, self.default_value)
        if stored_val not in self.categories:
            return self.default_value
        return stored_val


class NumberSetting(Setting):
    """Setting that can be a number within a defined range"""

    def __init__(self, numtype, attr, default_value, value_range):
        super().__init__(attr, default_value)
        self.numtype = numtype
        self.value_range = value_range

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        stored_val = store.get(obj.namespace, self.attr, self.default_value)
        if (
            (self.numtype is int and isinstance(stored_val, self.numtype))
            or (self.numtype is float and isinstance(stored_val, (self.numtype, int)))
        ) and self.value_range[0] <= stored_val <= self.value_range[1]:
            return stored_val

        return self.default_value


class Store:
    """Acts as a simple JSON file store for settings, falling back to an in-memory dict if no SD"""

    def __init__(self):
        self.settings = {}
        self.file_location = Store.get_vfs_location(SD_PATH)
        self.dirty = False

        # Check for the correct settings persist location
        # Try to load from SD
        self._load_settings()

        # Define location based on what was loaded or default undefined
        self.file_location = (
            self.settings.get("settings", {})
            .get("persist", {})
            .get("location", "undefined")
        )

        # Settings not found on SD, or 'persist.location' key not defined
        if SD_PATH not in self.file_location:
            # Try to load from flash
            self.file_location = Store.get_vfs_location(FLASH_PATH)
            self._load_settings()

        # Settings persist location will point to SD (if defined) else defaults to flash
        self.file_location = Store.get_vfs_location(
            self.settings.get("settings", {})
            .get("persist", {})
            .get("location", FLASH_PATH)
        )

    @classmethod
    def get_vfs_location(cls, location):
        """Returns the formatted vfs location for SD/flash"""
        return "/" + location + "/"

    def _load_settings(self):
        """Loads settings based on the current file_location (SD/flash)"""
        try:
            with open(self.file_location + SETTINGS_FILENAME, "r") as f:
                self.settings = json.loads(f.read())
        except:
            pass

    def get(self, namespace, setting_name, default_value):
        """Returns a setting value under the given namespace, or default value if not set"""
        s = json.loads(
            json.dumps(self.settings)
        )  # deepcopy to avoid building out namespaces
        for level in namespace.split("."):
            s[level] = s.get(level, {})
            s = s[level]
        if setting_name not in s:
            return default_value
        return s[setting_name]

    def set(self, namespace, setting_name, setting_value):
        """Stores a setting value under the given namespace if new/changed.
        Does NOT automatically save settings to flash or sd!
        """
        s = self.settings
        for level in namespace.split("."):
            s[level] = s.get(level, {})
            s = s[level]
        old_value = s.get(setting_name, None)
        if old_value != setting_value:
            s[setting_name] = setting_value
            self.dirty = True

    def delete(self, namespace, setting_name):
        """Deletes dict storage in self.settings for namespace.setting_name,
        also deletes storage for setting_name's parent namespace nodes, if empty.
        """
        s = self.settings
        levels = []
        for level in namespace.split("."):
            s[level] = s.get(level, {})
            levels.append([s, level])
            s = s[level]
        if setting_name in s:
            del s[setting_name]
            self.dirty = True
        for s, level in reversed(levels):
            if not s[level]:
                del s[level]
                self.dirty = True

    def update_file_location(self, location):
        """Delete any unused persistent settings when set location"""
        self.file_location = Store.get_vfs_location(location)
        try:
            if FLASH_PATH in self.file_location:
                os.remove(Store.get_vfs_location(SD_PATH) + SETTINGS_FILENAME)
            else:
                os.remove(Store.get_vfs_location(FLASH_PATH) + SETTINGS_FILENAME)
        except:
            pass

    def save_settings(self):
        """Helper to persist SETTINGS_FILENAME where user selected"""
        persisted = False

        if self.dirty:
            settings_filename = self.file_location + SETTINGS_FILENAME
            new_contents = json.dumps(self.settings)
            old_contents = "{}"
            try:
                with open(settings_filename, "r") as f:
                    old_contents = f.read()
            except:
                pass
            # Compare old and new file contents, if different, write new content
            if new_contents != old_contents:
                try:
                    with open(settings_filename, "w") as f:
                        f.write(new_contents)
                    persisted = True
                except:
                    pass
            self.dirty = False

        return persisted


# Initialize singleton
store = Store()
