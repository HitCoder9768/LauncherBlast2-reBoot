import fix_qt_import_error
import sys, os, PyQt5.QtWidgets, json, feedparser, json, pathlib, characterText, urllib, subprocess
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMenu, QMessageBox
from LauncherUI import *
from datetime import date
from qss import themes
import EditServerMain

fool = date.today()==date(date.today().year, 4, 1)

versionString = "reBoot-2.0"

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        self.configData = self.readConfig()

        self.applyStyle()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.app = app

        # server ips stored internally so u don't dox people's ips if you're streaming or smth
        self.serverIps = []

        # load servers from file ===================================================== #
        #self.loadServerList()
        self.hasLoadedServers = False

        # launcher config settings =========================#
        self.launcherConfigFile = "LauncherBlast2Conf.json"


        # allow posix systems to use wine ============================================ #
        if(os.name=="posix"):
            self.ui.WineToggle.setEnabled(True)

        # file dialog options to keep shit consistent ================================ #
        self.FileDialogOptions = QFileDialog.Options()
        #self.FileDialogOptions |= QFileDialog.DontUseNativeDialog

        # set tab to game tab initially ============================================== #
        self.ui.MainTabsStackedWidget.setCurrentIndex(1)

        # fix resolution of skin image =============================================== #
        self.ui.PlayerSkinImage.setPixmap(QtGui.QPixmap(":/assets/img/sonic.png").scaled(135,190,aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.FastTransformation))

        # changed skin index ========================================================= #
        self.ui.PlayerSkinInput.currentIndexChanged.connect(self.changeSkinImage)

        # clear files list =========================================================== #
        self.ui.GameFilesList.clear()

        # clear servers list ========================================================= #
        self.ui.ServerList.clear()

        # dock "tabs" ================================================================ #
        self.ui.NewsTabButton.clicked.connect(lambda: self.changeMainTab(0))
        self.ui.GameTabButton.clicked.connect(lambda: self.changeMainTab(1))
        self.ui.HelpTabButton.clicked.connect(lambda: self.changeMainTab(2))
        self.ui.SettingsTabButton.clicked.connect(lambda: self.changeMainTab(3))

        # game "tabs" ================================================================ #
        self.ui.ProfileTabButton.clicked.connect(lambda: self.changeGameTab(0))
        self.ui.FilesTabButton.clicked.connect(lambda: self.changeGameTab(1))
        self.ui.GameSettingsTabButton.clicked.connect(lambda: self.changeGameTab(2))
        self.ui.PlayerSetupTabButton.clicked.connect(lambda: self.changeGameTab(3))
        self.ui.HostGameTabButton.clicked.connect(lambda: self.changeGameTab(4))
        self.ui.JoinGameTabButton.clicked.connect(lambda: self.changeGameTab(5))

        # files list buttons ========================================================= #
        self.ui.GameFilesClearButton.clicked.connect(self.clearFilesList)
        self.ui.GameFilesDeleteButton.clicked.connect(self.deleteSelectedFiles)
        self.ui.GameFilesUpButton.clicked.connect(self.moveSelectedFilesUp)
        self.ui.GameFilesDownButton.clicked.connect(self.moveSelectedFilesDown)
        self.ui.GameFilesAddButton.clicked.connect(self.addFiles)
        self.ui.GameFilesSaveButton.clicked.connect(self.saveFileList)
        self.ui.GameFilesLoadButton.clicked.connect(self.loadFileList)
        self.ui.GameFilesExecScrBrowseButton.clicked.connect(self.setExecFilePath)

        # server list buttons ======================================================== #
        self.ui.AddServerButton.clicked.connect(self.showAddServerDialog)
        self.ui.JoinServerButton.clicked.connect(self.joinSelectedServer)
        self.ui.DeleteServerButton.clicked.connect(self.deleteSelectedServer)
        self.ui.EditServerButton.clicked.connect(self.openServerEditor)
        self.ui.JoinAddressButton.clicked.connect(self.joinFromIP)

        # play button ================================================================ #
        self.ui.GamePlayButton.clicked.connect(self.launchGameNormally)
        #self.ui.GameOptionsDropDownButton.clicked.connect()
        self.gameOptionsDropDownMenu = QMenu()
        self.gameOptionsDropDownMenu.addAction("Save current parameters to script",self.exportScript)
        self.ui.GameOptionsDropDownButton.setMenu(self.gameOptionsDropDownMenu)
        self.ui.GameOptionsDropDownButton.clicked.connect(self.showGameOptionsDropDownMenu)

        # load news feed from srb2.org =============================================== #
        self.loadNewsFeed()
        
        # and then add the spacer at the bottom
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ui.verticalLayout_20.addItem(spacerItem)

    def showGameOptionsDropDownMenu(self):
        menu = QMenu()
        menu.addAction("Save current parameters to script",self.exportScript)
        menu.exec()

    def loadNewsFeed(self):
        # ok lets uh, get the news feed or something?
        srb2_rss_url = "https://www.srb2.org/feed/"

        feed = feedparser.parse(srb2_rss_url)
        items = feed["items"]

        for item in items:
            # title
            articleTitleLabel = QtWidgets.QLabel(self.ui.NewsScrollAreaContent)
            articleTitleLabel.setStyleSheet("font-size: 14pt;")
            urlLink="<a href=\"" + item["link"] + "\" style=\"color: #aaa;\">" + item["title"] + "</a>"
            articleTitleLabel.setText(QtCore.QCoreApplication.translate("MainWindow", urlLink))
            articleTitleLabel.setOpenExternalLinks(True)
            self.ui.verticalLayout_20.addWidget(articleTitleLabel)

            # author name and date
            authorNameLabel = QtWidgets.QLabel(self.ui.NewsScrollAreaContent)
            authorNameLabel.setStyleSheet("font-weight: 400;")
            authorNameLabel.setText(item["author"] + " - "+ item["published"].replace(" +0000",""))
            self.ui.verticalLayout_20.addWidget(authorNameLabel)

            # snippet
            infoLabel = QtWidgets.QLabel(self.ui.NewsScrollAreaContent)
            infoLabel.setStyleSheet("font-weight: 400;")
            infoLabel.setText("<div style=\"text-wrap: wrap-word;\">"+item["summary"]+"</div>")
            infoLabel.setWordWrap(True)
            infoLabel.adjustSize()
            infoLabel.setSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Minimum)
            self.ui.verticalLayout_20.addWidget(infoLabel)

    # add server window ============================================================== #
    # ================================================================================ #
    def showAddServerDialog(self):
        self.childWindow = EditServerMain.ChildWindow(self,"","",True)
        self.childWindow.show()
        return
        
    # change character image for skin thing ========================================== #
    # ================================================================================ #
    def changeSkinImage(self):
        assetImg = ":/assets/img/sonic.png"
        self.ui.PlayerSkinInfoText.setText(characterText.sonic)
        if(self.ui.PlayerSkinInput.currentIndex() == 2):
            assetImg = ":/assets/img/tails.png"
            self.ui.PlayerSkinInfoText.setText(characterText.tails)
        if(self.ui.PlayerSkinInput.currentIndex() == 3):
            assetImg = ":/assets/img/knuckles.png"
            self.ui.PlayerSkinInfoText.setText(characterText.knux)
        if(self.ui.PlayerSkinInput.currentIndex() == 4):
            assetImg = ":/assets/img/rosy.png"
            self.ui.PlayerSkinInfoText.setText(characterText.amy)
        if(self.ui.PlayerSkinInput.currentIndex() == 5):
            assetImg = ":/assets/img/fang.png"
            self.ui.PlayerSkinInfoText.setText(characterText.fang)
        if(self.ui.PlayerSkinInput.currentIndex() == 6):
            assetImg = ":/assets/img/metal.png"
            self.ui.PlayerSkinInfoText.setText(characterText.metal)


        self.ui.PlayerSkinImage.setPixmap(QtGui.QPixmap(assetImg).scaled(135,190,aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.FastTransformation))
        return

    # create srb2 launch command ===================================================== #
    # ================================================================================ #
    # this converts all of the launcher inputs to a single-string command to launch    #
    # srb2.                                                                            #
    def getLaunchCommand(self):
        ui = self.ui
        com = ""
        if(self.ui.WineToggle.isChecked() and self.ui.WineToggle.isEnabled()): com += "wine "
        com += "\""+ui.GameExecFilePathInput.text()+"\""

        # game settings (from game settings tab) ===================================== #
        if(ui.GameRendererSetting.currentIndex()==0): com += " +renderer 1"
        if(ui.GameRendererSetting.currentIndex()==1): com += " +renderer 2"
        if(ui.GameFullscreenSetting.currentIndex()==0): com += " +fullscreen 1"
        if(ui.GameFullscreenSetting.currentIndex()==1): com += " -borderless"
        if(ui.GameFullscreenSetting.currentIndex()==2): com += " -win"
        if(ui.GameMusicSetting.currentIndex()==0): com += " +digimusic On"
        if(ui.GameMusicSetting.currentIndex()==1): com += " +digimusic Off"
        if(ui.GameMusicSetting.currentIndex()==2): com += " -usecd"
        if(ui.GameMusicSetting.currentIndex()==3): com += " -nomusic"
        if(ui.GameSoundSetting.currentIndex()==1): com += " -nosound"
        if(ui.GameHorizontalResolutionInput.text()!="" and ui.GameVerticalResolutionInput.text()!=""):
            com += " -width " + ui.GameHorizontalResolutionInput.text() + " -height " + ui.GameVerticalResolutionInput.text()
        if(ui.PlayerNameInput.text()!=""): com += " +name \"" + ui.PlayerNameInput.text() + "\""
        if(ui.PlayerColorInput.currentIndex()!=0): com += " +color " + str(ui.PlayerColorInput.currentText().lower())
        if(ui.PlayerSkinInput.currentIndex()!=0): com += " +skin " + str(ui.PlayerSkinInput.currentText().lower().replace(" ",""))

        # get all files ============================================================== #
        com += " -file"
        for i in range(ui.GameFilesList.count()):
            com += " \"" + ui.GameFilesList.item(i).text() + "\""

        # add a script =============================================================== #
        if(ui.GameFilesExecScriptInput.text()!=""): com += " +exec " + ui.GameFilesExecScriptInput.text()

        # custom parameters ========================================================== #
        if(ui.GameArgsInput.text()!=""): com += " " + ui.GameArgsInput.text()
        
        return com

    # clear files list =============================================================== #
    # ================================================================================ #
    def clearFilesList(self):
        self.ui.GameFilesList.clear()
        return

    # delete current file ============================================================ #
    # ================================================================================ #
    def deleteSelectedFiles(self):
        for item in self.ui.GameFilesList.selectedItems():
            self.ui.GameFilesList.takeItem(self.ui.GameFilesList.row(item))
        return

    # move files up ================================================================== #
    # ================================================================================ #
    def moveSelectedFilesUp(self):
        for item in self.ui.GameFilesList.selectedItems():
            row = self.ui.GameFilesList.row(item)
            if(row==0): return
            cItem = self.ui.GameFilesList.takeItem(row)
            self.ui.GameFilesList.insertItem(row - 1, cItem)
            cItem.setSelected(True)
        return

    # move files down ================================================================ #
    # ================================================================================ #
    def moveSelectedFilesDown(self):
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
    def addFile(self, f):
        newItem = QtWidgets.QListWidgetItem()
        newItem.setText(os.path.basename(str(f)))
        newItemIcon = QtGui.QIcon()
        filetype = str(f).split(".")[-1]
        newItemIcon.addPixmap(QtGui.QPixmap(":/assets/img/filetypes/"+filetype+".png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        newItem.setIcon(newItemIcon)
        self.ui.GameFilesList.addItem(newItem)
        return

    # add files button =============================================================== #
    # ================================================================================ #
    def addFiles(self):
        files, _ = QFileDialog.getOpenFileNames(self,"Open files to add to SRB2", "", "All compatible SRB2 files (*.pk3 *.wad *.lua *.soc);;PK3 Files (*.pk3);;WAD Files (*.wad);;Lua Files (*.lua);;SOC files (*.soc)", options=self.FileDialogOptions)
        if files:
            # add each file to the file list with icon =============================== #
            for f in files:
                self.addFile(f)
        return

    def saveFileList(self):
        # convert to json compatible list ============================================ #
        items = []
        for i in range(self.ui.GameFilesList.count()):
            items.append(self.ui.GameFilesList.item(i).text())

        # open a file dialog ========================================================= #
        f, _ = QFileDialog.getSaveFileName(self,"Save file list","","JSON files (*.json)", options=self.FileDialogOptions)
        if f:
            with open(f, 'w') as outfile:
                json.dump(items,outfile)
        return

    def loadFileList(self):
        # open file ================================================================== #
        f, _ = QFileDialog.getOpenFileName(self,"Open file list","","JSON files (*.json)",options=self.FileDialogOptions)
        if f:
            with open(f,'r') as jsonFile:
                items = json.load(jsonFile)
                for item in items:
                    self.addFile(item)
        return

    def setExecFilePath(self):
        f, _ = QFileDialog.getOpenFileName(self,"Open script to execute on launch","","All compatible files (*.txt *.cfg);;All files (*)",options=self.FileDialogOptions)
        if(f):
            self.ui.GameFilesExecScriptInput.setText(f)

    # play button ==================================================================== #
    # ================================================================================ #
    def launchGameNormally(self):
        launchCommand = self.getLaunchCommand()
        os.system(launchCommand)
        return

    # change tab function ============================================================ #
    # ================================================================================ #
    def changeMainTab(self, index):
        self.ui.MainTabsStackedWidget.setCurrentIndex(index)
        return

    # change game tab function ======================================================= #
    # ================================================================================ #
    def changeGameTab(self, index):
        self.ui.GameContentStackedWidget.setCurrentIndex(index)
        return

    # save servers list to file ====================================================== #
    # ================================================================================ #
    def saveServerList(self):
        servList = []
        for i in range(len(self.serverIps)):
            data = { "name" : self.ui.ServerList.item(i).text(), "ip" : self.serverIps[i] }
            servList.append(data)
        with open("lb2ServerList.json", "w") as f:
            json.dump(servList, f)
        return

    # load server list =============================================================== #
    # ================================================================================ #
    def loadServerList(self):
        servList = []
        fpath = os.path.join(os.getcwd(),"lb2ServerList.json")
        if not os.path.isfile(fpath):
            return
        with open(fpath, "r") as f:
            servList = json.load(f)

        for server in servList:
            self.addServerToList(server["name"],server["ip"])
        return

    # add server to server list ====================================================== #
    # ================================================================================ #
    def addServerToList(self,name,ip):
        newItem = QtWidgets.QListWidgetItem()
        newItem.setText(name)
        self.serverIps.append(ip)
        self.ui.ServerList.addItem(newItem)
        self.saveServerList()
        return

    # open server editor ============================================================= #
    # ================================================================================ #
    def openServerEditor(self):
        ip = self.serverIps[self.ui.ServerList.selectedIndexes()[0].row()]
        name = self.ui.ServerList.selectedItems()[0].text()
        self.childWindow = EditServerMain.ChildWindow(self,name,ip,False)
        self.childWindow.show()
        return

    # edit server in list ============================================================ #
    # ================================================================================ #
    def editSelectedServer(self,name,ip):
        self.serverIps[self.ui.ServerList.selectedIndexes()[0].row()] = ip
        self.ui.ServerList.selectedItems()[0].setText(name)
        self.saveServerList()
        return

    # delete server in list ========================================================== #
    # ================================================================================ #
    def deleteServerFromList(self,index):
        self.serverIps.pop(index)
        self.ui.ServerList.takeItem(index)
        self.saveServerList()
        return

    # delete selected server ========================================================= #
    # ================================================================================ #
    def deleteSelectedServer(self):
        self.deleteServerFromList(self.ui.ServerList.selectedIndexes()[0].row())
        return

    # join current selected server in list =========================================== #
    # ================================================================================ #
    def joinSelectedServer(self):
        ipString = self.serverIps[self.ui.ServerList.selectedIndexes()[0].row()]
        os.system(self.getLaunchCommand() + " -connect " + ipString)
        return

    # join direct address ============================================================ #
    # ================================================================================ #
    def joinFromIP(self):
        ipString = self.ui.JoinAddressInput.text
        os.system(self.getLaunchCommand() + " -connect " + ipString)
        return

    # join current selected server in list =========================================== #
    # ================================================================================ #
    def startServer(self):
        launchCommand = self.ui.GameExecFilePathInput.text() + " -server"
        if(not self.ui.DedicatedServerToggle.isChecked):
            launchCommand = self.getLaunchCommand()

        if(self.ui.ServerNameInput.text()!=""): launchCommand += " +servername " + self.ui.ServerNameInput.text()
        if(self.ui.AdminPasswordInput.text()!=""): launchCommand += " +password " + self.ui.AdminPasswordInput.text()
        if(self.ui.RoomInput.currentIndex()!=0):
            launchCommand += " -id "
            if(self.ui.RoomInput.currentIndex()==1): launchCommand += "33"
            if(self.ui.RoomInput.currentIndex()==2): launchCommand += "28"
            if(self.ui.RoomInput.currentIndex()==3): launchCommand += "38"
            if(self.ui.RoomInput.currentIndex()==4): launchCommand += "31"
        launchCommand += " -gametype " + str(self.ui.GametypeInput.currentIndex())
        launchCommand += " +advancemap " + str(self.ui.AdvanceMapInput.currentIndex())
        if(self.ui.PointLimitInput.text()!=""): launchCommand += " +pointlimit " + self.ui.PointLimitInput.text()
        else: launchCommand += " +pointlimit 1000"
        if(self.ui.TimeLimitInput.text()!=""): launchCommand += " +timelimit " + self.ui.TimeLimitInput.text()
        else: launchCommand += " +timelimit 0"
        if(self.ui.MaxPlayersInput.text()!=""): launchCommand += " +maxplayers " + self.ui.MaxPlayersInput.text()
        else: launchCommand += " +maxplayers 8"
        if(self.ui.ForceSkinInput.currentText()!=""): launchCommand += " +forceskin " + self.ui.ForceSkinInput.currentText().lower().replace(" ","")
        if(self.ui.PortInput.text()!=""): launchCommand += " -port " + self.ui.PortInput.text()
        else: launchCommand += " -port 5029"
        if(self.ui.DisableWeaponsToggle.isChecked()): launchCommand += " +specialrings 1"
        else: launchCommand += " +specialrings 0"
        if(self.ui.SuddenDeathToggle.isChecked()): launchCommand += " +suddendeath 1"
        else: launchCommand += " +suddendeath 0"
        if(self.ui.DedicatedServerToggle.isChecked()): launchCommand += " -dedicated"
        if(self.ui.UploadToggle.isChecked()): launchCommand += " +downloading 1"
        else: launchCommand += " +downloading 0"

        os.system(launchCommand)
        return

    # when closed save stuff ========================================================= #
    # ================================================================================ #
    def closeEvent(self, e):
        self.saveConfig()
        return

    # wait for window the fully start ================================================ #
    # ================================================================================ #
    def applicationStarted(self):
        # fix resolution of the image on the play tab ================================ #
        self.loadServerList()
        self.loadConfig()
        self.checkVersion()

        # april fools day stuff
        if(fool):
            self.ui.PlayerSkinInput.setCurrentIndex(4)
            self.ui.PlayerColorInput.setCurrentIndex(57)
            self.ui.PlayerColorInput.setEnabled(False)
            self.ui.PlayerSkinInput.setEnabled(False)

        return

    # save launcher config =========================================================== #
    # ================================================================================ #
    def saveConfig(self):
        # generate the json data for the config
        confJson = {"files":[],"player":{},"game":{"resolution":{}},"host":{},"settings":{}}
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
    def readConfig(self):
        configData = {}
        fpath = os.path.join(os.getcwd(),"LauncherBlast2Conf.json")
        #print(fpath)
        if not os.path.isfile(fpath):
            return 0
        with open(fpath, "r") as f:
            configData = json.load(f)

        return configData

    # load launcher config =========================================================== #
    # ================================================================================ #
    def loadConfig(self):

        if(self.configData == 0):
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

        if(self.ui.SaveFilesToConfigToggle.isChecked):
            for f in self.configData["files"]:
                self.addFile(f)
        
        
        self.changeSkinImage()
        return

    # apply launchder style ========================================================== #
    # ================================================================================ #
    def applyStyle(self):
        # set up the launcher theme
        if(self.configData == 0):
            self.setStyleSheet(themes.main + themes.dark)
            return

        if(self.configData["settings"]["theme"] == 0): chosentheme = themes.dark
        if(self.configData["settings"]["theme"] == 1): chosentheme = themes.light
        if(self.configData["settings"]["theme"] == 2): chosentheme = themes.blue
        if(self.configData["settings"]["theme"] == 3): chosentheme = themes.orange
        if(self.configData["settings"]["theme"] == 4): chosentheme = themes.red
        if(self.configData["settings"]["theme"] == 5): chosentheme = themes.pink
        if(self.configData["settings"]["theme"] == 6): chosentheme = themes.lightsout

        # april fools day stuff. pls dont spoil for others!11!1
        if(fool):
            chosentheme = themes.pink

        self.setStyleSheet(themes.main + chosentheme)
        return

    # apply launchder style ========================================================== #
    # ================================================================================ #
    def exportScript(self):
        fileFilter = "Batch files (*.bat);;Shell scripts (*.sh)"
        if(os.name=="posix"):
            fileFilter = "Shell scripts (*.sh);;Batch files (*.bat)"
        fileFilter += ";;All files (*)"
        fileName,_ = QFileDialog.getSaveFileName(self,"Save script",os.getcwd(),fileFilter)
        if fileName:
            outText = ""
            if(fileName.endswith(".sh")): outText += "#!bin/bash\n"
            outText += self.getLaunchCommand()
            with open(fileName, "w") as f:
                f.write(outText)
        return

    def checkVersion(self):
        print("checking version")

        link = "https://hitcoder-test.neocities.org/launcherblast-version.html"
        try:
            f = urllib.request.urlopen(link,timeout=100)
        except:
            print("Version check error")
            return
        
        myfile = f.read()
        versionGot = (str(myfile).replace("b'","").replace("\\n'",""))
        print("Latest: "+versionGot)
        print("Current: "+versionString)
        verNum = versionGot.replace("reBoot-","")

        # check launcher version ===================================================== #
        if(float(verNum) > float(versionString.replace("reBoot-",""))):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("There is a new version available. Please check the SRB2 Message Board.")
            msg.setWindowTitle("Launcher update")
            msg.setDetailedText("Running: "+versionString+"\nLatest: "+versionGot)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif (float(verNum) < float(versionString.replace("reBoot-",""))):
            print("Greetings, time traveller.")
        else:
            print("up-to-date ("+versionString+")")
        

def main():
    app = QApplication(sys.argv)
    w = MainWindow(app)
    w.show()
    t = QtCore.QTimer()
    t.singleShot(0,w.applicationStarted)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()