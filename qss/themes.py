themes = {}
themes["dark"] = """
/* dock at top */
#DockTabFrame{
	background-color: #1e1e1e;
	border-color: #2f2f2f;
}

/* bottom play button panel */
#GamePlayFrame{
	background-color: #1e1e1e;
}

/* stacked widget */
QStackedWidget>QWidget{
	background-color: #2f2f2f;
}

/* list widget */
QListWidget{
	background-color: transparent;
	color: #ffffff;
}

/* scroll bars */
QScrollBar:vertical{
	background-color: #282828;
}

QScrollBar::sub-page, QScrollBar::add-page{
	background: #3b3b3b;
}

QScrollBar::handle{
	background-color: #acacac;
}

QScrollBar::handle:hover{
	background-color: #bebebe;
}

QScrollBar::handle:pressed{
	background-color: #131313;
}

/* main tabs frame */
QWidget#MainTabsFrame{
	background-color: #1e1e1e;
}

/* radio buttons for the sidebar */
QRadioButton{
	color: #ffffff;
}

QRadioButton:hover, QRadioButton:checked:hover{
	background-color: #424242;
}

QRadioButton:checked{
	background-color: #3b3b3b;
}

QRadioButton::indicator{
	background-color: transparent;
}

QRadioButton::indicator:checked{
	background-color: #2f55ff;
}

/* radio buttons for dock bar tabs */
#DockTabFrame QRadioButton::checked{
	background-color: #2f2f2f;
	border-color: #2f55ff;
}

/* q splitter */
QSplitter::handle{
	background-color: #3b3b3b;
}

/* text elementsss */

QLabel, QCheckBox{
	color: #ffffff;
	background-color: transparent;
}

/* Buttons */
QPushButton{
    font-family: "Segoe UI";
	background-color: #3c5fcf;
	color: #ffffff;
}

QPushButton:hover{
background-color: #3c5fff;
}

QPushButton:pressed{
background-color: #1a45cc;
}

QPushButton:!enabled{
	background-color: #616161;
	color: #cfcfcf;
}

/* CheckBoxes */
QCheckBox::indicator{
	background-color: #ffffff;
	border-color: #131313;
}

QCheckBox::indicator:hover{
	border-color: #282828;
}

QCheckBox::indicator:checked:hover{
	border-color: #4c6fff;
}

QCheckBox::indicator:checked{
	border-color: #3c64ff;
}

QCheckBox::indicator:pressed, QCheckBox::indicator:checked:pressed{
	background-color: #aaaaaa;
}

QCheckBox:disabled{
	color: #cccccc;
}

QCheckBox::indicator:disabled{
	border-color: #2b2b2b;
	background-color: #cccccc;
}

/* scroll area background */
QScrollArea>QWidget>QWidget{
	background-color: #3b3b3b;
}

QTabBar::tab{
	color: #bebebe;
}

QTabBar::tab:hover{
	color: #ffffff;
	background-color: #424242;
}

QTabBar::tab:selected{
	color: #ffffff;
	border-bottom-color: #2f55ff;
}

QTabWidget::pane{
	background-color: #3b3b3b;
}

/* content frames */
#GamePageContentFrame>QWidget>QWidget{
	background-color: #3b3b3b;
}

QTabWidget>QWidget>QWidget{
	background-color: #3b3b3b;
}

/* Combobox, line edit */

QLineEdit, QComboBox{
	background-color: #131313;
	color: #ffffff;
}

QComboBox::drop-down{
	image: url(:/assets/img/combobox-dropdown.png);
}

QComboBox:hover{
	background-color: #282828;
}

QTextEdit{
	color: #ffffff;
}"""
themes["light"] = """
/* stacked widget */
QStackedWidget>QWidget{
	background-color: #f5f5fa;
}

/* list widget */
QListWidget{
	background-color: transparent;
	color: #000000;
}

/* scroll bars */
QScrollBar:vertical{
	background-color: #f2f2f2;
}

QScrollBar::sub-page, QScrollBar::add-page{
	background: #ffffff;
}

QScrollBar::handle{
	background-color: #999999;
}

QScrollBar::handle:hover{
	background-color: #aaaaaa;
}

QScrollBar::handle:pressed{
	background-color: #ededed;
}

/* main tabs frame */
QWidget#MainTabsFrame{
	background-color: #ededed;
}

/* radio buttons for the sidebar */
QRadioButton{
	color: #000000;
}

QRadioButton:hover, QRadioButton:checked:hover{
	background-color: #AfCfff;
}

QRadioButton:checked{
	background-color: #9fBfff;
}

QRadioButton::indicator{
	background-color: transparent;
}

QRadioButton::indicator:checked{
	background-color: #2f55ff;
}

/* q splitter */
QSplitter::handle{
	background-color: #ededed;
}

/* text elementsss */

QLabel, QCheckBox{
	color: #000000;
	background-color: transparent;
}

/* Buttons */
QPushButton{
    font-family: "Segoe UI";
	background-color: #3c5fcf;
	color: #ffffff;
}

QPushButton:hover{
	background-color: #3c5fff;
}

QPushButton:pressed{
	background-color: #1a45cc;
}

QPushButton:!enabled{
	background-color:#616161;
	color: #ededed;
}

/* CheckBoxes */
QCheckBox::indicator{
	background-color: #ffffff;
	border-color: #222222;
}

QCheckBox::indicator:hover{
	border-color: #4c4c4c;
}

QCheckBox::indicator:checked:hover{
	border-color: #4c6fff;
}

QCheckBox::indicator:checked{
	border-color: #3c64ff;
}

QCheckBox::indicator:pressed, QCheckBox::indicator:checked:pressed{
	background-color: #aaaaaa;
}

QCheckBox:disabled{
	color: #cccccc;
}

QCheckBox::indicator:disabled{
	border-color: #4c4c4c;
	background-color: #cccccc;
}

/* scroll area background */
QScrollArea>QWidget>QWidget{
	background-color: #f5f5fa;
}

QTabBar::tab{
	color: #bebebe;
}

QTabBar::tab:hover{
	color: #000000;
	background-color: #ffffff;
}

QTabBar::tab:selected{
	color: #000000;
	border-bottom-color: #2f55ff;
}

QTabWidget::pane{
	background-color: #ffffff;
}

QTabWidget>QWidget>QWidget{
	background-color: #ffffff;
}

/* Combobox, line edit */

QLineEdit, QComboBox{
	background-color: #ffffff;
	border: 1px solid #f5f5fa;
	color: #000000;
}

QComboBox::drop-down{
	image: url(:/assets/img/combobox-dropdown-light.png);
}

QComboBox:hover{
	background-color: #f2f2f2;
}

/* dock at top */
#DockTabFrame{
	background-color: #7f9fff;
	border-color: #f2f4ff;
}

/* dock buttons */
#DockTabFrame QRadioButton::checked{
	background-color: #f2f4ff;
	border-color: #2f55ff;
}

/* bottom play button panel */
#GamePlayFrame{
	background-color: #7f9fff;
}

/* game page tabs */
#GamePageTabsFrame{
	background-color: #f2f4ff;
}"""
themes["main"] = """
/* base widgets */
QWidget{
	border: 0;
}

QScrollArea{
	border: 0;
}

/* list widget */
QListWidget{
	border: 0;
	font-family: "Segoe UI";
	font-size: 12pt;
}

QListWidget::item{
	padding: 2px;
	padding-left: 8px;
	padding-right: 8px;
}

/* scroll bars */
QScrollBar:vertical{
	width: 8px;
	margin: 1px;
}

/* radio buttons for the sidebar */

QRadioButton{
	font-family: "Segoe UI";
	font-size: 12pt;
	font: bold;
	height: 32px;
	padding-top: 4px;
	padding-bottom: 4px;
	padding-right: 16px;
}

QRadioButton::icon{
	margin-right: 2px;
}

QRadioButton::indicator{
	width: 4px;
	height: 32px;
}

/* top dock */
#DockTabFrame{
	border-bottom: 1px solid transparent;
}

/* radio buttons for main tabs */
#DockTabFrame QRadioButton{
	font-family: "Segoe UI";
	font-size: 12pt;
	font: bold;
	height: 48px;
	padding-top: 2px;
	padding-bottom: 0;
	padding-right: 0;
	border-top: 4px solid transparent;
}

#DockTabFrame QRadioButton::icon{
	margin: 0;
}

#DockTabFrame QRadioButton::indicator{
	width: 0;
}

/* text elementsss */
QLabel, QCheckBox{
	font: bold 10pt;
	font-family: "Segoe UI";
	padding-left: 0px;
	padding-top: 6px;
	max-height: 20px;
}

QLabel#PlayerSkinInfoText{
	font: bold 10pt;
	padding: 0;
	padding-left: 4px;
	padding-right: 4px;
}

QLabel#GamePlayGraphicLabel{
	max-height: 999999px;
	padding: 0;
}

#PlayerSkinInfoWrapper QLabel{
	padding: 0;
	margin: 4px;
	max-height: 999999px;
}

QStackedWidget>QWidget>QLabel{
	padding-left: 0;
}

/* Buttons */

QPushButton{
    font-family: "Segoe UI";
	font-size: 10pt;
	padding-left: 8px;
	padding-right: 8px;
	border: 0;
	min-height: 28px;
}

QPushButton#GamePlayButton{
	font: bold;
	font-size: 12pt;
	padding-left: 8px;
	padding-right: 8px;
	min-height: 38px;
}

/* CheckBoxes */

QCheckBox::indicator{
	border: 3px solid;
	border-right-width: 16px;
	width: 13px;
	height: 12px;
}

QCheckBox::indicator:checked{
	border-right-width: 3px;
	border-left-width: 16px;
}

/* scroll area background */
QScrollArea>QWidget>QWidget{
	border: none;
}

/* Tabs */

QTabWidget::tab-bar{
	left: 16px;
}

QTabBar::tab{
	font-size: 12pt;
	border-bottom: 2px solid transparent;
	height: 28px;
	width: 128px;
}

QTabBar::tab:selected{
	font: bold;
}

QTabWidget::pane{
	border: none;
}

/* Combobox, line edit */
QLineEdit, QComboBox{
	font-family: "Segoe UI";
	font-size: 12pt;
	border-radius: 4px;
	height: 24px;
	padding-left: 8px;
	padding-right: 8px;
	padding-bottom: 4px;
}

QComboBox::drop-down{
	border: 0;
	margin: 6px;
}

QTextEdit{
	background-color: transparent;
}"""
themes["pink"] = """
/* stacked widget */
QStackedWidget>QWidget{
	background-color: #C23657;
}

/* list widget */
QListWidget{
	background-color: transparent;
	color: #FFE0F0;
}

/* scroll bars */
QScrollBar:vertical{
	background-color: #282828;
}

QScrollBar::sub-page, QScrollBar::add-page{
	background: #D33C67;
}

QScrollBar::handle{
	background-color: #acacac;
}

QScrollBar::handle:hover{
	background-color: #FFB8F8;
}

QScrollBar::handle:pressed{
	background-color: #AC2D40;
}

/* main tabs frame */
QWidget#MainTabsFrame{
	background-color: #B53049;
}

/* radio buttons for the sidebar */
QRadioButton{
	color: #FFE0F0;
}

QRadioButton:hover, QRadioButton:checked:hover{
	background-color: #383838;
}

QRadioButton:checked{
	background-color: #B73574;
}

QRadioButton::indicator{
	background-color: transparent;
}

QRadioButton::indicator:checked{
	background-color: #E021C6;
}

/* q splitter */
QSplitter::handle{
	background-color: #AC2D40;
}

/* text elementsss */

QLabel, QCheckBox{
	color: #FFE0F0;
	background-color: transparent;
}

/* Buttons */
QPushButton{
    font-family: "Segoe UI";
	background-color: #E24CCE;
	color: #FFE0F0;
}

QPushButton:hover{
background-color: #E650E6;
}

QPushButton:pressed{
background-color: #C543C3;
}

QPushButton:!enabled{
	background-color:#616161;
	color: #cfcfcf;
}

/* CheckBoxes */
QCheckBox::indicator{
	background-color: #FFE0F0;
	border-color: #AC2D40;
}

QCheckBox::indicator:hover{
	border-color: #282828;
}

QCheckBox::indicator:checked:hover{
	border-color: #4c6fff;
}

QCheckBox::indicator:checked{
	border-color: #3c64ff;
}

QCheckBox::indicator:pressed, QCheckBox::indicator:checked:pressed{
	background-color: #aaaaaa;
}

QCheckBox:disabled{
	color: #cccccc;
}

QCheckBox::indicator:disabled{
	border-color: #C23657;
	background-color: #cccccc;
}

/* scroll area background */
QScrollArea>QWidget>QWidget{
	background-color: #D33C67;
}

QTabBar::tab{
	color: #FFB8F8;
}

QTabBar::tab:hover{
	color: #FFE0F0;
	background-color: #E0479B;
}

QTabBar::tab:selected{
	color: #FFE0F0;
	border-bottom-color: #E021C6;
}

QTabWidget::pane{
	background-color: #D33C67;
}

QTabWidget>QWidget>QWidget{
	background-color: #D33C67;
}

/* Combobox, line edit */

QLineEdit, QComboBox{
	background-color: #AC2D40;
	color: #FFE0F0;
}

QComboBox::drop-down{
	image: url(:/assets/img/combobox-dropdown.png);
}

QComboBox:hover{
	background-color: #282828;
}

#DockTabFrame{
	background-color: #6C1D40;
}

#GamePlayFrame{
	background-color: #6C1D40;
}"""
