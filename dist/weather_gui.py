import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk, ImageDraw  # type: ignore[reportMissingImports]
import io
import threading
from datetime import datetime

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather VN - Dự báo thời tiết Việt Nam")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Data cache
        self.weather_data = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = tk.Label(self.root, text="🌤️ Thời Tiết Việt Nam", 
                        font=("Arial", 20, "bold"), fg="#2c3e50")
        title.pack(pady=20)
        
        # City input
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        tk.Label(input_frame, text="Thành phố:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.city_var = tk.StringVar(value="Hanoi")
        city_entry = tk.Entry(input_frame, textvariable=self.city_var, font=("Arial", 12), width=15)
        city_entry.pack(side=tk.LEFT, padx=10)
        tk.Button(input_frame, text="Tìm", command=self.get_weather, bg="#3498db", fg="white").pack(side=tk.LEFT)
        
        # Weather display
        self.weather_frame = tk.Frame(self.root, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        self.weather_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Refresh button
        tk.Button(self.root, text="🔄 Refresh", command=self.get_weather,
                 bg="#e74c3c", fg="white", font=("Arial", 10)).pack(pady=10)
    
    def get_weather(self):
        """Lấy thời tiết từ Open-Meteo (free, no key)."""
        city = self.city_var.get().strip()
        if not city:
            messagebox.showerror("Lỗi", "Nhập tên thành phố!")
            return
        
        # Thread để không freeze GUI
        threading.Thread(target=self.fetch_weather, args=(city,), daemon=True).start()
    
    def fetch_weather(self, city):
        """Fetch data Open-Meteo."""
        try:
            # Tìm lat/lon city (Open-Meteo cần tọa độ)
            geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},VN&limit=1&appid=dummy"
            # Fallback tọa độ VN cities (hardcode cho nhanh)
            coords = {
                "Hanoi": (21.0285, 105.8542),
                "Saigon": (10.8231, 106.6297),
                "Danang": (16.0471, 108.2062),
                "Huế": (16.4637, 107.5909)
            }
            
            if city.title() in coords:
                lat, lon = coords[city.title()]
            else:
                messagebox.showwarning("Cảnh báo", f"City '{city}' dùng tọa độ mặc định Hanoi")
                lat, lon = 21.0285, 105.8542
            
            # Open-Meteo API (free, no key)
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,precipitation_probability&timezone=Asia/Bangkok"
            res = requests.get(url)
            data = res.json()
            
            current = data["current_weather"]
            self.weather_data = {
                "city": city.title(),
                "temp": current["temperature"],
                "wind": current["windspeed"],
                "time": datetime.now().strftime("%H:%M %d/%m"),
                "condition": self.get_condition(current["temperature"], data.get("hourly", {}))
            }
            
            # Update GUI main thread
            self.root.after(0, self.update_display)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi lấy dữ liệu: {str(e)}"))
    
    def get_condition(self, temp, hourly):
        """Xác định thời tiết từ temp."""
        if temp < 20:
            return "Lạnh ❄️"
        elif temp > 30:
            return "Nóng ☀️"
        else:
            return "Mát mẻ 🌤️"
    
    def update_display(self):
        """Hiển thị weather data."""
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        data = self.weather_data
        if not data:
            return
        
        # Icon thời tiết (vẽ đơn giản)
        canvas = tk.Canvas(self.weather_frame, width=100, height=100, bg="#ecf0f1", highlightthickness=0)
        canvas.pack(pady=20)
        draw = Image.new('RGBA', (100, 100), '#87CEEB')
        img_draw = ImageDraw.Draw(draw)
        if "Nóng" in data["condition"]:
            img_draw.ellipse([20, 20, 80, 80], fill="yellow")
        elif "Lạnh" in data["condition"]:
            img_draw.ellipse([25, 25, 75, 75], fill="lightblue")
        else:
            img_draw.rectangle([20, 30, 80, 70], fill="white")
        photo = ImageTk.PhotoImage(draw)
        canvas.create_image(50, 50, image=photo)
        canvas.image = photo
        
        # Info
        tk.Label(self.weather_frame, text=f"{data['city']}, VN", 
                font=("Arial", 24, "bold")).pack(pady=10)
        tk.Label(self.weather_frame, text=f"{data['temp']}°C", 
                font=("Arial", 36, "bold"), fg="#e74c3c").pack()
        tk.Label(self.weather_frame, text=data["condition"], 
                font=("Arial", 16)).pack(pady=5)
        tk.Label(self.weather_frame, text=f"Gió: {data['wind']} km/h | {data['time']}",
                font=("Arial", 12), fg="#7f8c8d").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
