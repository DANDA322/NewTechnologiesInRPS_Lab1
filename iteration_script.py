import pandas as pd

CSV_FILE_NAME = "dataset_copy_random/dataset_copy_random_annotations.csv"
CLASS_LABEL = 'cat'


def get_next_instance(class_label, start_index=0):
    """

    :param class_label: Метка класса
    :param start_index: Индекс картинки
    :return: Файл
    """
    # Чтение данных из файла
    df = pd.read_csv(CSV_FILE_NAME, encoding='cp1251')

    # Фильтрация данных по метке класса
    class_df = df[df['class_label'] == class_label]

    # Проверка, есть ли экземпляры класса
    if class_df.empty:
        return None

    # Проверка, что не вышли за пределы индексов
    if start_index >= len(class_df):
        return None

    # Получаем следующий экземпляр и возвращаем файл
    next_instance = class_df.iloc[start_index]
    return open(next_instance['absolute_path'])


if __name__ == "__main__":

    for i in range(10):

        # Вызов функции для получения следующей картинки
        next_instance = get_next_instance(CLASS_LABEL, i)

        if next_instance is not None:
            print(f'Следующий экземпляр класса "{CLASS_LABEL}" по пути: {next_instance}')
            next_instance.close()
        else:
            print(f'Экземпляры класса "{CLASS_LABEL}" закончились.')
