import csv
import os
import shutil

from annotation import Create_annotation_file

OUTPUT_FOLDER = "dataset_copy"
CSV_FILE_NAME = "dataset_copy_annotations.csv"
DATASET_FOLDER = "dataset"


def copy_and_rename_dataset(dataset_folder, output_folder):
    """
    Копирует файлы из датасета в другую директорию, переименовывая их и создает файл аннотацию.

    :param dataset_folder: Путь к папке с датасетом
    :param output_folder: Путь куда будет скопирован датасет
    :return:
    """

    # Создаем CSV-файл для аннотаций
    annotation_file = os.path.join(output_folder, CSV_FILE_NAME)
    with open(annotation_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['absolute_path', 'relative_path', 'class_label'])

        # Проходим по всем файлам в датасете
        for root, _, files in os.walk(dataset_folder):
            for file_index, file in enumerate(files):
                # Получаем путь к файлу
                path = os.path.join(root, file)

                # Получаем метку класса (имя папки)
                class_label = os.path.basename(root)

                # Создаем новое имя файла с меткой класса и порядковым номером
                new_filename = f"{class_label}_{str(file_index).zfill(4)}{os.path.splitext(file)[-1]}"

                # Полный путь к новому файлу в выходной директории
                new_file_path = os.path.join(output_folder, new_filename)

                # Копируем файл и переименовываем
                shutil.copy(path, new_file_path)

                # Получаем абсолютный путь к новому файлу
                absolute_path = os.path.abspath(new_file_path)

                # Записываем информацию о файле в CSV-файл
                relative_path = os.path.relpath(new_file_path, start=output_folder)
                csv_writer.writerow([absolute_path, new_file_path, class_label])


if __name__ == "__main__":

    # Создаем директорию для копирования файлов, если она не существует
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Вызываем функцию для копирования и переименования датасета
    copy_and_rename_dataset(DATASET_FOLDER, OUTPUT_FOLDER)

    print(f"Датасет успешно скопирован и переименован в {OUTPUT_FOLDER}")

    print(f"Файл-аннотация создан: {CSV_FILE_NAME}")
