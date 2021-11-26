import json
import os
import sys
import urllib
import urllib.parse
from datetime import date

import feedparser
from PySide6 import QtGui, QtCore, QtWidgets
from PySide6.QtWidgets import QFileDialog, QMenu, QMessageBox

import EditServerMain
import characterText
import srb2query
from LauncherUI import *
from qss import themes

fool = date.today() == date(date.today().year, 4, 1)

versionString = "reBoot-2.0"


class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.configData = self.read_config()

        self.apply_style()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.app = app
        self.setWindowTitle("Launcherblast2 reBoot-2.0")

        # server ips stored internally so u don't dox people's ips if you're streaming or smth
        self.saved_server_ips = []

        # Dict associating QListWidget items with server data:
        self.master_server_list = {}
        self.load_ms_list()

        # load servers from file ===================================================== #
        # self.loadServerList()
        self.has_loaded_servers = False

        # launcher config settings =========================#
        self.launcherConfigFile = "LauncherBlast2Conf.json"

        # allow posix systems to use wine ============================================ #
        if os.name == "posix":
            self.ui.WineToggle.setEnabled(True)

        # file dialog options to keep shit consistent ================================ #
        self.FileDialogOptions = QFileDialog.Options()
        # self.FileDialogOptions |= QFileDialog.DontUseNativeDialog

        # set tab to game tab initially ============================================== #
        self.ui.MainTabsStackedWidget.setCurrentIndex(1)
        self.ui.GameContentStackedWidget.setCurrentIndex(0)

        # fix resolution of skin image =============================================== #
        self.ui.PlayerSkinImage.setPixmap(QtGui.QPixmap(":/assets/img/sonic.png")
                                          .scaled(135,
                                                  190,
                                                  QtCore.Qt.KeepAspectRatio,
                                                  QtCore.Qt.FastTransformation))

        # changed skin index ========================================================= #
        self.ui.PlayerSkinInput.currentIndexChanged.connect(self.change_skin_image)

        # clear files list =========================================================== #
        self.ui.GameFilesList.clear()

        # clear servers list ========================================================= #
        self.ui.ServerList.clear()

        # dock "tabs" ================================================================ #
        self.ui.NewsTabButton.clicked.connect(lambda: self.change_main_tab(0))
        self.ui.GameTabButton.clicked.connect(lambda: self.change_main_tab(1))
        self.ui.HelpTabButton.clicked.connect(lambda: self.change_main_tab(2))
        self.ui.SettingsTabButton.clicked.connect(lambda: self.change_main_tab(3))

        # game "tabs" ================================================================ #
        self.ui.ProfileTabButton.clicked.connect(lambda: self.changeGameTab(0))
        self.ui.FilesTabButton.clicked.connect(lambda: self.changeGameTab(1))
        self.ui.GameSettingsTabButton.clicked.connect(lambda: self.changeGameTab(2))
        self.ui.PlayerSetupTabButton.clicked.connect(lambda: self.changeGameTab(3))
        self.ui.HostGameTabButton.clicked.connect(lambda: self.changeGameTab(4))
        self.ui.JoinGameTabButton.clicked.connect(lambda: self.changeGameTab(5))

        # files list buttons ========================================================= #
        self.ui.GameFilesClearButton.clicked.connect(self.clear_files_list)
        self.ui.GameFilesDeleteButton.clicked.connect(self.delete_selected_files)
        self.ui.GameFilesUpButton.clicked.connect(self.move_selected_files_up)
        self.ui.GameFilesDownButton.clicked.connect(self.move_selected_files_down)
        self.ui.GameFilesAddButton.clicked.connect(self.add_files)
        self.ui.GameFilesSaveButton.clicked.connect(self.save_file_list)
        self.ui.GameFilesLoadButton.clicked.connect(self.load_file_list)
        self.ui.GameFilesExecScrBrowseButton.clicked.connect(self.set_exec_file_path)

        # server list buttons ======================================================== #
        self.ui.AddServerButton.clicked.connect(self.show_add_server_dialog)
        self.ui.JoinServerButton.clicked.connect(self.join_selected_server)
        self.ui.DeleteServerButton.clicked.connect(self.delete_selected_server)
        self.ui.EditServerButton.clicked.connect(self.open_server_editor)
        self.ui.JoinAddressButton.clicked.connect(self.join_from_ip)
        self.ui.RefreshButton.clicked.connect(self.load_ms_list)
        self.ui.JoinMasterServerButton.clicked.connect(self.join_ms_selection)
        self.ui.SaveMSButton.clicked.connect(self.save_ms_selection)

        # play button ================================================================ #
        self.ui.GamePlayButton.clicked.connect(self.launch_game_normally)
        # self.ui.GameOptionsDropDownButton.clicked.connect()
        self.gameOptionsDropDownMenu = QMenu()
        self.gameOptionsDropDownMenu.addAction("Save current parameters to script", self.export_script)
        self.ui.GameOptionsDropDownButton.setMenu(self.gameOptionsDropDownMenu)
        self.ui.GameOptionsDropDownButton.clicked.connect(self.show_game_options_dropdown)

        # load news feed from srb2.org =============================================== #
        self.load_news()

        # and then add the spacer at the bottom
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ui.verticalLayout_20.addItem(spacerItem)

    def show_game_options_dropdown(self):
        menu = QMenu()
        menu.addAction("Save current parameters to script", self.export_script)
        menu.exec()

    def load_news(self):
        # ok lets uh, get the news feed or something?
        srb2_rss_url = "https://www.srb2.org/feed/"

        feed = feedparser.parse(srb2_rss_url)
        items = feed["items"]

        for item in items:
            # title
            article_title_label = QtWidgets.QLabel(self.ui.NewsScrollAreaContent)
            article_title_label.setStyleSheet("font-size: 14pt;")
            url_link = "<a href=\"" + item["link"] + "\" style=\"color: #ddd;\">" + item["title"] + "</a>"
            article_title_label.setText(QtCore.QCoreApplication.translate("MainWindow", url_link))
            article_title_label.setOpenExternalLinks(True)
            self.ui.verticalLayout_20.addWidget(article_title_label)

            # author name and date
            author_name_label = QtWidgets.QLabel(self.ui.NewsScrollAreaContent)
            author_name_label.setStyleSheet("font-weight: 400;")
            author_name_label.setText(item["author"] + " - " + item["published"].replace(" +0000", ""))
            self.ui.verticalLayout_20.addWidget(author_name_label)

            # snippet
            info_label = QtWidgets.QLabel(self.ui.NewsScrollAreaContent)
            info_label.setStyleSheet("font-weight: 400;")
            info_label.setText("<div style=\"text-wrap: wrap-word;\">" + item["summary"] + "</div>")
            info_label.setWordWrap(True)
            info_label.adjustSize()
            info_label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            self.ui.verticalLayout_20.addWidget(info_label)

    # add server window ============================================================== #
    # ================================================================================ #
    def show_add_server_dialog(self):
        self.childWindow = EditServerMain.ChildWindow(self, "", "", True)
        self.childWindow.show()
        return

    # change character image for skin thing ========================================== #
    # ================================================================================ #
    def change_skin_image(self):
        asset_img = ":/assets/img/sonic.png"
        self.ui.PlayerSkinInfoText.setText(characterText.sonic)
        if self.ui.PlayerSkinInput.currentIndex() == 2:
            asset_img = ":/assets/img/tails.png"
            self.ui.PlayerSkinInfoText.setText(characterText.tails)
        if self.ui.PlayerSkinInput.currentIndex() == 3:
            asset_img = ":/assets/img/knuckles.png"
            self.ui.PlayerSkinInfoText.setText(characterText.knux)
        if self.ui.PlayerSkinInput.currentIndex() == 4:
            asset_img = ":/assets/img/rosy.png"
            self.ui.PlayerSkinInfoText.setText(characterText.amy)
        if self.ui.PlayerSkinInput.currentIndex() == 5:
            asset_img = ":/assets/img/fang.png"
            self.ui.PlayerSkinInfoText.setText(characterText.fang)
        if self.ui.PlayerSkinInput.currentIndex() == 6:
            asset_img = ":/assets/img/metal.png"
            self.ui.PlayerSkinInfoText.setText(characterText.metal)

        self.ui.PlayerSkinImage.setPixmap(QtGui.QPixmap(asset_img).scaled(135,
                                                                         190,
                                                                         QtCore.Qt.KeepAspectRatio,
                                                                         QtCore.Qt.FastTransformation))
        return

    # create srb2 launch command ===================================================== #
    # ================================================================================ #
    # this converts all of the launcher inputs to a single-string command to launch    #
    # srb2.                                                                            #
    def get_launch_command(self):
        ui = self.ui
        com = ""
        if self.ui.WineToggle.isChecked() and self.ui.WineToggle.isEnabled(): com += "wine "
        com += "\"" + ui.GameExecFilePathInput.text() + "\""

        # game settings (from game settings tab) ===================================== #
        if ui.GameRendererSetting.currentIndex() == 0: com += " +renderer 1"
        if ui.GameRendererSetting.currentIndex() == 1: com += " +renderer 2"
        if ui.GameFullscreenSetting.currentIndex() == 0: com += " +fullscreen 1"
        if ui.GameFullscreenSetting.currentIndex() == 1: com += " -borderless"
        if ui.GameFullscreenSetting.currentIndex() == 2: com += " -win"
        if ui.GameMusicSetting.currentIndex() == 0: com += " +digimusic On"
        if ui.GameMusicSetting.currentIndex() == 1: com += " +digimusic Off"
        if ui.GameMusicSetting.currentIndex() == 2: com += " -usecd"
        if ui.GameMusicSetting.currentIndex() == 3: com += " -nomusic"
        if ui.GameSoundSetting.currentIndex() == 1: com += " -nosound"
        if ui.GameHorizontalResolutionInput.text() != "" and ui.GameVerticalResolutionInput.text() != "":
            com += " -width " + ui.GameHorizontalResolutionInput.text() + " -height " + ui.GameVerticalResolutionInput.text()
        if ui.PlayerNameInput.text() != "": com += " +name \"" + ui.PlayerNameInput.text() + "\""
        if ui.PlayerColorInput.currentIndex() != 0: com += " +color " + str(ui.PlayerColorInput.currentText().lower())
        if ui.PlayerSkinInput.currentIndex() != 0: com += " +skin " + str(
            ui.PlayerSkinInput.currentText().lower().replace(" ", ""))

        # get all files ============================================================== #
        com += " -file"
        for i in range(ui.GameFilesList.count()):
            com += " \"" + ui.GameFilesList.item(i).text() + "\""

        # add a script =============================================================== #
        if ui.GameFilesExecScriptInput.text() != "": com += " +exec " + ui.GameFilesExecScriptInput.text()

        # custom parameters ========================================================== #
        if ui.GameArgsInput.text() != "": com += " " + ui.GameArgsInput.text()

        return com

    # clear files list =============================================================== #
    # ================================================================================ #
    def clear_files_list(self):
        self.ui.GameFilesList.clear()
        return

    # delete current file ============================================================ #
    # ================================================================================ #
    def delete_selected_files(self):
        for item in self.ui.GameFilesList.selectedItems():
            self.ui.GameFilesList.takeItem(self.ui.GameFilesList.row(item))
        return

    # move files up ================================================================== #
    # ================================================================================ #
    def move_selected_files_up(self):
        for item in self.ui.GameFilesList.selectedItems():
            row = self.ui.GameFilesList.row(item)
            if row == 0: return
            c_item = self.ui.GameFilesList.takeItem(row)
            self.ui.GameFilesList.insertItem(row - 1, c_item)
            c_item.setSelected(True)
        return

    # move files down ================================================================ #
    # ================================================================================ #
    def move_selected_files_down(self):
        reservedItems = []
        row = 0
        for item in self.ui.GameFilesList.selectedItems():
            row = self.ui.GameFilesList.row(item)
            cItem = self.ui.GameFilesList.takeItem(row)
            reservedItems.append(cItem)
        for item in reservedItems:
            row += 1
            self.ui.GameFilesList.insertItem(row, item)
            item.setSelected(True)
        return

    # add files to the file list ===================================================== #
    # ================================================================================ #
    def add_file(self, f):
        new_item = QtWidgets.QListWidgetItem()
        new_item.setText(os.path.basename(str(f)))
        new_item_icon = QtGui.QIcon()
        filetype = str(f).split(".")[-1]
        new_item_icon.addPixmap(QtGui.QPixmap(":/assets/img/filetypes/" + filetype + ".png"), QtGui.QIcon.Normal,
                              QtGui.QIcon.Off)
        new_item.setIcon(new_item_icon)
        self.ui.GameFilesList.addItem(new_item)
        return

    # add files button =============================================================== #
    # ================================================================================ #
    def add_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Open files to add to SRB2", "",
                                                "All compatible SRB2 files (*.pk3 *.wad *.lua *.soc);;PK3 Files (*.pk3);;WAD Files (*.wad);;Lua Files (*.lua);;SOC files (*.soc)",
                                                options=self.FileDialogOptions)
        if files:
            # add each file to the file list with icon =============================== #
            for f in files:
                self.add_file(f)
        return

    def save_file_list(self):
        # convert to json compatible list ============================================ #
        items = []
        for i in range(self.ui.GameFilesList.count()):
            items.append(self.ui.GameFilesList.item(i).text())

        # open a file dialog ========================================================= #
        f, _ = QFileDialog.getSaveFileName(self, "Save file list", "", "JSON files (*.json)",
                                           options=self.FileDialogOptions)
        if f:
            with open(f, 'w') as outfile:
                json.dump(items, outfile)
        return

    def load_file_list(self):
        # open file ================================================================== #
        f, _ = QFileDialog.getOpenFileName(self, "Open file list", "", "JSON files (*.json)",
                                           options=self.FileDialogOptions)
        if f:
            with open(f, 'r') as jsonFile:
                items = json.load(jsonFile)
                for item in items:
                    self.add_file(item)
        return

    def set_exec_file_path(self):
        f, _ = QFileDialog.getOpenFileName(self, "Open script to execute on launch", "",
                                           "All compatible files (*.txt *.cfg);;All files (*)",
                                           options=self.FileDialogOptions)
        if (f):
            self.ui.GameFilesExecScriptInput.setText(f)

    # play button ==================================================================== #
    # ================================================================================ #
    def launch_game_normally(self):
        launchCommand = self.get_launch_command()
        os.system(launchCommand)
        return

    # change tab function ============================================================ #
    # ================================================================================ #
    def change_main_tab(self, index):
        self.ui.MainTabsStackedWidget.setCurrentIndex(index)
        return

    # change game tab function ======================================================= #
    # ================================================================================ #
    def changeGameTab(self, index):
        self.ui.GameContentStackedWidget.setCurrentIndex(index)
        return

    def load_ms_list(self):
        ms_data = srb2query.get_server_list(srb2query.ms_url)
        del self.master_server_list
        self.master_server_list = {}
        for server in ms_data:
            entry_label = '{} | Room: {} | Version: {}'.format(
                server.get("name"),
                server.get("room"),
                server.get("version"))
            new_item = QtWidgets.QListWidgetItem()
            new_item.setText(entry_label)
            self.ui.MasterServerList.addItem(new_item)
            self.master_server_list[entry_label] = server
        return

    def join_ms_selection(self):
        selection = self.ui.MasterServerList.currentItem().text()
        ip_string = self.master_server_list[selection].get("ip")
        os.system(self.get_launch_command() + " -connect " + ip_string)
        return

    def save_ms_selection(self):
        selection = self.ui.MasterServerList.currentItem().text()
        server = self.master_server_list[selection]
        ip = server.get("ip")
        name = server.get("name")
        self.add_server_to_list(name, ip)

    # save servers list to file ====================================================== #
    # ================================================================================ #
    def save_server_list(self):
        serv_list = []
        for i in range(len(self.saved_server_ips)):
            data = {"name": self.ui.ServerList.item(i).text(), "ip": self.saved_server_ips[i]}
            serv_list.append(data)
        with open("lb2ServerList.json", "w") as f:
            json.dump(serv_list, f)
        return

    # load server list =============================================================== #
    # ================================================================================ #
    def load_server_list(self):
        serv_list = []
        fpath = os.path.join(os.getcwd(), "lb2ServerList.json")
        if not os.path.isfile(fpath):
            return
        with open(fpath, "r") as f:
            serv_list = json.load(f)

        for server in serv_list:
            self.add_server_to_list(server["name"], server["ip"])
        return

    # add server to server list ====================================================== #
    # ================================================================================ #
    def add_server_to_list(self, name, ip):
        new_item = QtWidgets.QListWidgetItem()
        new_item.setText(name)
        self.saved_server_ips.append(ip)
        self.ui.ServerList.addItem(new_item)
        self.save_server_list()
        return

    # open server editor ============================================================= #
    # ================================================================================ #
    def open_server_editor(self):
        ip = self.saved_server_ips[self.ui.ServerList.selectedIndexes()[0].row()]
        name = self.ui.ServerList.selectedItems()[0].text()
        self.childWindow = EditServerMain.ChildWindow(self, name, ip, False)
        self.childWindow.show()
        return

    # edit server in list ============================================================ #
    # ================================================================================ #
    def edit_selected_server(self, name, ip):
        self.saved_server_ips[self.ui.ServerList.selectedIndexes()[0].row()] = ip
        self.ui.ServerList.selectedItems()[0].setText(name)
        self.save_server_list()
        return

    # delete server in list ========================================================== #
    # ================================================================================ #
    def delete_server_from_list(self, index):
        self.saved_server_ips.pop(index)
        self.ui.ServerList.takeItem(index)
        self.save_server_list()
        return

    # delete selected server ========================================================= #
    # ================================================================================ #
    def delete_selected_server(self):
        self.delete_server_from_list(self.ui.ServerList.selectedIndexes()[0].row())
        return

    # join current selected server in list =========================================== #
    # ================================================================================ #
    def join_selected_server(self):
        ipString = self.saved_server_ips[self.ui.ServerList.selectedIndexes()[0].row()]
        os.system(self.get_launch_command() + " -connect " + ipString)
        return

    # join direct address ============================================================ #
    # ================================================================================ #
    def join_from_ip(self):
        ipString = self.ui.JoinAddressInput.text
        os.system(self.get_launch_command() + " -connect " + ipString)
        return

    # join current selected server in list =========================================== #
    # ================================================================================ #
    def start_server(self):
        launch_command = self.ui.GameExecFilePathInput.text() + " -server"
        if not self.ui.DedicatedServerToggle.isChecked:
            launch_command = self.get_launch_command()

        if self.ui.ServerNameInput.text() != "": launch_command += " +servername " + self.ui.ServerNameInput.text()
        if self.ui.AdminPasswordInput.text() != "": launch_command += " +password " + self.ui.AdminPasswordInput.text()
        if self.ui.RoomInput.currentIndex() != 0:
            launch_command += " -id "
            if self.ui.RoomInput.currentIndex() == 1: launch_command += "33"
            if self.ui.RoomInput.currentIndex() == 2: launch_command += "28"
            if self.ui.RoomInput.currentIndex() == 3: launch_command += "38"
            if self.ui.RoomInput.currentIndex() == 4: launch_command += "31"
        launch_command += " -gametype " + str(self.ui.GametypeInput.currentIndex())
        launch_command += " +advancemap " + str(self.ui.AdvanceMapInput.currentIndex())
        if "" != self.ui.PointLimitInput.text():
            launch_command += " +pointlimit " + self.ui.PointLimitInput.text()
        else:
            launch_command += " +pointlimit 1000"
        if self.ui.TimeLimitInput.text() != "":
            launch_command += " +timelimit " + self.ui.TimeLimitInput.text()
        else:
            launch_command += " +timelimit 0"
        if self.ui.MaxPlayersInput.text() != "":
            launch_command += " +maxplayers " + self.ui.MaxPlayersInput.text()
        else:
            launch_command += " +maxplayers 8"
        if (
                self.ui.ForceSkinInput.currentText() != ""): launch_command += " +forceskin " + self.ui.ForceSkinInput.currentText().lower().replace(
            " ", "")
        if self.ui.PortInput.text() != "":
            launch_command += " -port " + self.ui.PortInput.text()
        else:
            launch_command += " -port 5029"
        if self.ui.DisableWeaponsToggle.isChecked():
            launch_command += " +specialrings 1"
        else:
            launch_command += " +specialrings 0"
        if self.ui.SuddenDeathToggle.isChecked():
            launch_command += " +suddendeath 1"
        else:
            launch_command += " +suddendeath 0"
        if self.ui.DedicatedServerToggle.isChecked(): launch_command += " -dedicated"
        if self.ui.UploadToggle.isChecked():
            launch_command += " +downloading 1"
        else:
            launch_command += " +downloading 0"

        os.system(launch_command)
        return

    # when closed save stuff ========================================================= #
    # ================================================================================ #
    def closeEvent(self, e):
        self.save_config()
        return

    # wait for window the fully start ================================================ #
    # ================================================================================ #
    def applicationStarted(self):
        # fix resolution of the image on the play tab ================================ #
        self.load_server_list()
        self.load_config()
        self.check_version()

        # april fools day stuff
        if (fool):
            self.ui.PlayerSkinInput.setCurrentIndex(4)
            self.ui.PlayerColorInput.setCurrentIndex(57)
            self.ui.PlayerColorInput.setEnabled(False)
            self.ui.PlayerSkinInput.setEnabled(False)

        return

    # save launcher config =========================================================== #
    # ================================================================================ #
    def save_config(self):
        # generate the json data for the config
        confJson = {"files": [], "player": {}, "game": {"resolution": {}}, "host": {}, "settings": {}}
        confJson["player"]["name"] = self.ui.PlayerNameInput.text()
        confJson["player"]["skin"] = str(self.ui.PlayerSkinInput.currentText())
        confJson["player"]["color"] = self.ui.PlayerColorInput.currentIndex()
        confJson["game"]["resolution"]["width"] = self.ui.GameHorizontalResolutionInput.text()
        confJson["game"]["resolution"]["height"] = self.ui.GameVerticalResolutionInput.text()
        confJson["game"]["renderer"] = self.ui.GameRendererSetting.currentIndex()
        confJson["game"]["windowmode"] = self.ui.GameFullscreenSetting.currentIndex()
        confJson["game"]["music"] = self.ui.GameMusicSetting.currentIndex()
        confJson["game"]["sound"] = self.ui.GameSoundSetting.currentIndex()
        confJson["game"]["exepath"] = self.ui.GameExecFilePathInput.text()
        confJson["game"]["cliargs"] = self.ui.GameArgsInput.text()
        confJson["host"]["hostname"] = self.ui.ServerNameInput.text()
        confJson["host"]["password"] = self.ui.AdminPasswordInput.text()
        confJson["host"]["room"] = self.ui.RoomInput.currentIndex()
        confJson["host"]["gametype"] = self.ui.GametypeInput.currentIndex()
        confJson["host"]["advancemap"] = self.ui.AdvanceMapInput.currentIndex()
        confJson["host"]["pointlimit"] = self.ui.PointLimitInput.text()
        confJson["host"]["timelimit"] = self.ui.TimeLimitInput.text()
        confJson["host"]["maxplayers"] = self.ui.MaxPlayersInput.text()
        confJson["host"]["forceskin"] = str(self.ui.ForceSkinInput.currentText())
        confJson["host"]["disableweaponrings"] = self.ui.DisableWeaponsToggle.isChecked()
        confJson["host"]["suddendeath"] = self.ui.SuddenDeathToggle.isChecked()
        confJson["host"]["dedicated"] = self.ui.DedicatedServerToggle.isChecked()
        confJson["settings"]["wine"] = self.ui.WineToggle.isChecked()
        confJson["settings"]["theme"] = self.ui.LauncherThemeInput.currentIndex()
        confJson["settings"]["includefiles"] = self.ui.SaveFilesToConfigToggle.isChecked()

        for i in range(self.ui.GameFilesList.count()):
            confJson["files"].append(self.ui.GameFilesList.item(i).text())

        with open("LauncherBlast2Conf.json", "w") as f:
            json.dump(confJson, f)

        print("saved config")
        return

    # read launcher config json file ================================================= #
    # ================================================================================ #
    def read_config(self):
        config_data = {}
        fpath = os.path.join(os.getcwd(), "LauncherBlast2Conf.json")
        # print(fpath)
        if not os.path.isfile(fpath):
            return 0
        with open(fpath, "r") as f:
            config_data = json.load(f)

        return config_data

    # load launcher config =========================================================== #
    # ================================================================================ #
    def load_config(self):

        if self.configData == 0:
            return

        # now set all elements to their saved values
        self.ui.PlayerNameInput.setText(self.configData["player"]["name"])
        self.ui.PlayerSkinInput.setCurrentText(self.configData["player"]["skin"])
        self.ui.PlayerColorInput.setCurrentIndex(self.configData["player"]["color"])
        self.ui.GameHorizontalResolutionInput.setText(self.configData["game"]["resolution"]["width"])
        self.ui.GameVerticalResolutionInput.setText(self.configData["game"]["resolution"]["height"])
        self.ui.GameRendererSetting.setCurrentIndex(self.configData["game"]["renderer"])
        self.ui.GameFullscreenSetting.setCurrentIndex(self.configData["game"]["windowmode"])
        self.ui.GameMusicSetting.setCurrentIndex(self.configData["game"]["music"])
        self.ui.GameSoundSetting.setCurrentIndex(self.configData["game"]["sound"])
        self.ui.GameExecFilePathInput.setText(self.configData["game"]["exepath"])
        self.ui.GameArgsInput.setText(self.configData["game"]["cliargs"])
        self.ui.ServerNameInput.setText(self.configData["host"]["hostname"])
        self.ui.AdminPasswordInput.setText(self.configData["host"]["password"])
        self.ui.RoomInput.setCurrentIndex(self.configData["host"]["room"])
        self.ui.GametypeInput.setCurrentIndex(self.configData["host"]["gametype"])
        self.ui.AdvanceMapInput.setCurrentIndex(self.configData["host"]["advancemap"])
        self.ui.PointLimitInput.setText(self.configData["host"]["pointlimit"])
        self.ui.TimeLimitInput.setText(self.configData["host"]["timelimit"])
        self.ui.MaxPlayersInput.setText(self.configData["host"]["maxplayers"])
        self.ui.ForceSkinInput.setCurrentText(self.configData["host"]["forceskin"])
        self.ui.DisableWeaponsToggle.setChecked(self.configData["host"]["disableweaponrings"])
        self.ui.SuddenDeathToggle.setChecked(self.configData["host"]["suddendeath"])
        self.ui.DedicatedServerToggle.setChecked(self.configData["host"]["dedicated"])
        self.ui.WineToggle.setChecked(self.configData["settings"]["wine"])
        self.ui.LauncherThemeInput.setCurrentIndex(self.configData["settings"]["theme"])
        self.ui.SaveFilesToConfigToggle.setChecked(self.configData["settings"]["includefiles"])

        if self.ui.SaveFilesToConfigToggle.isChecked:
            for f in self.configData["files"]:
                self.add_file(f)

        self.change_skin_image()
        return

    # apply launchder style ========================================================== #
    # ================================================================================ #
    def apply_style(self):
        # set up the launcher theme
        if (self.configData == 0):
            self.setStyleSheet(themes.main + themes.dark)
            return

        if self.configData["settings"]["theme"] == 0: chosentheme = themes.dark
        if self.configData["settings"]["theme"] == 1: chosentheme = themes.light
        if self.configData["settings"]["theme"] == 2: chosentheme = themes.blue
        if self.configData["settings"]["theme"] == 3: chosentheme = themes.orange
        if self.configData["settings"]["theme"] == 4: chosentheme = themes.red
        if self.configData["settings"]["theme"] == 5: chosentheme = themes.pink
        if self.configData["settings"]["theme"] == 6: chosentheme = themes.lightsout

        # april fools day stuff. pls dont spoil for others!11!1
        if (fool):
            chosentheme = themes.pink

        self.setStyleSheet(themes.main + chosentheme)
        return

    # apply launchder style ========================================================== #
    # ================================================================================ #
    def export_script(self):
        file_filter = "Batch files (*.bat);;Shell scripts (*.sh)"
        if (os.name == "posix"):
            file_filter = "Shell scripts (*.sh);;Batch files (*.bat)"
        file_filter += ";;All files (*)"
        fileName, _ = QFileDialog.getSaveFileName(self, "Save script", os.getcwd(), file_filter)
        if fileName:
            out_text = ""
            if fileName.endswith(".sh"): out_text += "#!bin/bash\n"
            out_text += self.get_launch_command()
            with open(fileName, "w") as f:
                f.write(out_text)
        return

    def check_version(self):
        print("checking version")

        link = "https://hitcoder-test.neocities.org/launcherblast-version.html"
        try:
            f = urllib.request.urlopen(link, timeout=100)
        except:
            print("Version check error")
            return

        my_file = f.read()
        version_got = (str(my_file).replace("b'", "").replace("\\n'", ""))
        print("Latest: " + version_got)
        print("Current: " + versionString)
        ver_num = version_got.replace("reBoot-", "")

        # check launcher version ===================================================== #
        if float(ver_num) > float(versionString.replace("reBoot-", "")):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("There is a new version available. Please check the SRB2 Message Board.")
            msg.setWindowTitle("Launcher update")
            msg.setDetailedText("Running: " + versionString + "\nLatest: " + version_got)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif float(ver_num) < float(versionString.replace("reBoot-", "")):
            print("Greetings, time traveller.")
        else:
            print("up-to-date (" + versionString + ")")


def main():
    app = QApplication(sys.argv)
    w = MainWindow(app)
    w.show()
    t = QtCore.QTimer()
    t.singleShot(0, w.applicationStarted)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
