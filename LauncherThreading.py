import time

from PySide6 import QtCore
from PySide6.QtCore import Signal

from networking.mb_query import MBQuery
from networking.ms_query import get_server_list, ms_url, ms_kart_url

class QueryMessageBoard(QtCore.QThread):
    mod_description_sig1 = Signal(str)
    mod_list_sig1 = Signal(dict)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.mb_query = MBQuery()
        self.mod = None
        self.get_mod_description = False
        self.get_mods = False
        self.mods_type = None

    def on_request_mod_list(self, mods_type):
        self.get_mods = True
        self.mods_type = mods_type

    def on_request_mod_desc(self, mod):
        self.get_mod_description = True
        self.mod = mod

    def run(self):
        self.running = True
        while self.running:
            if self.get_mods:
                self.mods_list = {}
                subforum_url = None
                if self.mods_type == "Maps":
                    subforum_url = self.mb_query.maps_sublink
                if self.mods_type == "Characters":
                    subforum_url = self.mb_query.characters_sublink
                if self.mods_type == "Lua":
                    subforum_url = self.mb_query.lua_sublink
                if self.mods_type == "Assets":
                    subforum_url = self.mb_query.assets_sublink
                if self.mods_type == "Misc":
                    subforum_url = self.mb_query.misc_sublink
                mods = self.mb_query.get_mods(subforum_url)
                for mod in mods:
                    entry_text = mod.name
                    self.mods_list[entry_text] = mod

                self.mod_list_sig1.emit(self.mods_list)

                # Reset variables
                self.mods_list = {}
                self.get_mods = False
                self.mods_type = None

            if self.get_mod_description:
                if self.mod:
                    description = self.mb_query.get_mod_description(self.mod)
                    self.mod_description_sig1.emit(description)

                # Reset variables
                self.mod = None
                self.get_mod_description = False

            time.sleep(1)
            
            
class QueryMasterServer(QtCore.QThread):
    server_list_sig1 = Signal(list)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.query_ms = False
        self.running = True
    
    def on_refresh(self):
        """Refresh button clicked
        """
        self.query_ms = True
        
    def on_quit(self):
        self.running = False
        
    def run(self):
        while self.running:
            if self.query_ms:
                server_list = get_server_list(ms_url)
                self.server_list_sig1.emit(server_list)
                self.query_ms = False                    
            time.sleep(1)
