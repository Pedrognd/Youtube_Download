import sys
import yt_dlp
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox, QLabel, QMessageBox
from PySide6.QtCore import Qt

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Video Downloader')
        self.setGeometry(100, 100, 400, 200)

        # Layout
        layout = QVBoxLayout()

        # URL Input
        self.url_label = QLabel('YouTube Video URL:')
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        # Format Selection
        self.format_label = QLabel('Select Format:')
        self.format_combo = QComboBox()
        self.format_combo.addItems(['MP4', 'MP3'])
        layout.addWidget(self.format_label)
        layout.addWidget(self.format_combo)

        # Download Button
        self.download_button = QPushButton('Download')
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def download_video(self):
        url = self.url_input.text().strip()
        format_choice = self.format_combo.currentText()

        if not url:
            QMessageBox.warning(self, 'Input Error', 'Please enter a YouTube video URL.')
            return

        try:
            ydl_opts = {}
            if format_choice == 'MP4':
                ydl_opts = {
                    'format': 'mp4',
                    'outtmpl': '%(title)s.%(ext)s',
                }
            elif format_choice == 'MP3':
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': '%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            QMessageBox.information(self, 'Success', 'Download completed successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Download Error', f'An error occurred: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())