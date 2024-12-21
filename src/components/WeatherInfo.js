import React from "react";

function WeatherInfo({ weather }) {
  if (!weather) {
    return <p>Không có dữ liệu thời tiết.</p>;
  }

  const { name, main, weather: details } = weather;
  return (
    <div>
      <h2>Thời tiết tại {name}</h2>
      <p>Nhiệt độ: {main.temp}°C</p>
      <p>Độ ẩm: {main.humidity}%</p>
      <p>Mô tả: {details[0].description}</p>
    </div>
  );
}

export default WeatherInfo;
