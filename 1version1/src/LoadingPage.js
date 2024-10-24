import React, { useState, useRef } from 'react';
import './LoadingPage.css'; // Подключение CSS стилей

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null); // Реф для доступа к полю загрузки

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    setSelectedImage(file);
  };

  const handleCheckImage = async () => {
    if (selectedImage) {
      const formData = new FormData();
      formData.append('image', selectedImage);

      try {
        const response = await fetch('http://localhost:5000/check_image', {
          method: 'POST',
          body: formData,
        });
        const data = await response.json();

        // Определение текста предсказания на основе числа
        let predictionText;
        if (data.prediction === '0') {
          predictionText = 'Искусственный интеллект';
        } else if (data.prediction === '1') {
          predictionText = 'Не искусственный интеллект';
        } else {
          predictionText = 'Неизвестно';
        }

        setResult(`Предсказание: ${predictionText}, Уверенность: ${data.confidence.toFixed(2)}`);
        setSelectedImage(null); // Сброс выбранного изображения
        fileInputRef.current.value = ''; // Очистка поля выбора файла
      } catch (error) {
        console.error('Ошибка при проверке изображения:', error);
        setResult('Ошибка при проверке изображения');
      }
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src="logo.png" alt="Logo" className="App-logo" />
      </header>

      <main className="App-main">
        <p>Загрузите изображение для проверки</p>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          ref={fileInputRef} // Привязываем реф к полю загрузки
        />
        <button onClick={handleCheckImage}>Проверить изображение</button>

        {result && <p>{result}</p>}
      </main>

      <footer className="App-footer">
        <p>Footer content</p>
      </footer>
    </div>
  );
}

export default App;
