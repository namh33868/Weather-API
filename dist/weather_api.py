from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Weather VN API", version="1.0")

# CORS cho frontend khác
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class WeatherResponse(BaseModel):
    city: str
    country: str
    temp: float
    wind_speed: float
    condition: str
    timestamp: str

# Tọa độ cities VN
VN_CITIES = {
    "Hanoi": (21.0285, 105.8542),
    "Saigon": (10.8231, 106.6297),
    "Danang": (16.0471, 108.2062),
    "Hue": (16.4637, 107.5909),
    "Haiphong": (20.8449, 106.6881),
    "Cantho": (10.0341, 105.7221)
}

def get_condition(temp):
    """Xác định điều kiện thời tiết."""
    if temp < 20:
        return "Lạnh ❄️"
    elif temp > 30:
        return "Nóng ☀️"
    else:
        return "Mát mẻ 🌤️"

@app.get("/")
def root():
    return {
        "message": "Weather VN API - GET /weather/{city}",
        "cities": list(VN_CITIES.keys())
    }

@app.get("/weather/{city}", response_model=WeatherResponse)
async def get_weather(city: str):
    """Lấy thời tiết từ Open-Meteo."""
    city_cap = city.capitalize()
    
    if city_cap not in VN_CITIES:
        raise HTTPException(404, f"City '{city}' không hỗ trợ. Thử: {', '.join(VN_CITIES.keys())}")
    
    lat, lon = VN_CITIES[city_cap]
    
    try:
        # Open-Meteo API
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=Asia/Bangkok"
        res = requests.get(url, timeout=10)
        data = res.json()
        
        current = data["current_weather"]
        temp = current["temperature"]
        
        return WeatherResponse(
            city=city_cap,
            country="Vietnam",
            temp=round(temp, 1),
            wind_speed=round(current["windspeed"], 1),
            condition=get_condition(temp),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(500, f"Lỗi API: {str(e)}")

@app.get("/cities")
async def list_cities():
    """Danh sách cities hỗ trợ."""
    return {"cities": list(VN_CITIES.keys())}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
