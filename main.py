import os

# Создаем папку "dataset" и подпапки "cat" и "dog"
if not os.path.exists("dataset"):
    os.mkdir("dataset")
if not os.path.exists("dataset/cat"):
    os.mkdir("dataset/cat")
if not os.path.exists("dataset/dog"):
    os.mkdir("dataset/dog")
