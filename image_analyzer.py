import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, \
    QTableWidgetItem, QFileDialog, QLineEdit, QLabel, QDialog
import pandas as pd
import random

import analysis


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.df = pd.DataFrame()  # Инициализация пустого DataFrame
        self.df2 = pd.DataFrame()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Dataset Manipulation")
        self.setGeometry(100, 100, 800, 600)

        # Создание кнопок
        loadButton = QPushButton('Загрузить CSV')
        loadButton.clicked.connect(self.loadCsv)

        mapButton = QPushButton('Мапинг лейблов')
        mapButton.clicked.connect(self.mapLabels)

        addButton = QPushButton('Добавление размеров изображений')
        addButton.clicked.connect(self.addImageSize)

        # Создание таблицы
        self.tableWidget = QTableWidget()
        self.tableWidget2 = QTableWidget()

        # Расположение виджетов
        layout = QVBoxLayout()
        layout.addWidget(loadButton)
        layout.addWidget(mapButton)
        layout.addWidget(addButton)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.tableWidget2)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        statsButton = QPushButton('Статистика')
        statsButton.clicked.connect(self.showStatistics)

        filterLabelButton = QPushButton('Фильтр по метке')
        filterLabelButton.clicked.connect(self.filterByLabel)

        filterParametersButton = QPushButton('Фильтр по метке и размеру')
        filterParametersButton.clicked.connect(self.filterByParameters)

        countPixelButton = QPushButton('Подсчет количества пикселей')
        countPixelButton.clicked.connect(self.countPixels)

        showImagesButton = QPushButton('Показать случайные картинки')
        showImagesButton.clicked.connect(self.showImages)

        plotHistButton = QPushButton('Отрисовать гистограмму по каналам')
        plotHistButton.clicked.connect(self.plotHistogram)

        self.labelInput = QLineEdit()
        self.maxWidthInput = QLineEdit()
        self.maxHeightInput = QLineEdit()

        # Добавление новых виджетов в layout
        layout = self.centralWidget().layout()
        layout.addWidget(statsButton)
        layout.addWidget(filterLabelButton)
        layout.addWidget(self.labelInput)
        layout.addWidget(filterParametersButton)
        layout.addWidget(QLabel("Макс. ширина:"))
        layout.addWidget(self.maxWidthInput)
        layout.addWidget(QLabel("Макс. высота:"))
        layout.addWidget(self.maxHeightInput)
        layout.addWidget(countPixelButton)
        layout.addWidget(showImagesButton)
        layout.addWidget(plotHistButton)

    def loadCsv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите CSV файл", "", "CSV Files (*.csv)")
        if file_path:
            self.df = analysis.get_df(file_path)
            self.updateTable()

    def mapLabels(self):
        if not self.df.empty:
            class_mapping = {'cat': 0, 'dog': 1}  # Пример мапинга
            self.df = analysis.class_mapping_df(self.df, class_mapping)
            self.updateTable()

    def addImageSize(self):
        if not self.df.empty:
            self.df[['height', 'width', 'channels']] = self.df['absolute_path'].apply(analysis.get_image_size).apply(
                pd.Series)
            self.updateTable()

    def updateTable(self):
        self.tableWidget.setRowCount(self.df.shape[0])
        self.tableWidget.setColumnCount(self.df.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(self.df.columns)

        for i in range(self.df.shape[0]):
            for j in range(self.df.shape[1]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.df.iat[i, j])))

    def updateTable2(self):
        self.tableWidget2.setRowCount(self.df2.shape[0])
        self.tableWidget2.setColumnCount(self.df2.shape[1])
        self.tableWidget2.setHorizontalHeaderLabels(self.df2.columns)

        for i in range(self.df2.shape[0]):
            for j in range(self.df2.shape[1]):
                self.tableWidget2.setItem(i, j, QTableWidgetItem(str(self.df2.iat[i, j])))

    def showStatistics(self):
        if not self.df.empty:
            self.df2 = analysis.get_statistics(self.df)
            self.updateTable2()

    def filterByLabel(self):
        if not self.df.empty:
            target_label = self.labelInput.text()
            self.df = analysis.filter_dataframe_by_label(self.df, target_label)
            self.updateTable()

    def filterByParameters(self):
        if not self.df.empty:
            target_label = self.labelInput.text()
            max_width = int(self.maxWidthInput.text())
            max_height = int(self.maxHeightInput.text())
            self.df = analysis.filter_dataframe_by_parameters(self.df, target_label, max_width, max_height)
            self.updateTable()

    def countPixels(self):
        if not self.df.empty:
            self.df['pixel_count'] = self.df['absolute_path'].apply(analysis.count_pixels)
            self.updateTable()
            # Группировка DataFrame по метке класса
            self.df2 = self.df.groupby('label')['pixel_count'].agg(['min', 'max', 'mean'])
            self.updateTable2()

    def showImages(self):
        if not self.df.empty:
            selected_images = []
            target_label = self.labelInput.text()
            for i in range(5):
                group_images = self.df[self.df['class_label'] == target_label]['absolute_path'].tolist()
                selected_image = random.choice(group_images)
                selected_images.append(selected_image)
            analysis.show_images(selected_images)

    def plotHistogram(self):
        target_label = 0
        channels = analysis.plot_histogram(self.df, target_label)
        hist = analysis.plot_channel_histogram(channels)


# Запуск приложения
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
sys.exit(app.exec())
