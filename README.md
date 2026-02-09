# 🌤️ Weather VN App + API

Ứng dụng dự báo thời tiết Việt Nam với GUI Tkinter và FastAPI backend. Sử dụng Open-Meteo API (miễn phí, không cần key) để lấy dữ liệu thời tiết real-time.

## Demo
![Weather GUI](screenshots/weather-gui.png)
![API Docs](screenshots/api-docs.png)

## Tính năng
- ✅ **GUI Tkinter**: Giao diện đẹp, hiển thị nhiệt độ, gió, điều kiện thời tiết
- ✅ **6 thành phố VN**: Hanoi, Saigon, Danang, Hue, Haiphong, Cantho
- ✅ **FastAPI Backend**: Tạo API riêng từ dữ liệu Open-Meteo
- ✅ **Real-time data**: Cập nhật theo thời gian thực
- ✅ **Auto Swagger Docs**: http://localhost:8000/docs

## Cài đặt

### Yêu cầu
- Python 3.8+
- Pip

### Clone repo
```bash
git clone https://github.com/[username]/weather-vn-app.git
cd weather-vn-app
