from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Загрузка модели
model = load_model('trained_model.h5')

@app.route('/check_image', methods=['POST'])
def check_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    
    # Открытие изображения
    image = Image.open(io.BytesIO(file.read()))

    # Предварительная обработка изображения (если требуется)
    image = image.resize((224, 224))  # Измените размер, чтобы соответствовать входному размеру модели
    image_array = np.array(image)
    image_array = np.expand_dims(image_array, axis=0)  # Добавляем измерение для батча
    
    # Нормализация (если ваша модель требует этого)
    image_array = image_array / 255.0  # Приведение к диапазону [0, 1] если модель обучена на нормализованных данных

    # Прогнозирование с помощью модели
    predictions = model.predict(image_array)

    # Получаем предсказание и уверенность
    predicted_class = np.argmax(predictions, axis=1)[0]  # Класс с максимальной вероятностью
    confidence = np.max(predictions)  # Уровень уверенности

    return jsonify({'prediction': str(predicted_class), 'confidence': float(confidence)})

if __name__ == '__main__':
    app.run(debug=True)
