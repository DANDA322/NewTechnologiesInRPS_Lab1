import random

import pandas as pd
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_image_size(file_path):
    try:
        with Image.open(file_path) as img:
            width, height = img.size
            channels = len(img.getbands())
            return height, width, channels
    except Exception as e:
        print(f"Error reading image at {file_path}: {e}")
        return None, None, None


def filter_dataframe_by_label(dataframe, target_label):
    """
    Функция для фильтрации DataFrame по заданной метке класса
    """

    # Фильтрация по заданной метке класса
    filtered_df = dataframe[dataframe['class_label'] == target_label]
    return filtered_df


def filter_dataframe_by_parameters(dataframe, target_label, max_width, max_height):
    """
    Функция для фильтрации DataFrame по заданным параметрам
    """

    # Фильтрация по заданным параметрам
    filtered_df = dataframe[(dataframe['class_label'] == target_label) &
                            (dataframe['width'] <= max_width) &
                            (dataframe['height'] <= max_height)]

    return filtered_df


def count_pixels(file_path):
    """
    Функция для подсчета количества пикселей в изображении
    """
    try:
        img = cv2.imread(file_path)
        if img is not None:
            return img.size
        else:
            return None
    except Exception as e:
        print(f"Error counting pixels for image at {file_path}: {e}")
        return None

def show_images(image_paths):
    print(len(image_paths))
    fig, axes = plt.subplots(1, len(image_paths), figsize=(15, 5))
    for i, value in enumerate(image_paths):
        img = cv2.imread(value)
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        axes[i].imshow(img2)
        axes[i].set_title(i)
        axes[i].axis('off')
    plt.show()


def plot_histogram(dataframe, target_label):
    """
    Строит гистограмму для случайного изображения из DataFrame по заданной метке класса.

    Возвращает:
    - hist_channels: list, список массивов значений гистограммы для каждого канала.
    """

    # Выбор случайного изображения из заданного класса
    random_image_path = dataframe[dataframe['label'] == target_label].sample(1)['absolute_path'].iloc[0]

    print(random_image_path)

    # Загрузка изображения с использованием OpenCV
    img = cv2.imread(random_image_path)

    # Преобразование изображения из BGR в RGB (для правильного отображения в matplotlib)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Разделение изображения на отдельные каналы
    channels = cv2.split(img_rgb)

    # Строим гистограмму для каждого канала
    hist_channels = []
    for channel in channels:
        hist = cv2.calcHist([channel], [0], None, [256], [0, 256])
        hist_channels.append(hist)

    # Отображение изображения и гистограммы
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.title('Изображение')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        plt.plot(hist_channels[i], color=color)
    plt.title('Гистограмма по каналам')
    plt.xlabel('Значение пикселя')
    plt.ylabel('Частота')

    plt.show()

    return hist_channels


def plot_channel_histogram(channels):
    # Строим гистограмму для каждого канала
    hist_channels = []
    for channel in channels:
        hist = cv2.calcHist([channel], [0], None, [256], [0, 256])
        hist_channels.append(hist)

    # Отображение гистограммы
    plt.figure(figsize=(12, 6))

    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        plt.plot(hist_channels[i], color=color, label=f'Channel {i}')

    plt.title('Гистограмма цветовых каналов')
    plt.xlabel('Значение пикселя')
    plt.ylabel('Частота')
    plt.legend()
    plt.show()

    return hist_channels


def test():
    # 1
    print(1)
    csv_file_path = 'dataset/annotation.csv'
    df = pd.read_csv(csv_file_path, encoding='cp1251')
    df = df[['class_label', 'absolute_path']]
    print(df)

    # 3
    print(3)
    class_mapping = {'cat': 0, 'dog': 1}
    df['label'] = df['class_label'].map(class_mapping).astype('category')
    print(df.head())

    # 4
    print(4)
    df[['height', 'width', 'channels']] = df['absolute_path'].apply(get_image_size).apply(pd.Series)
    print(df[['absolute_path', 'height', 'width', 'channels']])

    # 5
    # Статистика для столбцов с размерами изображений
    print(5)
    image_size_stats = df[['height', 'width', 'channels']].describe()
    print("Статистика для размеров изображений:")
    print(image_size_stats)

    # Статистика для столбца с метками классов
    class_label_stats = df['label'].describe()

    # Табличка с суммой по метке
    class_label_counts = df['label'].value_counts()

    plt.figure(figsize=(8, 6))
    class_label_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title('Распределение меток классов')
    plt.show()

    print("Статистика для столбца с метками классов:")
    print(class_label_stats)
    print("\nТабличка с суммой по метке:")
    print(class_label_counts)

    # 6
    print("\n6. Фильтрация по метке")
    target_label = 'cat'
    filtered_df = filter_dataframe_by_label(df, target_label)
    print(filtered_df)

    # 7
    print("\n7. Фильтрация по метке и размеру")
    max_width = 450
    max_height = 450
    filtered_df2 = filter_dataframe_by_parameters(df, target_label, max_width, max_height)
    print(filtered_df2.head())

    # 8
    print("\n8. Вычисление количества пикселей и группировка")
    # Добавление нового столбца с количеством пикселей
    df['pixel_count'] = df['absolute_path'].apply(count_pixels)
    print(df)
    # Группировка DataFrame по метке класса
    grouped_df = df.groupby('label')['pixel_count'].agg(['min', 'max', 'mean'])
    print(grouped_df)




    # Выберем случайные изображения из каждой группы
    selected_images = []

    for i in range(5):
        group_images = df[df['class_label'] == target_label]['absolute_path'].tolist()
        print(group_images)
        selected_image = random.choice(group_images)
        selected_images.append(selected_image)

    # Отобразим выбранные изображения
    show_images(selected_images)


    # 9
    print("\n9. Строим гистограмму")
    print(df)
    target_label = 0
    channels = plot_histogram(df, target_label)

    hist = plot_channel_histogram(channels)


if __name__ == "__main__":
    test()
