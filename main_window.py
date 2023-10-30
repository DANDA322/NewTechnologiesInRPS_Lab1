import os

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget
from PyQt6.QtGui import QPixmap, QImage
import sys

# Importing necessary functions from provided scripts
from annotation import create_annotation_file
from copy_dataset1 import copy_and_rename_dataset
from copy_dataset_random import copy_and_rename_dataset_with_annotation
from iterator import InstancesIterator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dataset Manager")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel("Выберите папку с датасетом")
        layout.addWidget(self.label)

        self.select_folder_btn = QPushButton("Выбрать папку с датасетом")
        self.select_folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_btn)

        self.create_annotation_btn = QPushButton("Создать файл-аннотацию")
        self.create_annotation_btn.clicked.connect(self.create_annotation)
        layout.addWidget(self.create_annotation_btn)

        self.copy_and_rename_btn = QPushButton("Скопировать датасет и создать аннотацию")
        self.copy_and_rename_btn.clicked.connect(self.copy_and_rename)
        layout.addWidget(self.copy_and_rename_btn)

        self.copy_and_random_btn = QPushButton("Скопировать датасет и рандомизировать названия и создать аннотацию")
        self.copy_and_random_btn.clicked.connect(self.copy_and_random)
        layout.addWidget(self.copy_and_random_btn)

        self.next_cat_btn = QPushButton("Следующая кошка")
        self.next_cat_btn.clicked.connect(self.show_next_cat)
        layout.addWidget(self.next_cat_btn)

        self.next_dog_btn = QPushButton("Следующая собака")
        self.next_dog_btn.clicked.connect(self.show_next_dog)
        layout.addWidget(self.next_dog_btn)

        self.reset_dataset_btn = QPushButton("Reset Dataset")
        self.reset_dataset_btn.clicked.connect(self.reset_dataset)
        layout.addWidget(self.reset_dataset_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.folder_path = None
        self.cat_iterator = None
        self.dog_iterator = None
        self.annotation_file = None

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, 'Выберите папку с датасетом')
        self.label.setText(f"Выберите папку с датасетом: {self.folder_path}")

    def create_annotation(self):
        if self.folder_path:
            out_path = QFileDialog.getExistingDirectory(self, 'Выберите папку куда сохранить файл')
            out_path = os.path.join(out_path, 'annotation.csv')
            create_annotation_file(os.path.basename(self.folder_path), out_path)
            self.label.setText(f"Файл-аннотация создан: {out_path}")
        else:
            self.label.setText("Сначала выберите директорию с датасетом!")

    def copy_and_rename(self):
        if self.folder_path:
            out_path = QFileDialog.getExistingDirectory(self, 'Выберите папку куда сохранить датасет')
            copy_and_rename_dataset(os.path.basename(self.folder_path), os.path.basename(out_path))
            self.label.setText(f"Датасет скопирован и файл аннотация создан")
        else:
            self.label.setText("Сначала выберите директорию с датасетом!")

    def copy_and_random(self):
        if self.folder_path:
            out_path = QFileDialog.getExistingDirectory(self, 'Выберите папку куда сохранить датасет')
            copy_and_rename_dataset_with_annotation(os.path.basename(self.folder_path), os.path.basename(out_path))
            self.label.setText(f"Датасет скопирован и файл аннотация создан")
        else:
            self.label.setText("Сначала выберите директорию с датасетом!")

    def show_next_cat(self):
        if not self.annotation_file:
            self.annotation_file, _ = QFileDialog.getOpenFileName(self, "Select Annotation CSV File", "",
                                                                  "CSV Files (*.csv)")
            if not self.annotation_file:  # Если файл не был выбран
                self.label.setText("Выберите CSV файл-аннотацию!")
                return

        if not self.cat_iterator:
            self.cat_iterator = InstancesIterator(self.annotation_file, "cat")
        try:
            next_cat_file_path = next(self.cat_iterator)
            pixmap = QPixmap(next_cat_file_path)
            self.label.setPixmap(pixmap)
        except StopIteration:
            self.label.setText("Коты в датасете закончились!")

    def show_next_dog(self):
        if not self.annotation_file:
            self.annotation_file, _ = QFileDialog.getOpenFileName(self, "Select Annotation CSV File", "",
                                                                  "CSV Files (*.csv)")
            if not self.annotation_file:  # Если файл не был выбран
                self.label.setText("Выберите CSV файл-аннотацию!")
                return

        if not self.dog_iterator:
            self.dog_iterator = InstancesIterator(self.annotation_file, "dog")
        try:
            next_cat_file_path = next(self.dog_iterator)
            pixmap = QPixmap(next_cat_file_path)
            self.label.setPixmap(pixmap)
        except StopIteration:
            self.label.setText("Собаки в датасете закончились!")

    def reset_dataset(self):
        self.annotation_file = None
        self.cat_iterator = None
        self.dog_iterator = None
        self.label.setText("Датасет очищен. Выберите новый CSV файл-аннотацию.")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
