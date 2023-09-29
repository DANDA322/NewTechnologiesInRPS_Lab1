import os
import csv


# Функция для создания CSV-файла с аннотациями
def create_annotation_file(dataset_folder, output_file):
    """

    :param dataset_folder: Путь к папке с датасетом
    :param output_file:  Имя и путь для создания CSV-файла
    :return: В результате выполнения функции создается CSV-файл с аннотацией
    """

    # Открываем CSV-файл для записи
    with open(output_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Записываем заголовки столбцов
        csv_writer.writerow(['absolute_path', 'relative_path', 'class_label'])

        # Проходим по всем файлам в датасете
        for root, _, files in os.walk(dataset_folder):
            for file in files:
                # Получаем абсолютный путь к файлу
                absolute_path = os.path.abspath(file)

                # Получаем относительный путь относительно вашего Python-проекта
                relative_path = os.path.join(root, file)

                # Получаем метку класса (имя папки)
                class_label = os.path.basename(root)

                # Записываем информацию о файле в CSV-файл
                csv_writer.writerow([absolute_path, relative_path, class_label])


if __name__ == "__main__":
    # Путь к папке с датасетом
    dataset_folder = 'dataset'

    # Имя и путь для создания CSV-файла
    output_file = 'dataset_annotations.csv'

    # Создаем аннотацию
    create_annotation_file(dataset_folder, output_file)

    print(f"CSV-файл с аннотациями создан: {output_file}")
