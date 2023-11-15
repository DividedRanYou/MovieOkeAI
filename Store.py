# Store.py

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QMenu, QAction
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class CustomWebEngineView(QWebEngineView):
    def contextMenuEvent(self, event):
        pass

class MyWebBrowser:
    def __init__(self):
        test_url = "https://movieokestore.shelldroid.repl.co/Other/Test.html"
        self.URL = "https://movieokestore.shelldroid.repl.co"

        self.window = QWidget()
        self.window.setWindowTitle("MovieOkeStore")
        self.layout = QVBoxLayout(self.window)
        self.horizontal = QHBoxLayout()

        self.browser = CustomWebEngineView()

        self.layout.addLayout(self.horizontal)
        self.layout.addWidget(self.browser)
        self.browser.setUrl(QUrl(f"{self.URL}"))

        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.downloadRequested.connect(self.onDownloadRequested)

        self.window.show()

    def onDownloadRequested(self, download):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath, _ = QFileDialog.getSaveFileName(
            self.window, "Save File", download.url().toString(), "All Files (*);;Text Files (*.txt)", options=options)

        if filePath:
            download.setPath(filePath)
            download.accept()

if __name__ == "__main__":
    app = QApplication([])
    window = MyWebBrowser()
    app.exec_()
