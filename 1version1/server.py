from flask import Flask, request, jsonify
from fastai.vision.all import *
from pathlib import Path
import os
import torch

app = Flask(__name__)

def label_func(x):
    return x.parent.name

# Загрузка обученной модели
model_path = Path('training_data/export.pkl')
learn = load_learner(model_path)

# Функция для проверки изображения
def check_image_authenticity(image):
    # Предсказание с помощью модели
    prediction, _, probs = learn.predict(image)
    return str(prediction), probs.max().item()  # возвращаем предсказание и вероятность

@app.route('/check_image', methods=['POST'])
def check_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    # Получаем загруженное изображение
    image_file = request.files['image']
    image_path = os.path.join('uploads', image_file.filename)
    image_file.save(image_path)
    
    # Загружаем изображение для обработки
    img = PILImage.create(image_path)
    
    # Проверка изображения
    prediction, confidence = check_image_authenticity(img)
    
    # Возвращаем результат клиенту
    return jsonify({"prediction": prediction, "confidence": confidence})

if __name__ == '__main__':
    app.run(debug=True)
