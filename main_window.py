import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget
from PyQt6.QtGui import QPixmap
from annotation import create_annotation_file
from copy_dataset1 import copy_and_rename_dataset
from copy_dataset_random import copy_and_rename_dataset_with_annotation
from iterator import InstancesIterator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dataset Manager")
        self.setGeometry(100, 100, 800, 600)
        self.folder_path = None
        self.cat_iterator = None
        self.dog_iterator = None
        self.annotation_file = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Выберите папку с датасетом")
        layout.addWidget(self.label)
        self.create_button(layout, "Выбрать папку с датасетом", self.select_folder)
        self.create_button(layout, "Создать файл-аннотацию", self.create_annotation)
        self.create_button(layout, "Скопировать датасет и создать аннотацию", self.copy_and_rename)
        self.create_button(layout, "Скопировать датасет и рандомизировать названия и создать аннотацию", self.copy_and_random)
        self.create_button(layout, "Следующая кошка", self.show_next_cat)
        self.create_button(layout, "Следующая собака", self.show_next_dog)
        self.create_button(layout, "Reset Dataset", self.reset_dataset)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def create_button(self, layout, text, handler):
        button = QPushButton(text)
        button.clicked.connect(handler)
        layout.addWidget(button)

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
        self.show_next("cat", "Коты в датасете закончились!")

    def show_next_dog(self):
        self.show_next("dog", "Собаки в датасете закончились!")

    def show_next(self, animal_type, end_message):
        if not self.annotation_file:
            self.annotation_file, _ = QFileDialog.getOpenFileName(self, "Select Annotation CSV File", "", "CSV Files (*.csv)")
            if not self.annotation_file:
                self.label.setText("Выберите CSV файл-аннотацию!")
                return

        if animal_type == "cat":
            iterator = self.cat_iterator
        else:
            iterator = self.dog_iterator

        if not iterator:
            iterator = InstancesIterator(self.annotation_file, animal_type)

        try:
            next_file_path = next(iterator)
            pixmap = QPixmap(next_file_path)
            self.label.setPixmap(pixmap)
            if animal_type == "cat":
                self.cat_iterator = iterator
            else:
                self.dog_iterator = iterator
        except StopIteration:
            self.label.setText(end_message)

    def reset_dataset(self):
        self.annotation_file = None
        self.cat_iterator = None
        self.dog_iterator = None
        self.label.setText("Датасет очищен. Выберите новый CSV файл-аннотацию.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
