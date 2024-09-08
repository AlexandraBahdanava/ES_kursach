import React, { useState } from 'react';
import './LoadingPage.css'; // Подключение CSS стилей

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [result, setResult] = useState(null);

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
        setResult(`Предсказание: ${data.prediction}, Уверенность: ${data.confidence}`);
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
        {!result ? (
          <>
            <p>Загрузите изображение для проверки</p>
            <input type="file" accept="image/*" onChange={handleImageUpload} />
            <button onClick={handleCheckImage}>Проверить изображение</button>
          </>
        ) : (
          <p>{result}</p>
        )}
      </main>

      <footer className="App-footer">
        <p>Footer content</p>
      </footer>
    </div>
  );
}

export default App;
