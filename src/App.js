import React, { useState } from "react";
import axios from "axios";
import WeatherInput from "./components/WeatherInput";
import WeatherInfo from "./components/WeatherInfo";

function App() {
  const [weather, setWeather] = useState(null);
  
  const suggestedCities = [
    "Hanoi",
    "Ho Chi Minh",
    "Da Nang",
    "Hue",
    "Can Tho",
    "Haiphong",
    "Bien Hoa",
    "Dalat",
    "Nha Trang",
    "Vung Tau",
    "Rach Gia",
    "Nam Dinh"
  ];

  const cityDisplayNames = {
    "Hanoi": "Hà Nội",
    "Ho Chi Minh": "Hồ Chí Minh",
    "Da Nang": "Đà Nẵng",
    "Hue": "Huế",
    "Can Tho": "Cần Thơ",
    "Haiphong": "Hải Phòng",
    "Bien Hoa": "Biên Hòa",
    "Dalat": "Đà Lạt",
    "Nha Trang": "Nha Trang",
    "Vung Tau": "Vũng Tàu",
    "Rach Gia": "Rạch Giá",
    "Nam Dinh": "Nam Định"
  };

  const fetchWeather = async (city) => {
    const API_KEY = "0cdff52a42212b1519be63a4817edba5";
    const URL = `https://api.openweathermap.org/data/2.5/weather?q=${city},vn&appid=${API_KEY}&units=metric&lang=vi`;

    try {
      const response = await axios.get(URL);
      setWeather(response.data);
    } catch (error) {
      if (error.response) {
        if (error.response.status === 404) {
          alert("Thành phố không tồn tại. Vui lòng kiểm tra lại.");
        } else if (error.response.status === 401) {
          alert("API Key không hợp lệ. Vui lòng kiểm tra.");
        } else {
          alert("Có lỗi xảy ra: " + error.response.data.message);
        }
      } else if (error.request) {
        alert("Không thể kết nối tới máy chủ. Vui lòng kiểm tra lại kết nối mạng.");
      } else {
        alert("Có lỗi xảy ra khi gửi yêu cầu: " + error.message);
      }
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ textAlign: 'center', color: '#2c3e50' }}>Ứng dụng Thời tiết</h1>
      <WeatherInput fetchWeather={fetchWeather} />
      
      <div style={{ marginTop: '20px' }}>
        <h3 style={{ color: '#34495e' }}>Các thành phố phổ biến:</h3>
        <div style={{ 
          display: 'flex', 
          flexWrap: 'wrap', 
          gap: '10px',
          marginBottom: '20px' 
        }}>
          {suggestedCities.map((city) => (
            <button
              key={city}
              onClick={() => fetchWeather(city)}
              style={{
                padding: '8px 16px',
                border: '1px solid #3498db',
                borderRadius: '20px',
                backgroundColor: '#fff',
                color: '#3498db',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                ':hover': {
                  backgroundColor: '#3498db',
                  color: '#fff'
                }
              }}
            >
              {cityDisplayNames[city]}
            </button>
          ))}
        </div>
      </div>
      
      <WeatherInfo weather={weather} />
    </div>
  );
}

export default App;
