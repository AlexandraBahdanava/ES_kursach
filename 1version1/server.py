import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from pathlib import Path
from PIL import Image
import imghdr

# Устанавливаем путь к папке с изображениями
data_path = Path('C:/Users/bahda/Downloads/archive/Real_AI_SD_LD_Dataset/train')  # Замените на фактический путь

# Пример функции для преобразования изображений в формат RGBA (если требуется)
def convert_to_rgba(image_path):
    try:
        image_type = imghdr.what(image_path)
        if image_type is not None:
            image = Image.open(image_path)
            rgba_image = image.convert("RGBA")
            filename_without_extension = os.path.splitext(image_path)[0]
            rgba_image.save(f"{filename_without_extension}.png", quality=95)
            print(f"Изображение {image_path} успешно преобразовано в формат RGBA и сохранено в формате PNG")
        else:
            print(f"Файл {image_path} не является изображением")
    except Exception as e:
        print(f"Ошибка при обработке изображения {image_path}: {e}")

# Подготовка данных с использованием ImageDataGenerator
batch_size = 32
img_height = 224
img_width = 224

# Создаем генератор данных для аугментации и загрузки изображений
datagen = ImageDataGenerator(
    rescale=1./255,             # Масштабируем изображения
    validation_split=0.2,       # 20% изображений для валидации
    rotation_range=20,          # Вращение изображений для аугментации
    width_shift_range=0.2,      # Сдвиг по ширине
    height_shift_range=0.2,     # Сдвиг по высоте
    shear_range=0.2,            # Сдвиг изображения
    zoom_range=0.2,             # Увеличение изображения
    horizontal_flip=True,       # Горизонтальное отражение
    fill_mode='nearest'         # Заполнение пустых пикселей
)

# Подготовка данных для обучения и валидации
train_data_gen = datagen.flow_from_directory(
    directory=str(data_path),
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'  # Используем часть данных для тренировки
)

val_data_gen = datagen.flow_from_directory(
    directory=str(data_path),
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'  # Используем часть данных для валидации
)

# Создание модели на базе Keras (пример CNN)
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(train_data_gen.num_classes, activation='softmax')  # Количество классов, найденных генератором
])

# Компилируем модель
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Обучение модели
epochs = 10
history = model.fit(
    train_data_gen,
    validation_data=val_data_gen,
    epochs=epochs
)

# Сохранение обученной модели
model.save('trained_model.h5')

# Вывод графиков обучения
import matplotlib.pyplot as plt

# График потерь
plt.plot(history.history['loss'], label='training_loss')
plt.plot(history.history['val_loss'], label='validation_loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()

# График точности
plt.plot(history.history['accuracy'], label='training_accuracy')
plt.plot(history.history['val_accuracy'], label='validation_accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()
plt.show()
