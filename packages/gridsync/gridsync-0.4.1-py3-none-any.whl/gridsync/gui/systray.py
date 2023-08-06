# -*- coding: utf-8 -*-

import logging
import sys
import webbrowser

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import QAction, QMenu, QMessageBox, QSystemTrayIcon

from gridsync import resource, settings, APP_NAME
from gridsync._version import __version__


def open_documentation():
    webbrowser.open(settings['help']['docs_url'])


def open_issue():
    webbrowser.open(settings['help']['issues_url'])


class Menu(QMenu):
    def __init__(self, parent):
        super(Menu, self).__init__()
        self.parent = parent
        self.gui = self.parent.parent

        self.about_msg = QMessageBox()
        self.about_msg.setWindowTitle("{} - About".format(APP_NAME))
        app_icon = QIcon(resource(settings['application']['tray_icon']))
        self.about_msg.setIconPixmap(app_icon.pixmap(64, 64))
        self.about_msg.setText("{} {}".format(APP_NAME, __version__))
        self.about_msg.setWindowModality(Qt.WindowModal)

        self.populate()

    def _add_export_action(self, gateway):
        action = QAction(QIcon(''), gateway.name, self)
        action.triggered.connect(
            lambda: self.gui.main_window.export_recovery_key(gateway))
        self.export_menu.addAction(action)

    def populate(self):
        self.clear()
        logging.debug("(Re-)populating systray menu...")

        open_action = QAction(QIcon(''), "Open {}".format(APP_NAME), self)
        open_action.triggered.connect(self.gui.show)
        self.addAction(open_action)

        gateways = self.gui.main_window.gateways
        if gateways and len(gateways) > 1:
            self.export_menu = QMenu(self)
            self.export_menu.setTitle("Export Recovery Key")
            for gateway in gateways:
                self._add_export_action(gateway)
            self.addMenu(self.export_menu)
        elif gateways:
            export_action = QAction(QIcon(''), "Export Recovery Key...", self)
            export_action.triggered.connect(
                self.gui.main_window.export_recovery_key)
            self.addAction(export_action)

        help_menu = QMenu(self)
        help_menu.setTitle("Help")
        help_settings = settings.get('help')
        if help_settings:
            if help_settings.get('docs_url'):
                docs_action = QAction(
                    QIcon(''), "Browse Documentation...", self)
                docs_action.triggered.connect(open_documentation)
                help_menu.addAction(docs_action)
            if help_settings.get('issues_url'):
                issue_action = QAction(QIcon(''), "Report Issue...", self)
                issue_action.triggered.connect(open_issue)
                help_menu.addAction(issue_action)
            help_menu.addSeparator()
        about_action = QAction(QIcon(''), "About {}...".format(APP_NAME), self)
        about_action.triggered.connect(self.about_msg.exec_)
        help_menu.addAction(about_action)
        self.addMenu(help_menu)

        self.addSeparator()

        quit_action = QAction(
            QIcon(''), "&Quit {}".format(APP_NAME), self)
        quit_action.triggered.connect(self.gui.main_window.confirm_quit)
        self.addAction(quit_action)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super(SystemTrayIcon, self).__init__()
        self.parent = parent

        self.icon = QIcon(resource(settings['application']['tray_icon']))
        self.setIcon(self.icon)

        self.menu = Menu(self)
        self.setContextMenu(self.menu)
        self.activated.connect(self.on_click)

        self.animation = QMovie()
        self.animation.setFileName(
            resource(settings['application']['tray_icon_sync']))
        self.animation.updated.connect(self.update)
        self.animation.setCacheMode(True)

    def update(self):
        if self.parent.core.operations:
            self.animation.setPaused(False)
            self.setIcon(QIcon(self.animation.currentPixmap()))
        else:
            self.animation.setPaused(True)
            self.setIcon(self.icon)

    def on_click(self, value):
        if value == QSystemTrayIcon.Trigger and sys.platform != 'darwin':
            self.parent.show_main_window()
