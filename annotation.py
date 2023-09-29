import os
import csv


# Функция для создания CSV-файла с аннотациями
def create_annotation_file(dataset_folder, output_file):
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

                # Получаем метку класса (в данном примере используется имя папки)
                class_label = os.path.basename(root)

                # Записываем информацию о файле в CSV-файл
                csv_writer.writerow([absolute_path, relative_path, class_label])


if __name__ == "__main__":
    # Задайте путь к папке с вашим датасетом
    dataset_folder = 'dataset'

    # Задайте имя и путь для создания CSV-файла
    output_file = 'dataset_annotations.csv'

    # Вызываем функцию для создания аннотаций
    create_annotation_file(dataset_folder, output_file)

    print(f"CSV-файл с аннотациями создан: {output_file}")
