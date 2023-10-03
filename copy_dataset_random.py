import os
import random
import shutil
import csv

OUTPUT_FOLDER = "dataset_copy_random"
CSV_FILE_NAME = "dataset_copy_random_annotations.csv"
DATASET_FOLDER = "dataset"


def copy_and_rename_dataset_with_annotation(dataset_folder, output_folder):
    """
    Копирует файлы из датасета в другую директорию, переименовывая их случайным номером и создает файл аннотацию.

    :param dataset_folder: Путь к папке с датасетом
    :param output_folder: Путь куда будет скопирован датасет
    :return:
    """

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Создаем CSV-файл для аннотаций
    annotation_file = os.path.join(output_folder, CSV_FILE_NAME)
    with open(annotation_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['absolute_path', 'relative_path', 'class_label'])

        for root, _, files in os.walk(dataset_folder):
            for file in files:
                # Получаем путь к файлу
                path = os.path.join(root, file)

                # Получаем метку класса (имя папки)
                class_label = os.path.basename(root)

                random_number = random.randint(0, 10000)

                # Создаем новое имя файла с номером и расширением .jpg
                new_filename = f"{random_number}.jpg"

                # Полный путь к новому файлу в выходной директории
                new_file_path = os.path.join(output_folder, new_filename)

                # Копируем файл и переименовываем
                shutil.copy(path, new_file_path)

                # Получаем абсолютный путь к новому файлу
                absolute_path = os.path.abspath(new_file_path)

                # Записываем информацию о файле в CSV-файл
                csv_writer.writerow([absolute_path, new_file_path, class_label])


if __name__ == "__main__":
    copy_and_rename_dataset_with_annotation(DATASET_FOLDER, OUTPUT_FOLDER)

    print(f"Датасет успешно скопирован и переименован в {OUTPUT_FOLDER}")

    print(f"Файл-аннотация создан: {CSV_FILE_NAME}")
