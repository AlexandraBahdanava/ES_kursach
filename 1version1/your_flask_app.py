from flask import Flask, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

app = Flask(__name__)

# Загрузите вашу модель
model = load_model('trained_model.h5')

@app.route('/check_image', methods=['POST'])
def check_image():
    if 'image' not in request.files:
        return jsonify({'error': 'Нет изображения'}), 400
    
    img_file = request.files['image']
    img_path = 'C:/Users/bahda/Downloads/archive/Real_AI_SD_LD_Dataset/train/AI/0-917663-175692.jpg'
    img_file.save(img_path)  # Сохраняем временно загруженное изображение

    # Предобработка изображения
    img = image.load_img(img_path, target_size=(224, 224))  # Убедитесь, что размер соответствует вашему входу модели
    img_array = image.img_to_array(img) / 255.0  # Нормализация
    img_array = np.expand_dims(img_array, axis=0)  # Добавляем размерность для пакета

    # Получаем предсказание
    prediction = model.predict(img_array)
    class_index = np.argmax(prediction, axis=1)[0]
    confidence = prediction[0][class_index]

    # Предположим, что у вас есть словарь классов
    classes = ['AI', 'Not AI']  # Замените на ваши классы
    predicted_class = classes[class_index]

    return jsonify({'prediction': predicted_class, 'confidence': float(confidence)})

if __name__ == '__main__':
    app.run(port=5000)
