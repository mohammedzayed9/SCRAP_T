import sys
import csv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QRadioButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QLabel, QPushButton, QFileDialog
import requests
from bs4 import BeautifulSoup

class ScraperWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)

        self.links_radio = QRadioButton("Links")
        self.links_radio.setChecked(True)
        self.images_radio = QRadioButton("Images")

        self.url_label = QLabel("URL:")
        self.url_text = QTextEdit()
        self.url_text.setFixedHeight(30)

        self.scrape_button = QPushButton("Scrape")
        self.scrape_button.clicked.connect(self.scrape)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)

        radio_layout = QHBoxLayout()
        radio_layout.addWidget(self.links_radio)
        radio_layout.addWidget(self.images_radio)

        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_label)
        url_layout.addWidget(self.url_text)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.scrape_button)
        button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(radio_layout)
        main_layout.addLayout(url_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.text_edit)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("Web Scraper")

    def scrape(self):
        url = self.url_text.toPlainText().strip()
        if url:
            try:
                res = requests.get(url)
                soup = BeautifulSoup(res.text, 'html.parser')
                if self.links_radio.isChecked():
                    links = [link.get('href') for link in soup.find_all('a')]
                    self.text_edit.setText("\n".join(links))
                elif self.images_radio.isChecked():
                    images = [img.get('src') for img in soup.find_all('img')]
                    self.text_edit.setText("\n".join(images))
            except:
                self.text_edit.setText("An error occurred while scraping the URL.")
        else:
            self.text_edit.setText("Please enter a valid URL.")

    def save(self):
        scraped_data = self.text_edit.toPlainText().strip().split("\n")
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", ".", "CSV Files (*.csv)")
        if filename:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                for data in scraped_data:
                    writer.writerow([data])


app = QApplication(sys.argv)
window = ScraperWindow()
window.show()
sys.exit(app.exec_())
