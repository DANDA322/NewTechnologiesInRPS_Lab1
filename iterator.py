import pandas as pd

CSV_FILE_NAME = "dataset_copy_random/dataset_copy_random_annotations.csv"
CLASS_LABEL = 'cat'


class InstancesIterator:
    def __init__(self, csv_file_path, class_label):
        self.df = pd.read_csv(csv_file_path, encoding='cp1251')
        self.class_label = class_label
        self.class_df = self.df[self.df['class_label'] == class_label]
        self.current_instance_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_instance_index >= len(self.class_df):
            raise StopIteration

        instance = self.class_df.iloc[self.current_instance_index]
        self.current_instance_index += 1

        # return open(instance['absolute_path'])
        return instance['absolute_path']


if __name__ == "__main__":
    class_instances_iter = InstancesIterator(CSV_FILE_NAME, CLASS_LABEL)

    for file in class_instances_iter:
        print(f'Следующий экземпляр по пути: {file}')
        file.close()

