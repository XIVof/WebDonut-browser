import os
import traceback
def log_message_handler(msg_type, context, message):
    if msg_type == 0:  # QtDebugMsg
        return

    error_msg = f"Message type: {msg_type}\nMessage: {message}\nLocation: {context.file}:{context.line}, {context.function}\n"
    print(error_msg)
    with open("error_log.txt", "a") as log_file:
        log_file.write(error_msg)

    # Uncomment the following line if you want to show an error dialog for every error
    # QMessageBox.critical(None, 'Error', f'An error occurred: {message}')

from PyQt5.QtCore import QUrl, QSettings
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QMessageBox, QTabWidget, QVBoxLayout, QDialog, QListWidget, QPushButton, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage, QWebEngineProfile

class WebDonutBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        local_file_url = QUrl.fromLocalFile(os.path.abspath(os.path.join(os.path.dirname(__file__), "mainpage.html")))
        self.add_new_tab(local_file_url, "Main Page")

        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction(QIcon('back.png'), 'Назад', self)
        back_btn.setStatusTip('Назад на предыдущую страницу')
        back_btn.triggered.connect(lambda: self.current_tab().back())
        navbar.addAction(back_btn)

        forward_btn = QAction(QIcon('forward.png'), 'Вперед', self)
        forward_btn.setStatusTip('Вперед на следующую страницу')
        forward_btn.triggered.connect(lambda: self.current_tab().forward())
        navbar.addAction(forward_btn)

        reload_btn = QAction(QIcon('reload.png'), 'Обновить', self)
        reload_btn.setStatusTip('Обновить страницу')
        reload_btn.triggered.connect(lambda: self.current_tab().reload())
        navbar.addAction(reload_btn)

        home_btn = QAction(QIcon('home.png'), 'Домой', self)
        home_btn.setStatusTip('Перейти на домашнюю страницу')
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        go_btn = QAction(QIcon('go.png'), 'Перейти', self)
        go_btn.setStatusTip('Перейти по указанному адресу')
        go_btn.triggered.connect(self.navigate_to_url)
        navbar.addAction(go_btn)

        bookmark_btn = QAction(QIcon('bookmark.png'), 'Добавить в закладки', self)
        bookmark_btn.setStatusTip('Добавить текущую страницу в закладки')
        bookmark_btn.triggered.connect(self.add_to_bookmarks)
        navbar.addAction(bookmark_btn)

        load_bookmarks_btn = QAction(QIcon('load_bookmarks.png'), 'Загрузить закладки', self)
        load_bookmarks_btn.setStatusTip('Показать список закладок')
        load_bookmarks_btn.triggered.connect(self.show_bookmarks)
        navbar.addAction(load_bookmarks_btn)

        external_page_btn = QAction(QIcon('external_page.png'), 'Открыть внешнюю страницу', self)
        external_page_btn.setStatusTip('Открыть внешнюю страницу в новом окне')
        external_page_btn.triggered.connect(self.open_external_page)
        navbar.addAction(external_page_btn)

        new_tab_btn = QAction(QIcon('new_tab.png'), 'Новая вкладка', self)
        new_tab_btn.setStatusTip('Открыть новую вкладку')
        new_tab_btn.triggered.connect(self.add_new_tab_action)
        navbar.addAction(new_tab_btn)

        incognito_btn = QAction(QIcon('incognito.png'), 'Инкогнито', self)
        incognito_btn.setStatusTip('Открыть новую вкладку в режиме инкогнито')
        incognito_btn.triggered.connect(self.add_new_tab_incognito)
        navbar.addAction(incognito_btn)

        theme_menu = self.menuBar().addMenu('Тема')

        themes = [
            ('Светлая', ''),
            ('Темная', 'QMainWindow{background-color: #2e2e2e; color: #ffffff;} '
                    'QToolBar{border: 0px; background-color: #2e2e2e; spacing: 3px;} '
                    'QLineEdit{border: 1px solid #555; padding: 2px; background-color: #3a3a3a; color: #ffffff;} '
                    'QTabWidget{border: 0px; padding: 0px;} '
                    'QTabBar{background-color: #2e2e2e; border: 0px;} '
                    'QTabBar::tab{background-color: #3a3a3a; color: #ffffff; padding: 4px; margin: 0px;} '
                    'QTabBar::tab:selected{background-color: #555;} '
                    'QMenuBar{background-color: #2e2e2e;} '
                    'QMenu{background-color: #2e2e2e; color: #ffffff;} '
                    'QMenu::item:selected{background-color: #555;}'),
            ('Фиолетовая', 'QMainWindow{background-color: #800080; color: #ffffff;} '
                       'QToolBar{border: 0px; background-color: #800080; spacing: 3px;} '
                       'QLineEdit{border: 1px solid #555; padding: 2px; background-color: #9400D3; color: #ffffff;} '
                       'QTabWidget{border: 0px; padding: 0px;} '
                       'QTabBar{background-color: #800080; border: 0px;} '
                       'QTabBar::tab{background-color: #9400D3; color: #ffffff; padding: 4px; margin: 0px;} '
                       'QTabBar::tab:selected{background-color: #555;} '
                       'QMenuBar{background-color: #800080;} '
                       'QMenu{background-color: #800080; color: #ffffff;} '
                       'QMenu::item:selected{background-color: #555;}'),
            ('Синяя', 'QMainWindow{background-color: #000080; color: #ffffff;} '
                     'QToolBar{border: 0px; background-color: #000080; spacing: 3px;} '
                     'QLineEdit{border: 1px solid #555; padding: 2px; background-color: #0000CD; color: #ffffff;} '
                     'QTabWidget{border: 0px; padding: 0px;} '
                     'QTabBar{background-color: #000080; border: 0px;} '
                     'QTabBar::tab{background-color: #0000CD; color: #ffffff; padding: 4px; margin: 0px;} '
                     'QTabBar::tab:selected{background-color: #555;} '
                     'QMenuBar{background-color: #000080;} '
                     'QMenu{background-color: #000080; color: #ffffff;} '
                     'QMenu::item:selected{background-color: #555;}'),
            ('Желтая', 'QMainWindow{background-color: #FFFF00; color: #000000;} '
                       'QToolBar{border: 0px; background-color: #FFFF00; spacing: 3px;} '
                       'QLineEdit{border: 1px solid #555; padding: 2px; background-color: #FFD700; color: #000000;} '
                       'QTabWidget{border: 0px; padding: 0px;} '
                       'QTabBar{background-color: #FFFF00; border: 0px;} '
                       'QTabBar::tab{background-color: #FFD700; color: #000000; padding: 4px; margin: 0px;} '
                       'QTabBar::tab:selected{background-color: #555;} '
                       'QMenuBar{background-color: #FFFF00;} '
                       'QMenu{background-color: #FFFF00; color: #000000;} '
                       'QMenu::item:selected{background-color: #555;}'),
        ]

        for theme_name, stylesheet in themes:
            theme_action = QAction(theme_name, self)
            theme_action.triggered.connect(lambda _, sheet=stylesheet: self.set_theme(sheet))
            theme_menu.addAction(theme_action)

        search_menu = self.menuBar().addMenu('Поиск')
        self.search_history_menu = search_menu.addMenu('История поиска')

        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle('WebDonut Browser')

        self.bookmarks = []

        # Загрузка текущей темы из настроек
        self.load_theme()

        self.load_bookmarks()

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def add_new_tab_action(self):
        self.add_new_tab()

    def add_new_tab(self, qurl=None, label="Blank"):
        try:
            if qurl is None:
                qurl = QUrl('https://01242451-8c48-45ea-8b22-15d77776d2d7-00-3fl1lk3dvlb9t.spock.replit.dev/')

            browser = QWebEngineView()
            browser.setUrl(qurl)

            i = self.tabs.addTab(browser, QIcon('new_tab.png'), label)
            self.tabs.setCurrentIndex(i)

            browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
            browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def add_new_tab_incognito(self):
        incognito_profile = QWebEngineProfile("incognito", self)
        incognito_page = QWebEnginePage(incognito_profile, self)
        incognito_browser = QWebEngineView()
        incognito_browser.setPage(incognito_page)
        incognito_browser.setUrl(QUrl('https://01242451-8c48-45ea-8b22-15d77776d2d7-00-3fl1lk3dvlb9t.spock.replit.dev/'))

        i = self.tabs.addTab(incognito_browser, QIcon('incognito.png'), 'Инкогнито')
        self.tabs.setCurrentIndex(i)

        incognito_browser.urlChanged.connect(lambda qurl, browser=incognito_browser: self.update_urlbar(qurl, browser))
        incognito_browser.loadFinished.connect(lambda _, i=i, browser=incognito_browser: self.tabs.setTabText(i, browser.page().title()))

    def current_tab(self):
        return self.tabs.currentWidget()

    def navigate_home(self):
        self.current_tab().setUrl(QUrl("https://01242451-8c48-45ea-8b22-15d77776d2d7-00-3fl1lk3dvlb9t.spock.replit.dev/"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.current_tab().setUrl(q)

    def add_to_bookmarks(self):
        current_url = self.current_tab().url().toString()
        self.bookmarks.append(current_url)
        self.save_bookmarks()
        QMessageBox.information(self, 'Добавить в закладки', f'Добавлено в закладки:\n\n{current_url}')

    def show_bookmarks(self):
        if not self.bookmarks:
            QMessageBox.information(self, 'Закладки', 'Нет сохраненных закладок.')
            return

        dialog = QDialog(self)
        dialog.setWindowTitle('Закладки')

        layout = QVBoxLayout(dialog)

        list_widget = QListWidget()
        list_widget.addItems(self.bookmarks)

        open_button = QPushButton('Открыть')
        open_button.clicked.connect(self.open_selected_bookmark)

        layout.addWidget(list_widget)
        layout.addWidget(open_button)

        # Здесь инициализируем list_widget
        self.list_widget = list_widget

        dialog.exec_()

    def open_selected_bookmark(self):
        # Заменяем list_widget на self.list_widget
        selected_item = self.list_widget.currentItem()
        if selected_item:
            selected_url = selected_item.text()
            try:
                self.add_new_tab(QUrl(selected_url))
            except Exception as e:
                QMessageBox.warning(self, 'Ошибка', f'Не удалось открыть закладку:\n\n{str(e)}')

    def load_bookmarks(self):
        settings = QSettings("WebDonutBrowser", "Bookmarks")
        self.bookmarks = settings.value("bookmarks", [])

    def open_external_page(self):
        external_url, ok = QInputDialog.getText(self, 'Открыть внешнюю страницу', 'Введите URL:')
        if ok:
            external_browser = QWebEngineView()
            external_browser.setUrl(QUrl(external_url))
            external_browser.show()

    def set_theme(self, stylesheet):
        self.setStyleSheet(stylesheet)
        # Сохранение текущей темы в настройках
        settings = QSettings("WebDonutBrowser", "Settings")
        settings.setValue("theme", stylesheet)

    def load_theme(self):
        # Загрузка текущей темы из настроек
        settings = QSettings("WebDonutBrowser", "Settings")
        theme = settings.value("theme", '')
        if theme:
            self.set_theme(theme)

    def update_urlbar(self, qurl, browser=None):
        if browser != self.current_tab():
            return

        self.url_bar.setText(qurl.toString())
        self.url_bar.setCursorPosition(0)

    def closeEvent(self, event):
        try:
            # Переопределение closeEvent для сохранения закладок перед закрытием приложения
            self.save_bookmarks()
            event.accept()
        except Exception as e:
            print(f"An error occurred during closeEvent: {e}")
            traceback.print_exc()
            QMessageBox.critical(self, 'Error', f'An error occurred during closeEvent: {e}')
            event.ignore()

    def save_bookmarks(self):
        settings = QSettings("WebDonutBrowser", "Bookmarks")
        settings.setValue("bookmarks", self.bookmarks)


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('donut.png'))
    QApplication.setApplicationName("WebDonut Browser")
    window = WebDonutBrowser()
    window.show()
    
    app.exec_()

